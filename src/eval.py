"""
Created on Sat Nov  2 01:13:59 2013

@author: sanmayaj
"""

from sympy import *
from sympy.plotting import plot
from sympy.mpmath import splot
from sympy.parsing.sympy_parser import parse_expr
from func import *
import numpy as np

init_printing(use_latex = True)
'''
x, a = symbols('x a')

#f = Integral(x, x)
#print f.evalf(subs = {x:2})
f = x**2 + a
#print f
#my_symbols = []
my_vars = sorted(f.free_symbols)
#evaluated = f.subs(*zip(my_vars, [2,7]))

vals=[2,7]
d = {}
for i in range(len(vals)):
    d[my_vars[i]] = vals[i]
evaluated = f.evalf(subs = d)
print evaluated
fun = lambdify(tuple(my_vars), f)

print wrapper(fun, vals)

splot(fun, [0,2], [0,7])
#p.show()'''


fil = open('../data/inp3.txt', 'r')
lin = fil.readline()
payoff_list = []
player_count = 0

while lin != "":
    player_count += 1
    payoff_list.append(parse_expr(lin))
    lin = fil.readline()
fil.close()

used_symbols = get_symbols(payoff_list)
strat_vars = extract_strategy_vars(used_symbols, player_count)

player_strat_payoff_dict = {}
for pl in range(1, player_count + 1):
    player_strat_payoff_dict[pl] = (payoff_list[pl-1], strat_vars[pl-1])

der_list = deriv_list(player_strat_payoff_dict)
dbl_der_list = deriv_list(player_strat_payoff_dict, 2)

ans = solve(tuple(der_list), *strat_vars)

other_vars = subtract_lists(used_symbols, strat_vars)

vals = []
for e in other_vars:
    print "Supply value for independent variable", e
    s = raw_input()
    vals.append(float(s))

sym_val_dict = {}
for i in range(len(vals)):
    sym_val_dict[other_vars[i]] = vals[i]

for my_var in strat_vars:
    ex = ans[my_var]
    sol = ex.evalf(subs = sym_val_dict)
    sym_val_dict[my_var] = sol

evaluated_player_payoff_dict = {}

for plr_no, (ex, my_var) in player_strat_payoff_dict.iteritems():
    evaluated_player_payoff_dict[plr_no] = ex.evalf(subs = sym_val_dict)

graphs_list = []
p = None
color = 0
cycle_color_list = ['blue', 'red', 'green', 'orange', 'black']
for ex in ans.itervalues():
    #t = tuple([ex, tuple([other_vars[0], 0, sym_val_dict[other_vars[0]]])])
    subs_d = get_subs_dict_for_all_but(sym_val_dict, other_vars[0])
    ex_subs = ex.subs(subs_d)
    print ex_subs
    t = [ex_subs, tuple([other_vars[0], 0, sym_val_dict[other_vars[0]]])]
    if p:
        temp = plot(*t, line_color = cycle_color_list[color], show = False)
        p.extend(temp)
    else:
        p = plot(*t, show = False)
    #graphs_list.append(t)
    color += 1
    color %= 5

#p = plot(*graphs_list)
p.xlabel = str(other_vars[0])
p.ylabel = "strat"
p.show()

print sym_val_dict
print evaluated_player_payoff_dict

p = None

for i in range(len(der_list)):
    ex = der_list[i]
    my_ex = solve(ex, strat_vars[i])[0]
    subs_d = get_subs_dict_for_all_but(sym_val_dict, [strat_vars[i], strat_vars[(i+1)%player_count]])
    my_ex = my_ex.subs(subs_d)
    p = plot(my_ex, tuple([strat_vars[(i+1)%player_count], 0, 3*sym_val_dict[strat_vars[(i+1)%player_count]]]), show = False)
    p.xlabel = str(strat_vars[(i+1)%player_count])
    p.ylabel = str(strat_vars[i])
    p.title = "Variation of " + str(strat_vars[i]) + " with " + str(strat_vars[(i+1)%player_count])
    p.show()

