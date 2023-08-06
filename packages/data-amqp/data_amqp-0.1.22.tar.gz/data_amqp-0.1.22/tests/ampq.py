from data_amqp.amqp import AMQPData


amqp_options = {
    'code':'gnss',
    'vhost':'gpsdata',
    'exchange': 'exch_data',
    'host': '10.54.218.158',
    'credentials': ('gps','=0GPS0='),
    'qname':'gpsstream',
    'durable':True
}

value = None

mq = AMQPData(**amqp_options)

while not value == '-1':
    value = input("Entregame un mensaje para la cola gpsstream\n")
    enviar = {'msg': value}
    mq.send2gui(enviar)

