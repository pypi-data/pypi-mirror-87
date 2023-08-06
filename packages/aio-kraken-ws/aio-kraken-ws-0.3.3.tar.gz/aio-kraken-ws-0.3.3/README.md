aio-kraken-ws [![pipeline status](https://gitlab.com/botcrypto/aio-kraken-ws/badges/master/pipeline.svg)](https://gitlab.com/botcrypto/aio-kraken-ws/commits/master)
[![coverage report](https://gitlab.com/botcrypto/aio-kraken-ws/badges/master/coverage.svg)](https://gitlab.com/botcrypto/aio-kraken-ws/commits/master)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
===

A module to collect ohlc candles from Kraken using WebSockets that is asyncio friendly! Looking for automated trading tools? [Botcrypto](https://botcrypto.io) may interest you.

## Key features

- Subscribe to kraken data using a single WebSocket.
- Trigger a callback that is coroutine on each new closed candles from kraken.
- Easy subscription/unsubscription to datasets, i.e. [(PAIR, Unit Time)].
- Callback is regulary triggered at each end of the UT intervals, whatever is the number of data received by kraken.

## Getting started

#### Install

`pip install aio-kraken-ws`

#### Usage

```python
# check tests/learning/log_to_file.py for a complete example
async def callback(pair, interval, timestamp, o, h, l, c, v):
    """ A coroutine handling new candles.

    :param str pair:
    :param int interval: time in minutes
    :param int timestamp: candle open timestamp.
    :param float o: open price
    :param float h: high price
    :param float l: low price
    :param float c: close price
    :param float v: volume
    """
    with open("candles.txt", "a+") as file:
        file.write(f"[{pair}:{interval}]({timestamp},{o},{h},{l},{c},{v})\n")

kraken_ws = await KrakenWs.create(callback)
# subscribe to some datasets
kraken_ws.subscribe([("XBT/EUR", 1), ("ETH/EUR", 5)])
```

The `callback` function is called for each dataset at the end of each dataset's unit time interval.

E.g. if subscription start at 4h42.05 to the dataset `("XBT/EUR", 1)`, then callback is triggered at 4h43.00, at 4h44.00, at 4h45.00, etc... For `("XBT/EUR", 60)`, it would be at 5h00.00, at 6h00.00, etc... It's possible to get at most 10ms delay between the exact UT interval ending and the actual datetime of the call.

If **no** new data were received from Kraken during an interval, the callback is triggered with the latest known close price and v=0, as it's described in the following example.

E.g.
```python
kraken_ws.subscribe([("XBT/EUR", 1)])
# time.time() = 120
await callback("XBT/EUR", 1, 60, 42.0, 57.0, 19.0, 24.0, 150.0)
# time.time() = 180
await callback("XBT/EUR", 1, 120, 19.0, 24.0, 8.0, 10.0, 13.0)
# time.time() = 240 : no data received in 60s, i.e. no activity
await callback("XBT/EUR", 1, 180, 10.0, 10.0, 10.0, 10.0, 0.0)
```

### Error management

- An exception raised by the `callback` will be logged and it wont stop the streams
- If kraken send an error message, an `ERROR` log is emitted with the kraken payload
- If kraken send 'Subscription ohlc interval not supported', the related dataset is automatically unsubscripted

#### Warning

The `callback` should takes less than a minute to process. If the `callback` takes more than a minutes, a *warning* is emitted and you may lose market data.

Kraken WebSocket server seems to admit **20 subscriptions commands maximum**. Further commands seems to be ignored by the server.
**Hopfully, aio-kraken-ws manage this limitation for you!**

Moreover, after 24h a subscriptions seem to expire and no more market data is receive. To ensure we do not lose the stream of market data, **aio-kraken-ws** automatically reconnect and re-subscribe to the datasets every 30 minutes.

## Tests

You can find a wroking example of KrakenWs in `tests/learning/log_to_file.py`.

### Run tests locally

Clone the repo and install requirements
```sh
pip install -e .[test]
```

Run the suite tests
```sh
# unit tests - no call to kraken - fast
pytest --cov=aio_kraken_ws --cov-report= -v tests/unit

# integration tests - actual kraken subscription - slow
pytest --cov=aio_kraken_ws --cov-append -v -n 8 tests/integration
```

## Changelog

See https://cdlr75.gitlab.io/aio-kraken-ws/CHANGELOG.html
