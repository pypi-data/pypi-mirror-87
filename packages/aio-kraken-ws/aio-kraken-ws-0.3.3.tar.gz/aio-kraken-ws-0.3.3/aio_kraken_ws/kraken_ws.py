""" Module with the interface to interact with Kraken websocket API.
https://www.kraken.com/features/websocket-api
"""
import logging

from aio_kraken_ws.stream import Stream


logger = logging.getLogger(__name__)


def _cast_datasets(datasets):
    """ Ensure cast of datasets."""
    return [(str(pair), int(interval)) for pair, interval in datasets]


class KrakenWs:
    """ Interface to handle Kraken ws.

    ::

        kraken = await KrakenWs.create(callback)
        # or
        # kraken = KrakenWs(callback)
        # await kraken.start()

        await kraken.subscribe([("XBT/EUR", 1)]) # start subscription for interval 1 minute
        # → await callback("XBT/EUR",  # pair
        #                  1,  # interval
        #                  1568315100,  # open timestamp
        #                  8000.0,  # open price
        #                  8001.0,  # high price
        #                  7999.0,  # low price
        #                  8000.0,  # close price
        #                  15)  # volume
        await kraken.subscribe([("ETH/EUR", 1)]) # new subscription, doesn't stop the previsous one

        await kraken.unsubscribe([("XBT/EUR", 1), ("ETH/EUR", 1)]) # end of subscriptions

        await kraken.close() # shutdown → close ws

    """

    def __init__(self, callback, url="wss://ws.kraken.com", reset_period=60):
        """
        :param callback: coroutine call on new candle. Arguments are
            coroutine(pair: str, o: float, h: float, l: float, c: float, v: float, interval: int)
        :param str url: Kraken ws endpoint
        :param int reset_period: time in seconds. The ws connection is reset periodically.
        """
        logger.debug(f"connect to {url}")
        self.callback = callback
        self.url = url
        self.reset_period = reset_period
        self._stream = None
        self._pending_subscibre = []
        self._pending_unsubscibre = []

    @classmethod
    async def create(cls, callback, url="wss://ws.kraken.com", reset_period=60):
        """ Create and returns a running instance of KrakenWs.

        :param callback: coroutine call on new candle. Arguments are
            coroutine(pair: str, o: float, h: float, l: float, c: float, v: float, interval: int)
        :param str url: Kraken ws endpoint
        :param int reset_period: time in seconds. The ws connection is reset periodically.
        :returns: KrakenWs instance
        """
        kraken = cls(callback, url, reset_period)
        await kraken.start()
        logger.debug("KrakenWs instance created and started")
        return kraken

    async def start(self):
        """ Start the stream. """
        logger.debug("starting...")
        self._stream = Stream(self.url, self.callback, self.reset_period)
        for datasets in self._pending_subscibre:
            self._stream.subscribe(datasets)
            self._pending_subscibre = []
        for datasets in self._pending_unsubscibre:
            self._stream.unsubscribe(datasets)
            self._pending_unsubscibre = []
        await self._stream.start()

    def subscribe(self, datasets):
        """ Stream datasets.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minute
        """
        cast = _cast_datasets(datasets)
        logger.debug(f"subscribe to {cast}")
        if self._stream is not None:
            self._stream.subscribe(cast)
        else:
            self._pending_subscibre.append(cast)

    def unsubscribe(self, datasets):
        """ Stop streams.

        :param list((str,int)) datasets: list of (pair name, interval), interval is a time
            period in minute
        """
        cast = _cast_datasets(datasets)
        logger.debug(f"unsubscribe to {cast}")
        if self._stream is not None:
            self._stream.unsubscribe(cast)
        else:
            self._pending_unsubscibre.append(cast)

    @property
    def datasets(self):
        """ Datasets currently streamed.

        :returns: List of pair name, interval
        :rtype: list((str,int))
        """
        if self._stream is None:
            return []
        return list(self._stream.datasets)

    async def close(self):
        """ Stop all streams. """
        logger.info("Shutdown kraken ws.")
        if self._stream is not None:
            await self._stream.close()
