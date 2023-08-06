"""
Prueba de concepto:

Este test:

Toma una cola de rabbitmq a la que llegan los datos
Activa la clase que lee el canales

lo envía a

un ciclo

Cada parte aparece en diferentes procesos

El módulo cycle_read se puede reemplazar por una GUI

"""

import asyncio
import concurrent.futures
from functools import partial
from multiprocessing import Manager
from websocketdatamanager.rabbitmq import ReadMQBroker
from networktools.environment import get_env_variable
from datetime import datetime, timedelta
from tasktools.taskloop import TaskLoop
from networktools.colorprint import rprint, bprint, gprint


async def cycle_read(*args, **kwargs):
    delta = kwargs.get("delta", 2)
    sleep = kwargs.get('sleep', .1)
    anterior = kwargs.get('anterior')
    while (ahora := datetime.now()) <= anterior + timedelta(seconds=delta):
        await asyncio.sleep(sleep)
    kwargs["anterior"] = ahora
    queue_status = args[0]
    rprint(f"Desde {anterior} hasta {ahora}")
    if not queue_status.empty():
        for i in range(queue_status.qsize()):
            msg = queue_status.get()
            queue_status.task_done()
            bprint("===RECIBIDO===")
            gprint(msg)
    bprint("===--------===" * 5)
    return args, kwargs


def read_queue(args, kwargs):
    loop = asyncio.get_event_loop()
    kwargs["anterior"] = datetime.now()
    print(f"In read queue {args}, {kwargs}")
    task = TaskLoop(cycle_read, args, kwargs)
    task.create()
    try:
        loop.run_forever()
    except Exception as e:
        raise e


if __name__ == '__main__':
    amqp_data = {
        'amqp': True,
        'code': 'status',
        'vhost': "gpsdata",
        'host': "10.54.217.95",
        'credentials': ("enugeojson_prod", "geognss_prod"),
        'queue_name': 'status_gnss',
        'routing_key': 'status',
        'exchange': 'status_exchange',
        'durable': True,
        'consumer_tag': 'mq2ws',
        "log_path": "./readmqbroker",
        "multiprocessing": True,
        "queue_destiny": "queue2read"
    }
    print(amqp_data)
    workers = 2
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        manager = Manager()
        queue_status = manager.Queue()
        set_queue = {"status": queue_status}
        amqp_data['queue2read'] = queue_status
        engine_opts = {"status": amqp_data}
        reader = ReadMQBroker(
            set_queue,
            engine_opts,
        )
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, reader.task_cycle)
        loop.run_in_executor(
            executor,
            partial(read_queue, [queue_status], {
                "delta": 10,
                "sleep": .1
            }))
        try:
            loop.run_forever()
        except Exception as e:
            raise e
