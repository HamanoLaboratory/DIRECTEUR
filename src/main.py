#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from optimization import SimulatedAnnealing, State
from utils import ProfileBase as PF
from utils import *
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Create hiHep Compound File')

parser.add_argument("-i","--iteration", default = 100, type=int)
parser.add_argument("-t","--time", default = 60, type=int)
parser.add_argument('-n','--num', default=5, type=int, help='LimitNum')
parser.add_argument('-e','--evalnum', default=2, type=int, help='EvalNum')
parser.add_argument("-optD","--optimize_data", type=str)
parser.add_argument("-tarD","--target_data", type=str)
parser.add_argument('-out', '--output', default=None, type=str, help='output file name')

args = parser.parse_args()

    
target_data_path = args.target_data
targets = pd.read_csv(target_data_path , sep= '\t')

target_data = list(targets['value'])

optimize_data_path = args.optimize_data
optimize_data = get_data(optimize_data_path)



if __name__ == '__main__':
    params = {
    'MaxIteration' : args.iteration,
    'MaxTime': args.time,
    'LimitNum': args.num,
    'EvalNum': args.evalnum,
    'TargetCombination': [], #target keys
    'Targets': target_data, #gene profile
    }

print(f'INPUT optimize data: {optimize_data_path}')
print(f'INPUT target data: {target_data_path}')


state = State()

#set original evaluation function
SimulatedAnnealing.get_targets = PF.get_integrated_list
SimulatedAnnealing.calc_eval_func = PF.calc_eval_func
SimulatedAnnealing.eval_func1 = PF.eval_func1
SimulatedAnnealing.eval_func2 = PF.eval_func2
    
SA = SimulatedAnnealing(state, params, optimize_data, target_data)
   
try:
        SA.optimization()
        SA.save_info(args.output)
except KeyboardInterrupt:
        SA.save_info(args.output)
