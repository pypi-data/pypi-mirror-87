"""Slurry websocket client."""

from async_generator import aclosing
from slurry import Section
import trio
from trio_websocket import connect_websocket, connect_websocket_url
from trio_websocket import ConnectionTimeout, HandshakeError, DisconnectionTimeout
import ujson

CONN_TIMEOUT = 60 # default connect & disconnect timeout, in seconds
MESSAGE_QUEUE_SIZE = 1
MAX_MESSAGE_SIZE = 2 ** 20 # 1 MiB
RECEIVE_BYTES = 4 * 2 ** 10 # 4 KiB

class Websocket(Section):
    """Create a WebSocket client connection to a URL.

    The websocket will connect when the pipeline is started.

    :param str url: A WebSocket URL, i.e. `ws:` or `wss:` URL scheme.
    :param ssl_context: Optional SSL context used for ``wss:`` URLs. A default
        SSL context is used for ``wss:`` if this argument is ``None``.
    :type ssl_context: ssl.SSLContext or None
    :param subprotocols: An iterable of strings representing preferred
        subprotocols.
    :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
        HTTP header key/value pairs to send with the connection request. Note
        that headers used by the WebSocket protocol (e.g.
        ``Sec-WebSocket-Accept``) will be overwritten.
    :param int message_queue_size: The maximum number of messages that will be
        buffered in the library's internal message queue.
    :param int max_message_size: The maximum message size as measured by
        ``len()``. If a message is received that is larger than this size,
        then the connection is closed with code 1009 (Message Too Big).
    :param float connect_timeout: The number of seconds to wait for the
        connection before timing out.
    :param float disconnect_timeout: The number of seconds to wait when closing
        the connection before timing out.
    :param bool dumps: Unpack json output.
    :param bool loads: Pack json input.

    :raises HandshakeError: for any networking error,
        client-side timeout (ConnectionTimeout, DisconnectionTimeout),
        or server rejection (ConnectionRejected) during handshakes.
    """
    def __init__(self, url, ssl_context=None, *, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        parse_json=True):
        super().__init__()
        self.url = url
        self.ssl_context = ssl_context
        self.host = None
        self.port = None
        self.resource = None
        self.use_ssl = None
        self.subprotocols = subprotocols
        self.extra_headers = extra_headers
        self.message_queue_size = message_queue_size
        self.max_message_size = max_message_size
        self.connect_timeout = connect_timeout
        self.disconnect_timeout = disconnect_timeout
        self.parse_json = parse_json

    @classmethod
    def create(cls, host, port, resource, *, use_ssl, subprotocols=None,
        extra_headers=None,
        message_queue_size=MESSAGE_QUEUE_SIZE, max_message_size=MAX_MESSAGE_SIZE,
        connect_timeout=CONN_TIMEOUT, disconnect_timeout=CONN_TIMEOUT,
        parse_json=True):
        """Alternative client factory which creates a WebSocket client connection to a host/port.

        The websocket will connect when the pipeline is started.

        :param str host: The host to connect to.
        :param int port: The port to connect to.
        :param str resource: The resource, i.e. URL path.
        :param use_ssl: If this is an SSL context, then use that context. If this is
            ``True`` then use default SSL context. If this is ``False`` then disable
            SSL.
        :type use_ssl: bool or ssl.SSLContext
        :param subprotocols: An iterable of strings representing preferred
            subprotocols.
        :param list[tuple[bytes,bytes]] extra_headers: A list of 2-tuples containing
            HTTP header key/value pairs to send with the connection request. Note
            that headers used by the WebSocket protocol (e.g.
            ``Sec-WebSocket-Accept``) will be overwritten.
        :param int message_queue_size: The maximum number of messages that will be
            buffered in the library's internal message queue.
        :param int max_message_size: The maximum message size as measured by
            ``len()``. If a message is received that is larger than this size,
            then the connection is closed with code 1009 (Message Too Big).
        :param float connect_timeout: The number of seconds to wait for the
            connection before timing out.
        :param float disconnect_timeout: The number of seconds to wait when closing
            the connection before timing out.
        :param bool dumps: Unpack json output.
        :param bool loads: Pack json input.

        :raises HandshakeError: for any networking error,
            client-side timeout (ConnectionTimeout, DisconnectionTimeout),
            or server rejection (ConnectionRejected) during handshakes.
        """
        websocket = cls(None, None, subprotocols=subprotocols,
            extra_headers=extra_headers,
            message_queue_size=message_queue_size, max_message_size=max_message_size,
            connect_timeout=connect_timeout, disconnect_timeout=disconnect_timeout,
            parse_json=parse_json)
        websocket.host = host
        websocket.port = port
        websocket.resource = resource
        websocket.use_ssl = use_ssl

        return websocket

    async def pump(self, input, output):
        async def send_task(connection):
            send_message = connection.send_message
            async with aclosing(input) as aiter:
                async for message in aiter:
                    await send_message(message)

        async def send_json_task(connection):
            send_message = connection.send_message
            async with aclosing(input) as aiter:
                async for item in aiter:
                    await send_message(ujson.dumps(item))

        async def receive_task(connection):
            get_message = connection.get_message
            send = output.send
            while True:
                await send(await get_message())

        async def receive_json_task(connection):
            get_message = connection.get_message
            send = output.send
            while True:
                await send(ujson.loads(await get_message()))

        async with trio.open_nursery() as nursery:
            try:
                with trio.fail_after(self.connect_timeout):
                    if self.url:
                        connection = await connect_websocket_url(nursery,
                            self.url, self.ssl_context,
                            subprotocols=self.subprotocols,
                            extra_headers=self.extra_headers,
                            message_queue_size=self.message_queue_size,
                            max_message_size=self.max_message_size)
                    else:
                        connection = await connect_websocket(nursery, self.host, self.port,
                            self.resource, use_ssl=self.use_ssl, subprotocols=self.subprotocols,
                            extra_headers=self.extra_headers,
                            message_queue_size=self.message_queue_size,
                            max_message_size=self.max_message_size)
            except trio.TooSlowError:
                raise ConnectionTimeout from None
            except OSError as e:
                raise HandshakeError from e
            try:
                if input is not None:
                    if self.parse_json:
                        nursery.start_soon(send_json_task, connection)
                    else:
                        nursery.start_soon(send_task, connection)
                if self.parse_json:
                    await receive_json_task(connection)
                else:
                    await receive_task(connection)
            finally:
                try:
                    with trio.fail_after(self.disconnect_timeout):
                        await connection.aclose()
                except trio.TooSlowError:
                    raise DisconnectionTimeout from None
