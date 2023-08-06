import json
import time
import pika
import uuid
import gzip

name = "RPCmq"


class RPCmqEncoder(json.JSONEncoder):
    def default(self, obj):
        return super(RPCmqEncoder, self).default(obj)


class RPCmqServer:

    def __init__(self, **args):
        self.credit = pika.PlainCredentials(args["username"], args["password"])
        self.params = pika.ConnectionParameters(args["host"], args["port"], '/', self.credit)
        self.prefix = args["prefix"]
        self.uuid = args.get("uuid")
        self.funcs = {}
        self.debug = args.get("debug", False)
        self.send_channel = None
        self.send_opts = args.get("send_opts", {})
        self.send_try_count = args.get("send_try_count", 3)
        self.json_cls = args.get("json_cls", RPCmqEncoder)
        self.connections = []
        if not self.uuid:
            self.uuid = uuid.uuid4()
        # self.executor = ThreadPoolExecutor(thread_num)

    def channel(self):
        connection = pika.BlockingConnection(self.params)
        self.connections.append(connection)
        return connection.channel()

    def message_callback(self, channel, method, properties, body):
        # self.executor.submit(self.callback, channel, method, properties, body)
        try:
            self.callback(channel, method, properties, body)
        except Exception as ex:
            print("except:", self.uuid, ex)
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def callback(self, channel, method, properties, recv_body):
        recv_gzip = False
        if bytes([recv_body[0]]) == b'\x8e':
            recv_body = gzip.decompress(recv_body[1:])
            recv_gzip = True
        body = str(recv_body, encoding="utf-8")
        if self.debug:
            print("server recv:", channel.queue, body)
        obj = json.loads(body)
        start_clock = time.clock()
        result = {}
        if channel.queue in self.funcs:
            cls = self.funcs[channel.queue]
            if hasattr(cls, obj["method"]):
                try:
                    func = getattr(cls, obj["method"])
                    result = func(**obj["args"])
                except Exception as ex:
                    result['code'] = -1002
                    result['msg'] = str(ex)
                    # print("Call except %s" % ex)
            else:
                result['code'] = -1003
                result['msg'] = '方法名称错误'
            if hasattr(cls, 'version'):
                result['version'] = getattr(cls, 'version')
        else:
            result['code'] = -1001
            result['msg'] = "method not found"

        if not isinstance(result, dict):
            result = {
                "data": result
            }
        if "code" not in result:
            result['code'] = 0
        if "msg" not in result:
            result['msg'] = 'ok'
        result['id'] = obj['id']
        result['elapsed'] = int((time.clock() - start_clock) * 1000)
        if obj["ret"]:
            self.send(obj["rel"], result, recv_gzip)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def send(self, queue, data, send_gzip=False):
        send_body = json.dumps(data, cls=self.json_cls)
        if self.debug:
            print("server send:", queue, send_body)
        if send_gzip:
            send_body = bytes(send_body, encoding='utf8')
            send_body = gzip.compress(send_body)
            send_body = b'\x8e' + send_body
        error = None
        for try_num in range(self.send_try_count):
            try:
                if not self.send_channel or not self.send_channel.is_open:
                    self.send_channel = self.channel()
                self.send_channel.queue_declare(queue=queue, **self.send_opts)
                self.send_channel.basic_publish(exchange='', routing_key=queue, body=send_body)
                error = None
                break
            except Exception as ex:
                self.send_channel = None
                error = ex
        if error:
            raise error

    def start(self, **kwargs):
        import _thread
        import time

        def start_thread(cls, queue):
            full_queue = cls.prefix + queue
            channel = cls.channel()
            print("server start for queue:", queue)
            setattr(channel, 'queue', queue)
            channel.queue_declare(queue=full_queue)
            channel.basic_consume(full_queue, on_message_callback=cls.message_callback, auto_ack=False)
            channel.start_consuming()

        for k, v in self.funcs.items():
            _thread.start_new_thread(start_thread, (self, k))

        while True:
            time.sleep(1)

    def stop(self):
        try:
            for connection in self.connections:
                if connection.is_open:
                    connection.close()
        except Exception as ex:
            print("close connection except %s" % ex)

    def bind(self, **kwargs):
        def init(cls):
            if cls.__init__:
                cls.__init__(cls)
            queue = kwargs.get("queue")
            self.funcs[queue] = cls()
            return cls

        return init


class RPCmqClient:

    def __init__(self, **args):
        import _thread

        credit = pika.PlainCredentials(args["username"], args["password"])
        self.params = pika.ConnectionParameters(args["host"], args["port"], '/', credit)
        self.prefix = args.get("prefix")
        self.debug = args.get("debug", False)
        self.gzip = args.get("gzip", True)
        self.recv_queue = args.get("queue")
        self.recv_buffer = {}
        self.send_channel = None
        self.send_connect = pika.BlockingConnection(self.params)
        self.send_opts = args.get("send_opts", {})
        self.send_try_count = args.get("send_try_count", 3)
        self.json_cls = args.get("json_cls", RPCmqEncoder)
        self.connections = []

        def start_thread(cls, queue):
            recv_queue = cls.prefix + cls.recv_queue
            channel = cls.channel()
            print("client start for queue:", queue)
            setattr(channel, 'queue', queue)
            channel.queue_declare(queue=recv_queue)
            channel.basic_consume(recv_queue, on_message_callback=cls.message_callback, auto_ack=False)
            channel.start_consuming()

        _thread.start_new_thread(start_thread, (self, args["queue"]))

    def channel(self):
        connection = pika.BlockingConnection(self.params)
        self.connections.append(connection)
        return connection.channel()

    def call(self, send_queue, method, args, timeout=60000, ret=True):
        send_queue = self.prefix + send_queue
        recv_queue = self.prefix + self.recv_queue
        body = {
            'id': str(uuid.uuid4()),
            'method': method,
            'args': args,
            'rel': recv_queue,
            'ret': ret
        }
        send_body = json.dumps(body, cls=self.json_cls)
        if self.debug:
            print("client send:", send_queue, send_body)
        if self.gzip:
            send_body = bytes(send_body, encoding='utf8')
            send_body = gzip.compress(send_body)
            send_body = b'\x8e' + send_body
        error = None
        for try_num in range(self.send_try_count):
            try:
                if not self.send_channel or not self.send_channel.is_open:
                    self.send_channel = self.channel()
                self.send_channel.queue_declare(queue=send_queue, **self.send_opts)
                self.send_channel.basic_publish(exchange='', routing_key=send_queue, body=send_body)
                error = None
                break
            except Exception as ex:
                self.send_channel = None
                error = ex
        if error:
            raise error
        start_clock = time.clock()
        while True:
            if body['id'] in self.recv_buffer:
                buff = self.recv_buffer[body['id']]
                del self.recv_buffer[body['id']]
                return buff
            if start_clock - time.clock() > timeout:
                return {
                    'code': -1004,
                    'msg': '请求超时'
                }
            time.sleep(0.01)

    def message_callback(self, channel, method, properties, recv_body):
        if bytes([recv_body[0]]) == b'\x8e':
            recv_body = gzip.decompress(recv_body[1:])
        body = json.loads(recv_body)
        if self.debug:
            print("client recv:", channel.queue, body)
        if not body['id']:
            return
        self.recv_buffer[body['id']] = body
        channel.basic_ack(delivery_tag=method.delivery_tag)
