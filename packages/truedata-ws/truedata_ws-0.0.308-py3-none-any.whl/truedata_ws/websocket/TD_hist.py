from .support import historical_decorator
from websocket import create_connection

from datetime import datetime
import json
from logging import Logger

from colorama import Style, Fore


class HistoricalWebsocket:
    def __init__(self, login_id, password, url, historical_port, broker_token, logger: Logger):
        self.login_id = login_id
        self.password = password
        self.url = url
        self.historical_port = historical_port
        self.broker_token = broker_token
        self.logger = logger
        broker_append = ''
        if self.broker_token is not None:
            broker_append = f'&brokertoken={self.broker_token}'
        try:
            self.hist_socket = create_connection(f"wss://{self.url}:{self.historical_port}?user={self.login_id}&password={self.password}{broker_append}")
            welcome_msg = self.hist_socket.recv()
            welcome_msg = json.loads(welcome_msg)
            if welcome_msg['success']:
                self.logger.info(f"Connected successfully to {welcome_msg['message']}")
            else:
                self.logger.info(f"{Style.BRIGHT}{Fore.RED}Failed to connect with error message = {welcome_msg['message']}{Style.RESET_ALL}")
                self.hist_socket.close()
        except Exception as e:
            self.logger.warning(f"Failed to connect with {type(e)} = {e}")

    def get_n_historic_bars(self, contract, end_time, no_of_bars, bar_size):
        if bar_size.lower() != 'eod' and bar_size.lower() != 'tick':
            bar_size = bar_size.replace(' ', '')
            if bar_size[-1] == 's':
                bar_size = bar_size[:-1]
        try:
            self.logger.debug(f'{{"method": "gethistorylastnbars", "interval": "{bar_size}", "symbol": "{contract}", "nbars": "{no_of_bars}", "to": "{end_time}"}}')
            self.hist_socket.send(f'{{"method": "gethistorylastnbars", "interval": "{bar_size}", "symbol": "{contract}", "nbars": "{no_of_bars}", "to": "{end_time}"}}')
            raw_hist_data = self.hist_socket.recv()
            json_response = json.loads(raw_hist_data)
        except Exception as e:
            addn_err_str = ""
            if type(e) in [ConnectionResetError, ConnectionError, ConnectionAbortedError]:
                self.logger.error(f"Failed sending data with {type(e)} -> {e}")
                addn_err_str = "in send()"
            elif type(e) in [TimeoutError]:
                self.logger.error(f"Failed receiving data with {type(e)} -> {e}")
                addn_err_str = "in recv()"
            json_response = {"success": False, "message": f"({type(e)}) {addn_err_str} -> {e}"}

        if json_response['success']:
            hist_data = json_response['data']
            if bar_size.lower() == 'tick':
                hist_data = self.hist_tick_data_to_dict_list(hist_data, '%Y-%m-%dT%H:%M:%S')
            elif bar_size.lower() == 'eod':
                hist_data = self.hist_bar_data_to_dict_list(hist_data, '%Y-%m-%d')
            else:
                hist_data = self.hist_bar_data_to_dict_list(hist_data, '%Y-%m-%dT%H:%M:%S')
            return hist_data
        else:
            self.logger.error(f'{Style.BRIGHT}{Fore.RED}ERROR: Your request failed with error "{json_response["message"]}"{Style.RESET_ALL}')
            return []

    @historical_decorator
    def get_historic_data(self, contract, end_time, start_time, bar_size, options=None):
        try:
            self.hist_socket.send(f'{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{end_time}"}}')
        # def dive_for_data(hd_socket):
        #     dive_raw_data = hd_socket.recv()
        #     try:
        #         dive_response = json.loads(dive_raw_data)
        #     except json.decoder.JSONDecodeError:
        #         self.logger.error(f'{Style.BRIGHT}{Fore.RED}Caught a JSONDecodeError for the following request - {Style.RESET_ALL}')
        #         self.logger.error(f'{Style.BRIGHT}{Fore.RED}{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{end_time}"}}{Style.RESET_ALL}')
        #         self.logger.error(f'{dive_raw_data}')
        #         return []
        #     if dive_response['success']:
        #         try:
        #             if dive_response['message'] == 'HeartBeat':
        #                 return dive_for_data(hd_socket)
        #         except KeyError:
        #             return dive_response['data']
        #     else:
        #         self.logger.error(f'{Style.BRIGHT}{Fore.RED}ERROR: Your request failed with error "{dive_response["message"]}"{Style.RESET_ALL}')
        #         return []
        #
        # hist_data = dive_for_data(self.hist_socket)
        # ==== NEW ====
            dive_raw_data = self.hist_socket.recv()
            json_response = json.loads(dive_raw_data)
        except json.decoder.JSONDecodeError:
            self.logger.error(f'{Style.BRIGHT}{Fore.RED}Caught a JSONDecodeError for the following request - {Style.RESET_ALL}')
            self.logger.error(f'{Style.BRIGHT}{Fore.RED}{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{end_time}"}}{Style.RESET_ALL}')
            # noinspection PyUnboundLocalVariable
            self.logger.error(f'{dive_raw_data}')
            return []
        except Exception as e:
            addn_err_str = ""
            if type(e) in [ConnectionResetError, ConnectionError, ConnectionAbortedError]:
                self.logger.error(f"Failed sending data with {type(e)} -> {e}")
                addn_err_str = "in send()"
            elif type(e) in [TimeoutError]:
                self.logger.error(f"Failed receiving data with {type(e)} -> {e}")
                addn_err_str = "in recv()"
            json_response = {"success": False, "message": f"({type(e)}) {addn_err_str} -> {e}"}
        if json_response['success']:
            return options['processor_to_call'](json_response['data'], time_format=options['time_format'])
        else:
            self.logger.error(f'{Style.BRIGHT}{Fore.RED}Your request failed with error "{json_response["message"]}"{Style.RESET_ALL}')
            return []
        # ==== END NEW ====
        # hist_data = options['processor_to_call'](hist_data, time_format=options['time_format'])
        # return hist_data

    @staticmethod
    def hist_tick_data_to_dict_list(hist_data, time_format):
        data_list = []
        count = 0
        for j in hist_data:
            try:
                data_list.append({'time': datetime.strptime(j[0], time_format),
                                  'ltp': float(j[1]),
                                  'volume': int(j[2]),
                                  'oi': int(j[3]),
                                  'bid': float(j[4]),
                                  'bid_qty': int(j[5]),
                                  'ask': float(j[6]),
                                  'ask_qty': int(j[7])})
            except IndexError:  # No bid-ask data
                data_list.append({'time': datetime.strptime(j[0], time_format),
                                  'ltp': float(j[1]),
                                  'volume': int(j[2]),
                                  'oi': int(j[3])})
                continue
            count = count + 1
        return data_list

    @staticmethod
    def hist_bar_data_to_dict_list(hist_data, time_format):
        data_list = []

        for j in hist_data:
            data_list.append({'time': datetime.strptime(j[0], time_format),
                              'o': float(j[1]),
                              'h': float(j[2]),
                              'l': float(j[3]),
                              'c': float(j[4]),
                              'v': int(j[5]),
                              'oi': int(j[6])})
        return data_list
