from .support import TickLiveData, MinLiveData, TouchlineData
from .support import TDLiveDataError, TDHistoricDataError
from .TD_live import LiveClient
from .TD_hist import HistoricalWebsocket
from threading import Thread
from typing import Union
from collections import defaultdict

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import json

from colorama import Style, Fore
import logging


class TD:
    def __init__(self, login_id, password, broker_token=None, url='push.truedata.in', live_port=8082, historical_port=8092, logger_propagate=False, tz='Asia/Kolkata', logger_level=20, logger=None):
        self.live_websocket = None
        self.historical_websocket = None
        self.login_id = login_id
        self.password = password
        self.url = url
        self.live_port = live_port
        self.historical_port = historical_port
        if logger is None:
            self.logger = logging.getLogger('truedata_ws')
            self.logger.propagate = logger_propagate
            self.logger.setLevel(logger_level)
        else:
            self.logger = logger
        if live_port is None:
            self.connect_live = False
        else:
            self.connect_live = True
        if historical_port is None:
            self.connect_historical = False
        else:
            self.connect_historical = True
        self.broker_token = broker_token
        self.hist_data = {}
        self.live_data = {}
        self.symbol_mkt_id_map = defaultdict(set)
        self.streaming_symbols = {}
        self.touchline_data = {}
        self.default_market_data_id = 2000
        self.default_historical_data_id = 1000
        self.connect()

    def connect(self):
        broker_append = ''
        if self.broker_token is not None:
            broker_append = f'&brokertoken={self.broker_token}'
        if self.connect_live:
            self.live_websocket = LiveClient(self, f"wss://{self.url}:{self.live_port}?user={self.login_id}&password={self.password}{broker_append}")
            t = Thread(target=self.connect_thread, args=(), daemon=True)
            t.start()
        if self.connect_historical:
            self.historical_websocket = HistoricalWebsocket(self.login_id, self.password, self.url, self.historical_port, self.broker_token, self.logger)
        while self.connect_live and self.live_websocket.subscription_type == '':
            time.sleep(1)

    def connect_thread(self):
        self.live_websocket.run_forever(ping_interval=10, ping_timeout=5)
        self.logger.debug('Goodbye (properly) !!')

    def disconnect(self):
        self.live_websocket.disconnect_flag = True
        self.live_websocket.close()
        self.logger.info(f"{Fore.GREEN}Disconnected LIVE TrueData...{Style.RESET_ALL}")
        if self.connect_historical:
            self.historical_websocket.hist_socket.close()
            self.logger.info(f"{Fore.GREEN}Disconnected HISTORICAL TrueData...{Style.RESET_ALL}")

    @staticmethod
    def truedata_duration_map(regular_format, end_date):
        duration_units = regular_format.split()[1].upper()
        if len(duration_units) > 1:
            raise TDHistoricDataError("Misconfigured duration argument")
        duration_size = int(regular_format.split()[0])
        if duration_units == 'D':
            return (end_date - relativedelta(days=duration_size - 1)).date()
        elif duration_units == 'W':
            return (end_date - relativedelta(weeks=duration_size)).date()
        elif duration_units == 'M':
            return (end_date - relativedelta(months=duration_size)).date()
        elif duration_units == 'Y':
            return (end_date - relativedelta(years=duration_size)).date()

    def get_historic_data(self, contract,
                          ticker_id=None,
                          end_time=None,
                          duration=None,
                          start_time=None,
                          bar_size="1 min"):
        if start_time is not None and duration is None:
            return self.get_historical_data_from_start_time(contract=contract,
                                                            ticker_id=ticker_id,
                                                            end_time=end_time,
                                                            start_time=start_time,
                                                            bar_size=bar_size)
        else:
            return self.get_historical_data_from_duration(contract=contract,
                                                          ticker_id=ticker_id,
                                                          end_time=end_time,
                                                          duration=duration,
                                                          bar_size=bar_size)

    def get_n_historical_bars(self, contract,
                              ticker_id=None,
                              end_time: datetime = None,
                              no_of_bars: int = 1,
                              bar_size="1 min"):
        if end_time is None:
            end_time = datetime.today()
        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S')
        hist_data = self.historical_websocket.get_n_historic_bars(contract, end_time, no_of_bars, bar_size)
        if ticker_id is None:
            ticker_id = self.default_historical_data_id
            self.default_historical_data_id = self.default_historical_data_id + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    def get_historical_data_from_duration(self, contract,
                                          ticker_id=None,
                                          end_time: datetime = None,
                                          duration=None,
                                          bar_size="1 min"):
        if duration is None:
            duration = "1 D"
        if end_time is None:
            end_time = datetime.today()
        start_time = self.truedata_duration_map(duration, end_time)
        end_time = end_time.strftime('%Y-%m-%d') + 'T23:59:59'
        start_time = start_time.strftime('%Y-%m-%d') + 'T00:00:00'

        hist_data = self.historical_websocket.get_historic_data(contract, end_time, start_time, bar_size)
        if ticker_id is None:
            ticker_id = self.default_historical_data_id
            self.default_historical_data_id = self.default_historical_data_id + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    def get_historical_data_from_start_time(self, contract,
                                            ticker_id=None,
                                            end_time: datetime = None,
                                            start_time: datetime = None,
                                            bar_size="1 min"):
        if end_time is None:
            end_time = datetime.today().replace(hour=11, minute=59, second=59)
        if start_time is None:
            start_time = datetime.today().replace(hour=0, minute=0, second=0)

        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S')
        start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        hist_data = self.historical_websocket.get_historic_data(contract, end_time, start_time, bar_size)
        if ticker_id is None:
            ticker_id = self.default_historical_data_id
            self.default_historical_data_id = self.default_historical_data_id + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    @staticmethod
    def get_req_id_list(req_id: Union[int, list], len_contracts: int) -> list:
        if type(req_id) == list:
            if len(req_id) == len_contracts:
                return req_id
            else:
                raise TDLiveDataError("Lengths do not match...")
        elif type(req_id) == int:
            curr_req_id = req_id
            return [curr_req_id + i for i in range(0, len_contracts)]
        else:
            raise TDLiveDataError("Invalid req_id datatype...")

    def start_live_data(self, resolved_contracts, req_id=None):  # TODO: Prevent reuse of req_ids
        if req_id is not None:
            req_ids = self.get_req_id_list(req_id, len(resolved_contracts))
        else:
            req_ids = self.get_req_id_list(self.default_market_data_id, len(resolved_contracts))
            self.default_market_data_id = self.default_market_data_id + len(resolved_contracts)
        for j in range(0, len(req_ids)):
            resolved_contract = resolved_contracts[j].upper()
            self.touchline_data[req_ids[j]] = TouchlineData()
            if self.live_websocket.subscription_type == 'tick':
                self.live_data[req_ids[j]] = TickLiveData(resolved_contract)
            elif '+' in self.live_websocket.subscription_type:
                self.live_data[req_ids[j]] = TickLiveData(resolved_contract)
                self.live_data[req_ids[j]] = MinLiveData(resolved_contract)
            elif 'min' in self.live_websocket.subscription_type:
                self.live_data[req_ids[j]] = MinLiveData(resolved_contract)
            self.symbol_mkt_id_map[resolved_contract].update({req_ids[j]})
        self.live_websocket.send(f'{{"method": "addsymbol", "symbols": {json.dumps(resolved_contracts)}}}')
        return req_ids

    def stop_live_data(self, contracts):
        self.live_websocket.send(f'{{"method": "removesymbol", "symbols": {json.dumps(contracts)}}}')

    # def get_touchline(self):
    #     self.live_websocket.send(f'{{"method": "touchline"}}')
