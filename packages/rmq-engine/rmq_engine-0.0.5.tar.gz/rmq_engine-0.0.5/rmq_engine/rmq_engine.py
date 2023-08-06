from data_amqp import AMQPData


class RMQEngine:
    def __init__(self, *args, **kwargs):
        self.__status = False
        self.__queue_name = kwargs.get('queue_destiny')
        self.amqp = None
        if kwargs.get('amqp', False):
            try:
                self.amqp_opt = kwargs['amqp']
                self.amqp = AMQPData(**kwargs)
                self.__status = True
                self.__queue = kwargs.get(self.__queue_name)
                self.__queue_active = False
            except Exception as e:
                self.__status = False
                raise e

    @property
    def status(self):
        return self.__status

    def active_queue_switch(self):
        self.__queue_active = not self.__queue_active

    def enu_data(self, msg):
        self.amqp.manage_json_data(msg)

    def cycle(self):
        loop, task = self.amqp.create_task(self.__queue, self.__queue_active)
        if not loop.is_running():
            loop.run_forever()

    def connect(self):
        if self.amqp:
            self.amqp.connect()

    async def getdata(self, queue, opt=True):
        return await self.amqp.consume_exchange_mq(queue, opt)
