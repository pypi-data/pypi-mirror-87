import logging
import inspect
from socket import socket, AF_INET, SOCK_DGRAM, gethostname
from datetime import datetime
from .mongodb_connector import ConnectMongo
from sys import argv


def configure_logs():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s ', level=logging.INFO)


def get_module_name():
    """This function gets module and file name that called it. Must be called on instantiate the LogThis class."""
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return mod.__name__, argv[0]


class LogThis:

    def __init__(self, module):
        self.hostname = LogThis.get_hostname()
        self.ip = LogThis.get_host_ip()
        self.module = module[0]
        self.app = module[1]
        self.default_fields = {
            'Ip': self.ip,
            'HostName': self.hostname,
            'ModuleCalled': self.module,
            'App': self.app
        }

    def info(self, msg, payload=None, result=None):
        logging.info(f'Message:{msg}, Module:{self.module}, App:{self.app}, Payload:{payload}, Result:{result}')
        msg_info = {
            'Date': datetime.now(),
            'Severity': 'INFO',
            'MsgInfo': msg,
            'Payload': payload,
            'Result': result,
        }
        msg_info.update(self.default_fields)
        try:
            mongodb_connection = ConnectMongo()
            mongodb_connection.info_collection.insert_one(msg_info)
        except Exception as e:
            msg_info['Severity'] = 'ERROR'
            logging.error(f'Fail to send log for MongoDb - {e}, Message:{msg_info}')

    def error(self, msg):
        logging.error(f'Message:{msg}, Module:{self.module}, App:{self.app}')
        msg_error = {
            'Date': datetime.now(),
            'Severity': 'ERROR',
            'HostName': self.hostname,
            'MsgError': msg,
        }
        msg_error.update(self.default_fields)
        try:
            mongodb_connection = ConnectMongo()
            mongodb_connection.error_collection.insert_one(msg_error)
        except Exception as e:
            logging.error(f'Fail to send log for MongoDb - {e}, Message:{msg_error}')

    @staticmethod
    def get_hostname():
        try:
            host_name = gethostname()
        except:
            logging.error('Fail to get Hostname')
            host_name = 'N/A'
        return host_name

    @staticmethod
    def get_host_ip():
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            host_ip = s.getsockname()[0]
            s.close()
        except:
            logging.error('Fail to get get Ip')
            host_ip = 'N/A'
        return host_ip

