import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.metrcics_list = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.metrics_processing(data)

    def metrics_processing(self, data):
        try:
            data_ = str(data.decode()).split()
            if data_[0] is 'put':
                self.transport.write(self.put_metric(data_).encode())
            if data_[0] is 'get':
                self.transport.write(self.get_metric(data_).encode())
            if data_[0] is not 'put' or 'get':
                self.transport.write('error\nwrong command\n\n'.encode())
        except TimeoutError:
            self.transport.write('time\nis out\n\n'.encode())

    def put_metric(self, data_got):
        if data_got[1] not in self.metrcics_list.keys():
            self.metrcics_list[data_got[1]] = [tuple([data_got[2], data_got[3]])]
            return 'written\n\n'
        else:
            if self.metrcics_list[data_got[1]] == [tuple([data_got[2], data_got[3]])] or \
                    tuple([data_got[2], data_got[3]]) in self.metrcics_list[data_got[1]]:
                return 'already written\n\n'
            else:
                self.metrcics_list[data_got[1]].append(tuple([data_got[2], data_got[3]]))
                return 'written\n\n'

    def get_metric(self, data_send):
        if data_send[1] == '':
            return 'error\nwrong command\n\n'
        if data_send[1] is '*':
            server_answer = 'ok\n'
            for key in self.metrcics_list:
                for value in self.metrcics_list[key]:
                    server_answer += f'{key} {value[0]} {value[1]}\n'
            return server_answer
        else:
            if data_send[1] in self.metrcics_list.keys():
                ser_answer = 'ok\n'
                for value in self.metrcics_list[data_send[1]]:
                    ser_answer += f'{value[0]} {value[1]}\n'
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
