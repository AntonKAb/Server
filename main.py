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
        self.metrcics_list = {}

    def connection_made(self, sending):
        self.sending = sending

    def data_received(self, data):
        self.metrics_processing(data)

    def metrics_processing(self, data):
        try:
            data_ = str(data.decode()).split()
            if data_[0] is 'put':
                self.sending.write(self.put_metric(data_).encode())
            if data_[0] is 'get':
                self.sending.write(self.get_metric(data_).encode())
            if data_[0] is not 'put' or 'get':
                self.sending.write('error\nwrong command\n\n')
        except TimeoutError:
            return 'time\nis out\n\n'

    def put_metric(self, data_got):
        if data_got[1] not in self.metrcics_list.keys():
            self.metrcics_list[data_got[1]] = [data_got[2]]
            return 'written\n\n'
        else:
            if self.metrcics_list[data_got[1]] == [tuple([data_got[2], data_got[3]])] or \
                    tuple([data_got[2], data_got[3]]) in self.metrcics_list[data_got[1]]:
                return 'already written\n\n'
            else:
                self.metrcics_list[data_got[1]].append(tuple([data_got[2], data_got[3]]))
                return 'written\n\n'

    def get_metric(self, data_send):
        pass


def main():
    run_server("127.0.0.1", 8888)


if __name__ == '__main__':
    main()
