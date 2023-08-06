from data_amqp.amqp import AMQPData

amqp_options = {
    'code':'gnss',
    'vhost':'/gendata',
    'exchange': 'gendata',
    'host': 'localhost',
    'port': 5672,
    'credentials': ('gendata','gendata'),
    'queue_name':'stations',
    "routing_key":"gendata_stations",
    'durable':True
}

value = None

mq = AMQPData(**amqp_options)

while not value == '-1':
    value = input("Entregame un mensaje para la cola gpsstream\n")
    enviar = {'msg': value}
    mq.send2gui(enviar)

