#!/usr/bin/env python
from data_amqp.amqp import AMQPData
from tasktools.taskloop import TaskLoop
import asyncio
from networktools.colorprint import gprint, rprint


amqp_options = {
    'code': 'test',
    'vhost': '/gendata',
    'exchange': 'gendata',
    'host': 'localhost',
    "port": 5672,
    'credentials': ('recvdata', 'recvdata'),
    'queue_name': 'stations',
    'durable': True,
    "limit": 20,
    "routing_key": "gendata_stations",
    "consumer_tag": "gendata"
}

value = None

mq = AMQPData(**amqp_options)
mq.connect()
queue = asyncio.Queue()

from pprint import pprint

async def consume(*args, **kwargs):
    amqp = args[0]
    queue = args[1]
    print(amqp.channel.consume)
    count = 0
    for method_frame, properties, body in amqp.channel.consume('stations'):
        gprint(f"{method_frame}->{body}")
        amqp.channel.basic_ack(method_frame.delivery_tag)
        await queue.put(body)
        count += 1
        if count >= 1:
            break
    return args, kwargs

async def basic_consume(*args, **kwargs):
    print("Basic_consume")
    await asyncio.sleep(2)
    mq.channel.basic_consume("stations", print)
    return args, kwargs

async def read_queue(*args, **kwargs):
    queue = args[0]
    print("Leer cola", queue)
    await asyncio.sleep(.5)
    if not queue.empty():
        await queue.join()
        for i in range(queue.qsize()):
            elem = await queue.get()
            pprint(elem)
            queue.task_done()
    return [queue, *args], kwargs


loop = asyncio.get_event_loop()
task_a = TaskLoop(consume, [mq, queue], {})
task_a.create()
task_b = TaskLoop(read_queue, [queue], {})
task_b.create()
print(task_b)
loop.run_forever()
