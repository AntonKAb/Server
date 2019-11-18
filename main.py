import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.metrics_list = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.metrics_processing(data)

    def metrics_processing(self, data):
        data_ = data.decode().split()
        if data_[0] is 'put':
            self.transport.write(self.put_metric(data_).encode())
        elif data_[0] is 'get':
            self.transport.write(self.get_metric(data_).encode())
        elif data_[0] != 'put' and data_[0] != 'get':
            self.transport.write('error\nwrong command\n\n'.encode())

    def put_metric(self, data_got):
        if data_got[1] not in self.metrics_list.keys():
            self.metrics_list[data_got[1]] = [tuple([data_got[2], data_got[3]])]
            return 'ok\n\n'
        else:
            if self.metrics_list[data_got[1]] == [tuple([data_got[2], data_got[3]])] or \
                    tuple([data_got[2], data_got[3]]) in self.metrics_list[data_got[1]]:
                return 'ok\n\n'
            else:
                self.metrics_list[data_got[1]].append(tuple([data_got[2], data_got[3]]))
                return 'ok\n\n'

    def get_metric(self, data_send):
        if data_send[1] == '':
            return 'error\nwrong command\n\n'
        elif data_send[1] is '*':
            server_answer = 'ok\n'
            for key in self.metrics_list:
                for value in self.metrics_list[key]:
                    server_answer += f'{key} {value[0]} {value[1]}\n'
            return server_answer
        else:
            if data_send[1] in self.metrics_list.keys():
                ser_answer = 'ok\n'
                for value in self.metrics_list[data_send[1]]:
                    ser_answer += f'{data_send[1]} {value[0]} {value[1]}\n'
                return ser_answer
            else:
                return 'there\nis\nno metric\n\n'


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


run_server("127.0.0.1", 8888)
