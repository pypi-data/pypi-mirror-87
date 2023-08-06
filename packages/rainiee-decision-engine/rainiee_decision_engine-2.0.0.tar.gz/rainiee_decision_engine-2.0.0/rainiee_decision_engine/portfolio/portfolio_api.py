import json

from rainiee_decision_engine.base import data_pro


def algorithm_solve_vanilla_mvo(symbol_list, start_index, end_index):
    return data_pro.get_rainiee_client().algorithm_solve_vanilla_mvo(method_type='POST', req_param={
        'symbol_list': symbol_list,
        'start_index': start_index,
        'end_index': end_index
    })


def algorithm_solve_maximize_sharpe(symbol_list, start_index, end_index):
    return data_pro.get_rainiee_client().algorithm_solve_maximize_sharpe(method_type='POST', req_param={
        'symbol_list': symbol_list,
        'start_index': start_index,
        'end_index': end_index
    })


def algorithm_solve_vanilla_mvo_realtime(symbol_list, start_index, end_index):
    return data_pro.get_rainiee_client().algorithm_solve_vanilla_mvo_realtime(method_type='POST', req_param={
        'symbol_list': symbol_list,
        'start_index': start_index,
        'end_index': end_index
    })


def monitoring_baseline(portf, hold_index, hold_period):
    return data_pro.get_rainiee_client().monitoring_baseline(method_type='POST', req_param={
        'portf': json.dumps(portf),
        'hold_index': hold_index,
        'hold_period': hold_period
    })
