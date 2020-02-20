from numpy.random import exponential, normal, triangular, uniform, beta, \
    weibull, chisquare, gamma, lognormal, pareto, standard_t
from random import randrange

def get_dist_num(args):
    dist = args[0]
    
    for i in range(len(args[1:])):
        args[i+1] = float(args[1:][i])

    if dist == 'EXP':
        return exponential(args[1])
    elif dist == 'NOR':
        return normal(loc=args[1], scale=args[2]) # loc = média , scale = desvio
    elif dist == 'TRI':
        return triangular(args[1], args[2], args[3])
    elif dist == 'UNI':
        return uniform(low=args[1], high=args[2])
    elif dist == 'BET':
        return beta(args[1], args[2])
    elif dist == 'WEI':
        return weibull(args[1])
    elif dist == 'CAU': # CAU: Cauchy
        return 0
    elif dist == 'CHI':
        return chisquare(args[1])
    elif dist == 'ERL': # ERL: Erlang
        return 0
    elif dist == 'GAM':
        return gamma(args[1], scale=args[2])
    elif dist == 'LOG':
        return lognormal(mean=args[1], sigma=args[2])
    elif dist == 'PAR':
        return pareto(args[1])
    elif dist == 'STU':
        return standard_t(args[1])

def get_priority(args):
    list = []
    for i in range(len(args)):
        if i != 0:
            list.append(int(args[i]) + list[-1])
        else:
            list.append(int(args[i]))
            
    p = randrange(0,100)+1
    for i in range(len(list)):
        if p <= list[i]:
            return 5-i

def get_exam_medicine(probability) -> bool:
    em = randrange(0,100)+1
    if em <= float(probability[0]):
        return True
    else:
        return False