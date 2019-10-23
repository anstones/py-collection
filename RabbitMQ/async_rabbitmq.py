# coding: utf-8

import functools
import asyncio
import pika
from pika.adapters.asyncio_connection import AsyncioConnection


class AsyncConsumer(object):
    """This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, this class will stop and indicate
    that reconnection is necessary. You should look at the output, as
    there are limited reasons why the connection may be closed, which
    usually are tied to permission related issues or socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    """

    def __init__(self, logger, amqp_url, exchange_name, exchange_type, queue_name, routine_key, **kwargs):
        """
        Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param logger:
        :param str amqp_url: The AMQP url to connect with
        :param exchange_name:
        :param exchange_type:
        :param queue_name:
        :param routine_key:
        :param kwargs:
        """
        self._logger = logger
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._routine_key = routine_key
        self._kwargs = kwargs
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._consuming = False
        self._reconnect_delay = 0
        # In production, experiment with higher prefetch values for higher consumer throughput
        self._prefetch_count = 1

    def connect(self):
        """
        This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.adapters.asyncio_connection.AsyncioConnection

        """
        self._logger.info("connecting to %s", self._url)
        return AsyncioConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            self._logger.info("connection is closing or already closed")
        else:
            self._logger.info("closing connection")
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        """
        This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection: The connection

        """
        self._logger.info("connection opened")
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """
        This method is called by pika if the connection to RabbitMQ
        can't be established.

        :param pika.adapters.asyncio_connection.AsyncioConnection _unused_connection: The connection
        :param Exception err: The error

        """
        self._logger.error("connection open failed: %s", err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        """
        This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection _unused_connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of connection.

        """
        self._channel = None
        if not self._closing:
            self._logger.warning("connection closed, reconnect necessary: %s", reason)
            self.reconnect()

    def reconnect(self):
        """
        Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.

        """
        if not self._closing:
            self._connection.ioloop.call_later(self._get_reconnect_delay(), self.run)

    def open_channel(self):
        """
        Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        self._logger.info("creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """
        This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self._logger.info("channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange()

    def add_on_channel_close_callback(self):
        """
        This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self._logger.info("adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        """
        Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param Exception reason: why the channel was closed

        """
        self._logger.warning("Channel %i was closed: %s", channel, reason)
        self.close_connection()

    def setup_exchange(self):
        """
        Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.
        """
        self._logger.info("declaring exchange: %s", self._exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(self.on_exchange_declare_ok, user_data=self._exchange_name)
        self._channel.exchange_declare(
            exchange=self._exchange_name,
            exchange_type=self._exchange_type,
            passive=self._kwargs.get("exchange_passive", False),
            durable=self._kwargs.get("exchange_durable", False),
            auto_delete=self._kwargs.get("exchange_auto_delete", False),
            internal=self._kwargs.get("exchange_internal", False),
            arguments=self._kwargs.get("exchange_arguments"),
            callback=cb)

    def on_exchange_declare_ok(self, _unused_frame, user_data):
        """
        Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC command.

        :param pika.Frame.Method _unused_frame: Exchange.DeclareOk response frame
        :param str|unicode user_data: Extra user data (exchange name)

        """
        self._logger.info("exchange declared: %s", user_data)
        self.setup_queue()

    def setup_queue(self):
        """
        Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        """
        self._logger.info("declaring queue %s", self._queue_name)
        cb = functools.partial(self.on_queue_declare_ok, user_data=self._queue_name)
        self._channel.queue_declare(queue=self._queue_name,
                                    passive=self._kwargs.get("queue_passive", False),
                                    durable=self._kwargs.get("queue_durable", False),
                                    exclusive=self._kwargs.get("queue_exclusive", False),
                                    auto_delete=self._kwargs.get("queue_auto_delete", False),
                                    arguments=self._kwargs.get("queue_arguments"),
                                    callback=cb)

    def on_queue_declare_ok(self, _unused_frame, user_data):
        """
        Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode user_data: Extra user data (queue name)

        """
        queue_name = user_data
        self._logger.info("binding %s to %s with %s", self._exchange_name, queue_name, self._routine_key)
        cb = functools.partial(self.on_bind_ok, user_data=queue_name)
        self._channel.queue_bind(
            queue_name,
            self._exchange_name,
            routing_key=self._routine_key,
            callback=cb)

    def on_bind_ok(self, _unused_frame, user_data):
        """
        Invoked by pika when the Queue.Bind method has completed. At this
        point we will set the prefetch count for the channel.

        :param pika.frame.Method _unused_frame: The Queue.BindOk response frame
        :param str|unicode user_data: Extra user data (queue name)

        """
        self._logger.info("queue bound: %s", user_data)
        self.set_qos()

    def set_qos(self):
        """
        This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.

        """
        self._channel.basic_qos(prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        """
        Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame

        """
        self._logger.info('QOS set to: %d', self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """
        This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        self._logger.info("issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self._queue_name, self.on_message)
        self._consuming = True

    def add_on_cancel_callback(self):
        """
        Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        self._logger.info("adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """
        Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self._logger.info("consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """
        Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver basic_deliver method
        :param pika.Spec.BasicProperties properties:
        :param bytes body: The message body

        """
        self._logger.debug('received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body)
        if isinstance(body, bytes):
            message = body.decode("utf-8")
        else:
            message = body
        _ = asyncio.ensure_future(self.process_message(message))
        self.acknowledge_message(basic_deliver.delivery_tag)

    async def process_message(self, raw_message):
        """
        subclass should rewrite this method to process the message received
        :param message:
        :return:
        """
        raise NotImplementedError()

    def acknowledge_message(self, delivery_tag):
        """
        Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        self._logger.info("acknowledging message %s", delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """
        Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            self._logger.info("sending a Basic.Cancel RPC command to RabbitMQ")
            cb = functools.partial(self.on_cancel_ok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancel_ok(self, _unused_frame, user_data):
        """
        This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode user_data: Extra user data (consumer tag)

        """
        self._consuming = False
        self._logger.info("rabbitMQ acknowledged the cancellation of the consumer: %s", user_data)
        self.close_channel()

    def close_channel(self):
        """
        Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        self._logger.info("closing the channel")
        self._channel.close()

    def run(self):
        """
        Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the AsyncioConnection to operate.

        """
        self._connection = self.connect()

    def stop(self):
        """
        Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        if not self._closing:
            self._closing = True
            self._logger.info('stopping')
            self.stop_consuming()
            self._logger.info('stopped')

    def _get_reconnect_delay(self):
        if self._consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
