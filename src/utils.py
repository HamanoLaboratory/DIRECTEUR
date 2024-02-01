import json
import math
from re import T
from scipy.stats import pearsonr
import numpy as np


def get_data(path):
    with open(path, 'rb') as f:
        data = json.load(f)
    return data

def addition_list(in1, in2):
    add = np.array(in1) + np.array(in2)
    return add.tolist()


class ProfileBase():
    def get_integrated_list(self, values):
        for i, v in enumerate(values):
            if i == 0:
                integrated_list = v                
            else:                    
               integrated_list = addition_list(integrated_list, v)
   
        return integrated_list     

    def calc_eval_func(self):
        self.state.integrated_profile = self.get_targets(self.state.values)
        self.state.obj = 0
        for i in range(self.EvalNum):
            f = eval(f'self.eval_func{i+1}()')
            self.state.obj += f
            if self.state.initial:
                exec('self.f{}s = {}'.format(i+1,[f]))
            exec('self.f{}s.append({})'.format(i+1,f))

        self.objs.append(self.state.obj)
    
    #Evaluation on the number of compounds
    def eval_func1(self):
        if len(self.state.combination) > self.LimitNum:
            denominator = self.LimitNum**2 if len(self.TargetCombination) == 0 else len(self.TargetCombination)
            combination_num_score = math.exp(-(len(self.state.combination) / denominator))
        else:
            combination_num_score = 1
        self.state.f1 = combination_num_score      
        return self.state.f1
    
    #Correlation coefficient between gene expression data
    def eval_func2(self):
        correlation_score, p = pearsonr(self.Targets, self.state.integrated_profile)
        if math.isnan(correlation_score):
            correlation_score = 0
        self.state.f2 = correlation_score
        return self.state.f2
        
       