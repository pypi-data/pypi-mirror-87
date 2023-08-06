import json
import rainiee_decision_engine.base.data_pro as data_pro

class DecisionEngineClient(object):

    def __init__(self,username, password):
        data_pro.init_token(username,password)

    def data_pro(self):
        return data_pro

    def get_token(self):
        return data_pro.get_token()


    @staticmethod
    def trade_execute_order(symbol, index, order_type, price):
        return data_pro.get_rainiee_client().trade_execute_order(method_type='GET', req_param={
            'symbol': symbol,
            'index': index,
            'order_type': order_type,
            'price': price
        })

    @staticmethod
    def algorithm_solve_vanilla_mvo(symbol_list, start_index, end_index):
        return data_pro.get_rainiee_client().algorithm_solve_vanilla_mvo(method_type='POST', req_param={
            'symbol_list': symbol_list,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def algorithm_solve_maximize_sharpe(symbol_list, start_index, end_index):
        return data_pro.get_rainiee_client().algorithm_solve_maximize_sharpe(method_type='POST', req_param={
            'symbol_list': symbol_list,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def algorithm_solve_vanilla_mvo_realtime(symbol_list, start_index, end_index):
        return data_pro.get_rainiee_client().algorithm_solve_vanilla_mvo_realtime(method_type='POST', req_param={
            'symbol_list': symbol_list,
            'start_index': start_index,
            'end_index': end_index
        })

    @staticmethod
    def monitoring_baseline(portf, hold_index, hold_period):
        return data_pro.get_rainiee_client().monitoring_baseline(method_type='POST', req_param={
            'portf': json.dumps(portf),
            'hold_index': hold_index,
            'hold_period': hold_period
        })

    @staticmethod
    def cn_stockstats_returns_matrix(symbol_list, start_index, end_index):
        return data_pro.get_rainiee_client().cn_stockstats_returns_matrix(method_type='POST', req_param={
            'symbol_list': symbol_list,
            'start_index': start_index,
            'end_index': end_index
        })