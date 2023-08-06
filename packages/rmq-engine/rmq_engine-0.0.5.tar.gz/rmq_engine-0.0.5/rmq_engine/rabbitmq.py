from websocketdatamanager.rmq_engine import RMQEngine
from tasktools.taskloop import TaskLoop
import asyncio


class ReadMQBroker:
    """
    This class pretends to create a knut in what receive data from RMQ queues and send directly to the objects form dj-collector on the database
    """

    def __init__(self, queue_set, engine_opts, step=0.1, *args, **kwargs):
        self.step = step
        self.queue_set = queue_set
        self.engine_opts = engine_opts
        self.engine = False

    async def cycle_read_from_rmq(self, *args, **kwargs):
        engine = args[0]
        v = args[1]
        channels = args[2]
        if v == 0:
            aux_set = set()
            for channel in channels:
                rmq = engine.get(channel)
                try:
                    rmq.connect()
                except Exception as e:
                    print(f'''Error on connection to dj es -> channel {channel},
                          error {e}''')
                    v = 0
                    return [engine, v, channels], {"error": "No se puedo conectar"}
                aux_set.add(channel)
            for channel in aux_set:
                channels.remove(channel)
            aux_set = None
            v += 1
            await asyncio.sleep(self.step)
            return [engine, v, channels], {}
        else:
            for channel, rmq in engine.items():
                try:

                    queue = self.queue_set.get(channel)
                    # breakpoint()
                    queue, active = await rmq.amqp.consume_exchange_mq(
                        queue, True)
                except Exception as e:
                    print("Error en cycle send to dj es->%s" % e)
                    v = 0
                    channels.add(channel)
            await asyncio.sleep(self.step)
            return [engine, v, channels], {}

    def task_cycle(self):
        loop = asyncio.get_event_loop()
        tasks_list = []
        """
        RMQ Task
        """
        rmq_engine = {channel: RMQEngine(**value_dict)
                      for channel, value_dict in self.engine_opts.items()}
        {rmq.active_queue_switch() for rmq in rmq_engine.values()}
        # se crea el conjunto de canales existentes
        channels = set(self.engine_opts.keys())
        # mq 2 ws
        # la args de rmq
        # se activa ciclo de lectura rmq

        cycle_rmq_args = [rmq_engine, 0, channels]
        task = TaskLoop(self.cycle_read_from_rmq,
                        cycle_rmq_args, {},
                        **{"name": "read_from_rabbitmq"})
        task.create()
        if not loop.is_running():
            loop.run_forever()
