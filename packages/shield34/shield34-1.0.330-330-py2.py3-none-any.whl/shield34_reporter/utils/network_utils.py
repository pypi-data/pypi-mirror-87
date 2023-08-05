from contextlib import closing
from random import randint


class NetworkUtils():

    @staticmethod
    def is_port_in_use(hostname,port):
        import socket

        false_results = 0
        for i in range(0,2):
            try:
                socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_.settimeout(1)
                socket_.connect((hostname, port))
            except socket.error:
                false_results = false_results + 1
            finally:
                socket_.close()

        if false_results >=2:
            return False
        else:
            return True

    @staticmethod
    def get_random_port(hostname):
        while True:

            port_num = randint(20000, 20200)
            if not NetworkUtils.is_port_in_use(hostname,port_num):
                break
        return port_num