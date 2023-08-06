""" Manage datasets streams via websockets. """
import asyncio
from collections import namedtuple, defaultdict
from contextlib import suppress
import copy
import json
import logging
import time
import websockets


logger = logging.getLogger(__name__)


async def close_task(task):
    if task is not None and not task.done():
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


class Stream:
    """ Manage a socket and datasets. """

    def __init__(self, url, callback, reset_period):
        """
        :param str url: websocket server endpoint.
        :param coroutine callback: coroutine triggered on new candle.
        :param int reset_period: time in seconds. The ws connection is reset periodically.
        """
        self.url = url
        self.callback = callback
        self.reset_period = reset_period
        self._datasets_to_add = set()
        self._datasets_to_remove = set()
        self._ws = None
        self._worker_task = None
        self._read_task = None
        self._watchdog_task = None
        self._builders = {}
        self._read_is_over = asyncio.Event()  # event that trigger the watchdog

    @classmethod
    async def create(cls, url, callback, reset_period):
        """ Start to subscribe using ws.

        :param str url: websocket server endpoint.
        :param coroutine callback: coroutine triggered on new candle.
        :param int reset_period: time in seconds. The ws connection is reset periodically.
        :returns: Stream instance.
        """
        stream = cls(url, callback, reset_period)
        await stream.start()
        return stream

    async def start(self):
        """ Bring up the stream. """
        await self._connect()
        self._worker_task = asyncio.ensure_future(self.worker())
        self._watchdog_task = asyncio.ensure_future(self.watchdog())
        await self._start_read()

    @property
    def datasets(self):
        """ All datasets currently streamed. """
        return set(self._builders.keys()
                   ).union(self._datasets_to_add
                           ).difference(self._datasets_to_remove)

    async def _connect(self):
        """ Acquire websocket connection. """
        logger.info(f"connect to {self.url}")
        while True:
            try:
                self._ws = await asyncio.wait_for(websockets.connect(self.url), timeout=5)
                break
            except Exception:
                logger.exception(f"Fail to connect to {self.url}... Retry in a second.")
            await asyncio.sleep(1)

    async def _close_connection(self):
        """ Stop socket connection. """
        logger.info(f"close connection")
        if self._ws is not None:
            await self._ws.close()

    async def _start_read(self):
        """ Get ready to receive message from the ws. """
        start_event = asyncio.Event()
        self._read_task = asyncio.ensure_future(self._read(start_event))
        await start_event.wait()

    async def _send(self, data):
        """ Send a command to the server.

        :param dict data:
        """
        logger.info(f"→ {data}")
        await self._ws.send(json.dumps(data))

    def subscribe(self, datasets):
        """ Make a new subscription.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minutes
        """
        for dataset in datasets:
            self._datasets_to_add.add(dataset)

    def unsubscribe(self, datasets):
        """ Unsubscribe to datasets.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minutes
        """
        for dataset in datasets:
            self._datasets_to_remove.add(dataset)

    async def close(self):
        """ Stop to subscribe. """
        logger.debug(f"close stream")
        await close_task(self._watchdog_task)
        await close_task(self._worker_task)
        await self._close_connection()
        if self._read_task is not None:
            with suppress(websockets.exceptions.ConnectionClosedError):
                await self._read_task

    async def watchdog(self):
        """ Task handling ws deconnection. """
        while True:
            await self._read_is_over.wait()
            self._read_is_over.clear()
            logger.warning("reset ws connection")
            try:
                await self._reconnect()
            except websockets.exceptions.InvalidStatusCode as exc:
                if exc.status_code == 429:
                    logger.exception("Too many requests. Sleep 60 sec")
                    await asyncio.sleep(60)
                else:
                    logger.exception("fail to reconnect")
                self._read_is_over.set()
            except Exception:
                logger.exception("fail to reconnect")
                self._read_is_over.set()
            finally:
                await asyncio.sleep(1)

    async def _reconnect(self):
        """ Clean connection and start new subsriptions to current datasets. """
        logger.debug(f"reconnect")
        delay = 20
        while True:
            try:
                return await asyncio.wait_for(self._reconnect_actions(),
                                              timeout=delay)
            except asyncio.TimeoutError:
                logger.warning(f"Fail to reconnect with {delay}seconds. Retry...")

    async def _reconnect_actions(self):
        """ To do to reset the connection. """
        await self._close_connection()
        await self._connect()
        await self._start_read()
        await self._subscribe(self.datasets)

    async def _read(self, start_event):
        """ Background task that handle incoming data from the ws.

        :raises: websockets.exceptions.ConnectionClosed when subscription is over

        ::

            [823,
              ['1568266025.580083',
               '1568266080.000000',
               '0.00009900',
               '0.00009900',
               '0.00009900',
               '0.00009900',
               '0.00009900',
               '568.44750717',
               1],
              'ohlc-1',
              'XTZ/XBT']
        """
        start_event.set()
        logger.info("ready to receive data from Kraken.")
        async for message in self._ws:
            logger.debug(f"← {message}")
            try:
                await self._process_new_msg(message)
            except Exception:
                logger.exception(f"fail to process {message}")

        self._read_is_over.set()

    async def _process_new_msg(self, message):
        """ Process incoming messages from the kraken.

        :param str message: data from kraken ws.
        """
        msg = json.loads(message)
        if isinstance(msg, dict):
            if msg.get("status") == "error":
                # message is an error message...
                logger.error(msg)
                await self._manage_errors(msg)
            if msg.get("event") == "systemStatus":
                # Status sent on connection or system status changes.
                if msg.get("status") == "online":
                    logger.info(msg)
                else:
                    logger.warning(msg)
            return
        try:
            _, data, interval_type, pair = msg
            _, interval = interval_type.split('-')
            interval = int(interval)
        except ValueError:
            logger.debug(f"message ignored: {message}")
        else:
            # message is ohlc data...
            builder = self._get_ohlc_buidler(pair, interval)
            builder.new_data(data)

    async def _manage_errors(self, data):
        """ We received an error from the Kraken API. This method handle these errors.

        :param dict data: the kraken payload
        """
        if data.get("errorMessage") == "Subscription ohlc interval not supported":
            # unsubscribe to the dataset
            pair = data["pair"]
            interval = data["subscription"]["interval"]
            logger.warning(f"Unsubscribe to ({pair},{interval})")
            await self._unsubscribe([(pair, interval)])

    async def _subscribe(self, datasets):
        """ Perfom subscribe command.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minutes
        """
        intervals = self._group_pairs_by_interval(datasets)
        for interval, pairs in intervals.items():
            for pair in pairs:
                self._get_ohlc_buidler(pair, interval)
            await self._send({
                "event": "subscribe",
                "pair": pairs,
                "subscription": {
                    "name": "ohlc",
                    "interval": interval
                }
            })

    async def _unsubscribe(self, datasets):
        """ Perfom unsubscribe command.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minutes
        """
        intervals = self._group_pairs_by_interval(datasets)
        for interval, pairs in intervals.items():
            await self._send({
                "event": "unsubscribe",
                "pair": pairs,
                "subscription": {
                    "name": "ohlc",
                    "interval": interval
                }
            })
            for pair in pairs:
                self._del_ohlc_builder(pair, interval)

    async def _manage_subscriptions(self):
        """ Reset subsciptions to kraken server if necessary to get less than
        20 subsciptions commands (limit from Kraken Server).
        """
        await self._unsubscribe(self._datasets_to_remove)
        self._datasets_to_remove = set()
        if self._datasets_to_add:
            to_unsubscribe = self._builders.keys()
            to_add = self._datasets_to_add.union(to_unsubscribe)
            await self._unsubscribe(to_unsubscribe)
            await self._subscribe(to_add)
            self._datasets_to_add = set()

    async def worker(self):
        """ Periodically run and trigger callback with closed candles builded. """
        while True:
            try:
                await self._worker_job()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Error doing the job")
                await asyncio.sleep(1)

    @staticmethod
    def is_new_candle(dataset, timestamp):
        _, interval = dataset
        return timestamp % (interval * 60) == 0

    async def _worker_job(self):
        """ Actual job. """
        last_subsriptions_update = int(time.time())
        timestamp = int(time.time())
        await self._manage_subscriptions()
        now = int(time.time())
        if now - timestamp < 60:
            await self._sleep_until_next_interval()
        now = int(time.time())
        timestamp = now - (now % 60)

        await asyncio.gather(*[
            self._trigger_callback(timestamp, dataset, builder)
            for dataset, builder in self._builders.items()
            if self.is_new_candle(dataset, timestamp)
        ])

        exc_time = int(time.time()) - now
        if exc_time >= 60:
            logger.warning("Callback tooks more than a minute to process.")

        if timestamp - last_subsriptions_update >= self.reset_period:
            # Reset subscriptions.
            last_subsriptions_update = timestamp
            # Shutdown the watchdog.
            await close_task(self._watchdog_task)
            # Reset connection.
            await self._reconnect()
            # Restart the watchdog.
            self._read_is_over = asyncio.Event()
            self._watchdog_task = asyncio.ensure_future(self.watchdog())

    async def _trigger_callback(self, timestamp, dataset, builder):
        pair, interval = dataset
        ohlc = builder.get_ohlc(timestamp - interval * 60)
        if ohlc is None:
            return
        logger.info(f"new candle ({pair}, {interval}, *{ohlc})")
        try:
            await self.callback(pair, interval, *ohlc)
        except Exception:
            logger.exception("error with callback processing "
                             f"({pair}, {interval}, *{ohlc})")

    def _get_ohlc_buidler(self, pair, interval):
        """
        :param str pair:
        :param int interval:
        :rtype: OhlcBuilder
        """
        try:
            return self._builders[(pair, interval)]
        except KeyError:
            pass

        builder = OhlcBuilder(interval)
        self._builders[(pair, interval)] = builder
        return builder

    def _del_ohlc_builder(self, pair, interval):
        """
        :param str pair:
        :param int interval:
        """
        try:
            del self._builders[(pair, interval)]
        except KeyError:
            pass

    @staticmethod
    def _group_pairs_by_interval(datasets):
        """ Helper to format a dataset. """
        intervals = defaultdict(list)
        for pair, interval in datasets:
            intervals[interval].append(pair)
        return intervals

    @staticmethod
    async def _sleep_until_next_interval():
        """ Sleep until next UT interval.
        Precision is 10ms max after the exact date according to the system.
        """
        now = int(time.time() * 100)
        to_sleep = (6000 - (now % 6000)) / 100
        await asyncio.sleep(to_sleep)


