from networktools.geo import (rad2deg, deg2rad, radius, sph_rotation_matrix,
                              llh2ecef, ecef2llh, ecef2neu)
from networktools.time import timestamp, gps_week2time, gps_time
from networktools.statistics import matrix_VCV, rotate
from networktools.colorprint import gprint, rprint, bprint
from data_geo.geojson import GeoJSONData
import json
import pika
import copy
import queue
# from networktools.colorprint import gprint, bprint, rprint
import asyncio
from datadbs.general import GeneralData
from tasktools.taskloop import TaskLoop
from pprint import pprint


class AMQPData(GeneralData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creds = kwargs.get('credentials', [])
        self.vhost = kwargs.get('vhost', '/')
        self.exchange = kwargs.get('exchange', '')
        self.exch_type = kwargs.get('exchange_type', 'fanout')
        self.queue_name = kwargs.get('queue_name', 'status_gnss')
        self.routing_key = kwargs.get('routing_key', 'status')
        self.consumer_tag = kwargs.get('consumer_tag', 'gnss')
        self.durable = kwargs.get('durable', True)
        self.limit = kwargs.get('limit', 5)
        self.ping = kwargs.get('ping', 30)
        self.multi = kwargs.get('multiprocessing', False)
        self.ttl = kwargs.get('ttl',1200000)
        self.source = kwargs.get('source',False)
        try:
            self.connect()
        except Exception as e:
            self.logger.exception(
                "Error en conexión Rabbitmq. %s, args %s, kwargs %s" %
                (e, args, kwargs))

    def connect(self):
        try:
            self.credentials = pika.PlainCredentials(*self.creds)
        except Exception as e:
            self.logger.exception("Error creando credenciales Rabbitmq")
            raise e
        try:
            self.parameters = pika.ConnectionParameters(
                host=self.host,
                virtual_host=self.vhost,
                credentials=self.credentials,
                heartbeat=self.ping)
        except Exception as e:
            self.logger.exception("Error conectando parámetros Rabbitmq")
            raise e
        try:
            self.connection = pika.BlockingConnection(self.parameters)
        except Exception as e:
            self.logger.exception(
                "Error conectando Rabbitmq, bloquing connection")
            raise e
        try:
            self.channel = self.connection.channel()
            # bind by default to:
            # conecta exchange con queue
            self.connected = True
        except Exception as e:
            self.logger.exception("Error conectando canal Rabbitmq")
            raise e
        try:
            bprint(f"Queue binding on connection: {self.queue_name} <-> source: {self.source}")
            if self.source:
                self.channel.queue_declare(self.queue_name, 
                    durable=self.durable, 
                    arguments={'x-message-ttl' : self.ttl})
                self.channel.queue_bind(self.queue_name, self.exchange, self.routing_key)
            else:
                self.queue_name = self.channel.queue_declare("csn_ppp",exclusive=True)[0]
                self.channel.queue_bind(self.queue_name, exchange=self.exchange)
        except Exception as e:
            self.logger.exception("Error declaring queue -> %s" % e)
            self.connected = False
            raise e

    def reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        self.should_reconnect = True
        self.stop()

    def manage_data(self, geojson):
        value = copy.deepcopy(geojson)
        if 'DT_GEN' in value['properties'].keys():
            del value['properties']['DT_GEN']
        if 'dt' in value['properties'].keys():
            del value['properties']['dt']
        text = json.dumps(value)
        try:
            res = self.publish(self.exchange, self.routing_key,
                               "{}\n".format(text))
        except Exception as e:
            self.logger.exception("Error publicando datos -> %s, text" %
                                  (e, text))
        del value
        return geojson

    def manage_json_data(self, value):
        text = json.dumps(value)
        print("Exchange", self.exchange, self.routing_key)
        res = self.publish(self.exchange, self.routing_key,
                           f"{text}\n")
        return value

    def send2gui(self, to_gui):
        try:
            text = json.dumps(to_gui)
            print("Exchange", self.exchange, self.routing_key)
            res = self.publish(self.exchange, self.routing_key,
                               f"{to_gui}\n")
            return res
        except Exception as e:
            self.logger("Exception en send a gui %s" % e)
            raise e

    def publish(self, exchange, key, msg):
        sended = False
        while not sended:
            try:
                self.channel.basic_publish(exchange=exchange,
                                           routing_key=self.routing_key,
                                           body=msg)
                sended = True
            except Exception as e:
                self.connected = False
                print("Fail to send %s" % e)
                self.connect()

    def read_from_gui(self):
        data = []
        count = 0
        for method_frame, properties, body in self.channel.consume(
                self.queue_name):
            try:
                strb = str(body, 'utf-8').replace("'", "\"")
                new_json = json.loads(strb)
            except Exception as e:
                self.logger.exception("Error en leer desde gui %s" % e)
                raise e
            data.append(new_json)
            self.channel.basic_ack(method_frame.delivery_tag)
            count += 1
            if count >= 24:
                break
        return data

    async def consume_mq(self, *args, **kwargs):
        queue = args[0]
        active = args[1]
        count = 0
        consumer_args = self.get_consumer_args()
        for method_frame, properties, body in self.channel.consume(
                *consumer_args):
            try:
                strb = str(body, 'utf-8').replace("'", "\"")
                new_json = json.loads(strb)
            except Exception as e:
                self.logger.exception(
                    "Error en transformar json, consume_mq, error %s" % e)
                raise e
            if active:
                if isinstance(queue, queue.Queue):
                    queue.put(new_json)
                elif isinstance(queue, asyncio.queue.Queue):
                    await queue.put(new_json)
                elif self.multi:
                    queue.put(new_json)
            else:
                self.logger.info("Consumeindo json %s" % json)
            # self.channel.basic_ack(method_frame.delivery_tag)
            count += 1
            if count >= 24:
                break
        return args, kwargs

    def get_consumer_args(self):
        return [self.queue_name, self.consumer_tag]


    async def consume_exchange_mq(self, *args, **kwargs):
        queue_destiny = args[0]
        active = args[1]
        count = 0
        consumer_args = self.get_consumer_args()
        print("Consuming from exchange", consumer_args)
        for method_frame, properties, body in self.channel.consume(
                *consumer_args):
            try:
                strb = str(body, 'utf-8').replace("'", "\"")
                new_json = json.loads(strb)
            except Exception as e:
                self.logger.exception(
                    "Error on consume_exchange_mq convert json %s, error %e" %
                    (body, e))
                raise e
            if active:
                if isinstance(queue_destiny, queue.Queue):
                    queue_destiny.put(new_json)
                elif isinstance(queue_destiny, asyncio.Queue):
                    await queue_destiny.put(new_json)
                elif self.multi:
                    queue_destiny.put(new_json)
                else:
                    print("No enviado")
            else:
                self.logger.info("Consumeindo json %s" % json)
            count += 1
            if count >= self.limit:
                break
        return args, kwargs

    def create_task(self, queue_mq2ws, active):
        try:
            loop = asyncio.get_event_loop()
            args = [queue_mq2ws, active]
            kwargs = {}
            task = TaskLoop(self.consume_mq, args, kwargs)
            task.create()
        except Exception as e:
            self.logger.exception("Error on create_task RMQ %s, error %e" %
                                  (queue_mq2ws, e))
        return loop, task

    def create_exchange_task(self, queue_mq2ws, active):
        try:
            loop = asyncio.get_event_loop()
            args = [queue_mq2ws, active]
            kwargs = {}
            task = TaskLoop(self.consume_exchange_mq, args, kwargs)
            print("Tarea consumir data", task)
            task.create()
        except Exception as e:
            self.logger.exception(
                "Error on create_exchange_task RMQ %s, error %e" %
                (queue_mq2ws, e))
        return loop, task

    def consume_mq_task(self, queue_mq2ws, active):
        loop, task = self.create_task(queue_mq2ws, active)
        if not loop.is_running():
            loop.run_forever()
