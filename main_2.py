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
        self.metrics_dict = {}

    async def metrics_processing(self, data):
        get_data = await data.read(1024)
        try:
            data_ = str(get_data.decode()).split()
            if data_[0] is 'put':
                self.put_metric(data_)
            if data_[0] is 'get':
                self.get_metric(data_)
            if data_[0] is not 'put' or 'get':
                print('error\nwrong command\n\n')
        except TimeoutError:
            print('time\nis out\n\n')

    def put_metric(self, data_got):
        file = open('data.txt', 'a')
        self.metrics_dict[data_got[1]] = data_got[2]
        file.write(f'{data_got[1]} : {self.metrics_dict[data_got[1]]}')
        file.close()
        print('written\n\n')

    def get_metric(self, data_send):
        with open('data.txt', 'r') as file:
            metrics = file.readlines()
        list_ = []
        if data_send[1] != '*':
            for i in metrics:
                if i.split()[0] == data_send[1]:
                    list_.append(i.split()[0])
                    print(i[:-1])
            if len(list_) < 1:
                print('there\nis\nno metric\n\n')
        else:
            for i in metrics:
                if i.split()[0] == data_send[1]:
                    print(i[:-1])


def main():
    run_server("127.0.0.1", 8888)


if __name__ == '__main__':
    main()
