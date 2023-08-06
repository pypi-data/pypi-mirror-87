# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

from streamsx.topology.schema import StreamSchema
#
# Defines Message types with default attribute names and types.
_SPL_SCHEMA_STRING_MESSAGE = 'tuple<rstring message,rstring key>'
_SPL_SCHEMA_BLOB_MESSAGE = 'tuple<blob message,rstring key>'
_SPL_SCHEMA_STRING_MESSAGE_META = 'tuple<rstring message,rstring key,rstring topic,int32 partition,int64 offset,int64 messageTimestamp>'
_SPL_SCHEMA_BLOB_MESSAGE_META = 'tuple<blob message,rstring key,rstring topic,int32 partition,int64 offset,int64 messageTimestamp>'


class Schema:
    """
    Structured stream schemas for keyed messages for :py:class:`~streamsx.kafka.KafkaConsumer`, 
    and for streams that are published by :py:class:`~streamsx.kafka.KafkaProducer` to Kafka topics.
    
    The schemas
    
    * :py:const:`StringMessage`
    * :py:const:`BinaryMessage`
    
    have the attributes ``message``, and ``key``. They vary in the type for the 
    ``message`` attribute and can be used for :py:class:`~streamsx.kafka.KafkaConsumer` 
    and for the stream published with :py:class:`~streamsx.kafka.KafkaProducer`.
    
    The schemas
    
    * :py:const:`StringMessageMeta`
    * :py:const:`BinaryMessageMeta`
    
    have the attributes ``message``, ``key``, ``topic``, ``partition``, ``offset``, and ``messageTimestamp``. They vary in the type for the 
    ``message`` attribute and can be used for :py:class:`~streamsx.kafka.KafkaConsumer`.
    
    All schemas defined in this class are instances of `streamsx.topology.schema.StreamSchema`.
    
    The following sample uses structured schemas for publishing messages with keys to a 
    possibly partitioned topic in a Kafka broker. Then, it creates a consumer group 
    that subscribes to the topic, and processes the received messages in parallel channels
    partitioned by the message key::

        from streamsx.topology.topology import Topology
        from streamsx.topology.context import submit, ContextTypes
        from streamsx.topology.topology import Routing
        from streamsx.topology.schema import StreamSchema
        from streamsx.kafka.schema import Schema
        from streamsx.kafka import KafkaConsumer, KafkaProducer
        
        import random
        import time
        import json
        from datetime import datetime
        
        
        # Define a callable source for data that we push into Event Streams
        class SensorReadingsSource(object):
            def __call__(self):
                # This is just an example of using generated data,
                # Here you could connect to db
                # generate data
                # connect to data set
                # open file
                i = 0
                # wait that the consumer is ready before we start creating data
                time.sleep(20.0)
                while(i < 100000):
                    time.sleep(0.001)
                    i = i + 1
                    sensor_id = random.randint(1, 100)
                    reading = {}
                    reading["sensor_id"] = "sensor_" + str(sensor_id)
                    reading["value"] = random.random() * 3000
                    reading["ts"] = int(datetime.now().timestamp())
                    yield reading
        
        
        # parses the JSON in the message and adds the attributes to a tuple
        def flat_message_json(tuple):
            messageAsDict = json.loads(tuple['message'])
            tuple.update(messageAsDict)
            return tuple
        
        
        # calculate a hash code of a string in a consistent way
        # needed for partitioned parallel streams
        def string_hashcode(s):
            h = 0
            for c in s:
                h = (31 * h + ord(c)) & 0xFFFFFFFF
            return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        
        
        topology = Topology('KafkaGroupParallel')
        
        #
        # the producer part
        #
        # create the data and map them to the attributes 'message' and 'key' of the
        # 'Schema.StringMessage' schema for Kafka, so that we have messages with keys
        sensorStream = topology.source(
            SensorReadingsSource(),
            "RawDataSource"
            ).map(
                func=lambda reading: {'message': json.dumps(reading),
                                      'key': reading['sensor_id']},
                name="ToKeyedMessage",
                schema=Schema.StringMessage)
        # assume, we are running a Kafka broker at localhost:9092
        producer = KafkaProducer(config={'bootstrap.servers': 'localhost:9092'}, topic="ThreePartitions")
        sensorStream.for_each(producer)
        
        #
        # the consumer side
        #
        # subscribe, create a consumer group with 3 consumers
        
        consumerSchema = Schema.StringMessageMeta
        consumer = KafkaConsumer(config={'bootstrap.servers': 'localhost:9092'},
                                 topic="ThreePartitions",
                                 schema=consumerSchema)
        consumer.group_id = "my_consumer_group"
        consumer.group_size = 5
        
        received = topology.source(consumer, name="SensorSubscribe").end_parallel()
        
        # start a different parallel region partitioned by message key,
        # so that each key always goes into the same parallel channel
        receivedParallelPartitioned = received.parallel(
            5,
            routing=Routing.HASH_PARTITIONED,
            func=lambda x: string_hashcode(x['key']))
        
        # schema extension, here we use the Python 2.7, 3 way
        flattenedSchema = consumerSchema.extend(
            StreamSchema('tuple<rstring sensor_id, float64 value, int64 ts>'))
        
        receivedParallelPartitionedFlattened = receivedParallelPartitioned.map(
            func=flat_message_json,
            name='JSON2Attributes',
            schema=flattenedSchema)
        
        # validate by remove negativ and zero values from the streams,
        # pass only positive vaues and timestamps
        receivedValidated = receivedParallelPartitionedFlattened.filter(
            lambda tup: (tup['value'] > 0) and (tup['ts'] > 0),
            name='Validate')
        
        # end parallel processing and print the merged result stream to stdout log
        receivedValidated.end_parallel().print()
        
        submit(ContextTypes.DISTRIBUTED, topology)
    """

    StringMessage = StreamSchema (_SPL_SCHEMA_STRING_MESSAGE)
    """
    Stream schema with message and key, both being strings.

    The schema defines following attributes
    
    * message(str) - the message content
    * key(str) - the key for partitioning
    
    This schema can be used for both :py:class:`~streamsx.kafka.KafkaConsumer` 
    and for the stream published with :py:class:`~streamsx.kafka.KafkaProducer`.

     .. versionadded:: 1.2
    """

    StringMessageMeta = StreamSchema (_SPL_SCHEMA_STRING_MESSAGE_META)
    """
    Stream schema with message, key, and message meta data, where both message and key are strings.
    
    The schema defines following attributes
    
    * message(str) - the message content
    * key(str) - the key for partitioning
    * topic(str) - the Event Streams topic
    * partition(int) - the topic partition number (32 bit)
    * offset(int) - the offset of the message within the topic partition (64 bit)
    * messageTimestamp(int) - the message timestamp in milliseconds since epoch (64 bit)

    This schema can be used for :py:class:`~streamsx.kafka.KafkaConsumer`.

     .. versionadded:: 1.2
    """

    BinaryMessage = StreamSchema (_SPL_SCHEMA_BLOB_MESSAGE)
    """
    Stream schema with message and key, where the message is a binary object (sequence of bytes), and the key is a string.

    The schema defines following attributes
    
    * message(bytes) - the message content
    * key(str) - the key for partitioning
    
    This schema can be used for both :py:class:`~streamsx.kafka.KafkaConsumer` 
    and for the stream published with :py:class:`~streamsx.kafka.KafkaProducer`.

     .. versionadded:: 1.2
    """

    BinaryMessageMeta = StreamSchema (_SPL_SCHEMA_BLOB_MESSAGE_META)
    """
    Stream schema with message, key, and message meta data, where the message is a binary object (sequence of bytes), and the key is a string.
    
    The schema defines following attributes
    
    * message(bytes) - the message content
    * key(str) - the key for partitioning
    * topic(str) - the Event Streams topic
    * partition(int) - the topic partition number (32 bit)
    * offset(int) - the offset of the message within the topic partition (64 bit)
    * messageTimestamp(int) - the message timestamp in milliseconds since epoch (64 bit)

    This schema can be used for :py:class:`~streamsx.kafka.KafkaConsumer`.

     .. versionadded:: 1.2
    """

    pass
