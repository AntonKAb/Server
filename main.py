import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    new_conn = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(new_conn)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Connection error\n\n')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.metrics_list = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.metrics_processing(data.decode())

    def metrics_processing(self, data):
        data_ = data.split()
        if data_[0] == 'put':
            self.transport.write(processing_metrics.put_metric(data).encode())
        elif data_[0] == 'get':
            self.transport.write(processing_metrics.get_metric(data).encode())
        else:
            self.transport.write('error\nwrong command\n\n'.encode())


class MetricsProcessing(ClientServerProtocol):
    def put_metric(self, data):
        data_got = data.split()
        if data_got[1] not in self.metrics_list:
            self.metrics_list[data_got[1]] = [tuple([data_got[2], data_got[3]])]
            # print(self.metrics, 'put_metric')
            return 'ok\n\n'
        else:
            if tuple([data_got[2], data_got[3]]) not in self.metrics_list[data_got[1]]:
                self.metrics_list[data_got[1]].append(tuple([data_got[2], data_got[3]]))
                # print(self.metrics, 'put_metric')
                return 'ok\n\n'
            else:
                # print(self.metrics, 'put_metric')
                return 'ok\n\n'

    def get_metric(self, data):
        data_ = data.split()
        if data_[1] is None or data_[1] is '':
            return 'error\nwrong command\n\n'
        if len(self.metrics_list) == 0:
            return {}
        if data_[1] is '*':
            answer = 'ok\n'
            for key in self.metrics_list:
                for value in self.metrics_list[key]:
                    answer += f'{key} {value[0]} {value[1]}\n'
            return answer + '\n'
        else:
            if data_[1] in self.metrics_list.keys():
                answer = 'ok\n'
                for value in self.metrics_list[data_[1]]:
                    answer += f'{data_[1]} {value[0]} {value[1]}\n'
                return answer + '\n'
            else:
                return 'there is no metric\n\n'


processing_metrics = MetricsProcessing()
run_server('127.0.0.1', 8888)