Candle = namedtuple("Candle", "t, o, h, l, c, v")


class OhlcBuilder:
    """ Build closed candle for a market from Kraken data. """

    def __init__(self, interval):
        """
        :param int interval: in minute
        """
        self.interval_sec = interval * 60
        self.candle = None  # current candle
        self._next_candle_tmp = self.next_timestamp()
        self.last_candle = None  # latest closed candles

    def next_timestamp(self):
        """ Start time of the next candle. """
        now = int(time.time())
        return now - (now % self.interval_sec) + self.interval_sec

    def new_data(self, data):
        """ Build current candle with data received from the websocket.

        :param data: part of message of the kraken msg that contain market data.
        """
        try:
            tmp, end_tmp, o, h, l, c, _, v, _ = data
        except ValueError:
            logger.debug(f"data ignored: {data}")
            return

        tmp = float(tmp)
        end_tmp = int(float(end_tmp))

        timestamp = end_tmp - self.interval_sec
        candle = Candle(timestamp, float(o), float(h), float(l), float(c), float(v))

        if candle.t >= self._next_candle_tmp:
            self._next_candle_tmp = self.next_timestamp()
            self.last_candle = copy.deepcopy(self.candle or candle)
            self.candle = candle

        self.candle = candle
        logger.debug(f"current candle (ut:{self.interval_sec}):{self.candle}")

    def get_ohlc(self, timestamp):
        """ Get closed candle that start at the given timestamp.

        :param int timestamp:
        :returns: dump of the candle or None
        """
        # we do not have data yet
        if self.candle is None:
            return None

        # the latest close candle match the timestamp
        if self.last_candle is not None and timestamp == self.last_candle.t:
            return self._dump_to_ohlc(self.last_candle)

        # last data receiv is the most up to date.
        if timestamp - self.candle.t <= self.interval_sec:
            return self._dump_to_ohlc(self.candle)

        # no activity
        if timestamp - self.candle.t > self.interval_sec:
            close = self.candle.c
            return [timestamp, close, close, close, close, 0]

        return None

    @staticmethod
    def _dump_to_ohlc(candle):
        return [candle.t, candle.o, candle.h, candle.l, candle.c, candle.v]
