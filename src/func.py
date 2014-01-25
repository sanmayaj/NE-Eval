# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 18:12:49 2013

@author: sanmayaj
"""

from sympy import diff, Symbol

def wrapper(func, args):
    return func(*args)


def get_symbols(expr_list = []):
    list_sym = []
    if len(expr_list) == 0:
        return None
    else:
        for expr in expr_list:
            temp = sorted(expr.free_symbols)
            for sym in temp:
                if list_sym.__contains__(sym):
                    continue
                else:
                    list_sym.append(sym)
        return list_sym


def extract_strategy_vars(used_sym, plyr_cnt):
    var_list_dict = {}
    pref_count_dict = {}
    n = 1
    strat_pref = ''
    for sy in used_sym:
        sy_str = str(sy)
        if sy_str.isalpha():
            continue
        elif (sy_str.endswith(str(n)) or sy_str.endswith('1')):
            pref = sy_str[:len(sy_str) - 1]
            if var_list_dict.__contains__(pref):
                var_list_dict[pref].append(sy)
                pref_count_dict[pref] += 1
                n += 1
            else:
                var_list_dict[pref] = [sy]
                pref_count_dict[pref] = 1
                n = 2
        else:
            continue
    for k, v in pref_count_dict.iteritems():
        if v == plyr_cnt:
            strat_pref = pref
    return var_list_dict[strat_pref]


def deriv_list(l = {}, n = 1):
    d = []
    for x in l.itervalues():
        x = x + (n,)
        d.append(diff(*x))
    return d
    
def subtract_lists(li1, li2):
    ans = []
    if li1.__len__() > 0:
        for element in li1:
            if not li2.__contains__(element):
                ans.append(element)
            else:
                continue
    return ans

def get_subs_dict_for_all_but(di, *args):
    ans_dict = {}
    #print "args", args, type(*args)
    if type(*args) == type(list()):
        for key in di.iterkeys():
            if key in args[0]:
                continue
            else:
                ans_dict[key] = di[key]
    elif type(*args) == type(Symbol('x')):
        for key in di.iterkeys():
            if str(key) == str(*args):
                continue
            else:
                ans_dict[key] = di[key]
    #print ans_dict
    return ans_dict
