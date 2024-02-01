import copy
import json
import math
from tqdm import tqdm
import random
import time
import datetime
import os

class State():
    def __init__(self):
        self.initial = True
        self.iteration = 0

class SimulatedAnnealing():
    Ps= []
    Changes = []
    
    #set condition
    def __init__(self, state, params, optimize_data, target_data):
        #state
        self.state = state
        
        # data
        self.optimize_data = optimize_data
        self.target_data = target_data
    
        #params
        self.params = params
        
        #params
        for k, v in params.items():
            exec('self.{} = {}'.format(k,v))
            
       
        

    #calc probability
    def prob(self):
        if self.state.obj >= self.tmp_state.obj:
            p = 1
        else:
            p = math.exp( (self.state.obj - self.tmp_state.obj) * self.state.iteration / self.datasize)
        return p
    
    def get_values(self, combination, used_flag=False):
        values = []
        
        used_combination = []
        for k in combination:
            key_info = []
            key_info.append(k)
            try:
                d = self.data[k]
                values.append(d)
                used_combination.append(d)
            except:
                pass   
        self.state.compound_info = used_combination
        if used_flag:
            return values, used_combination
        
        return values
    
    # calc eval function score
    def calc_eval_func(self):
        self.state.obj = 0
        for i in range(self.EvalNum):
            f = eval(f'self.eval_func{i+1}()')
            self.state.obj +=  f
            
            if self.state.initial:
                exec('self.f{}s = {}'.format(i+1,[]))
            exec('self.f{}s.append({})'.format(i+1,f))
            
        self.objs.append(self.state.obj)
        pass
        
    def eval_func1(self):
        #return self.state.f1
        pass
    
    def eval_func2(self):
        #return self.state.f2
        pass

    def get_targets_info(self):
        # get Targets from TargetCombination
        self.data = self.target_data
        if self.Targets == []:
            self.Target_values, used_combination = self.get_values(self.TargetCombination, used_flag=True)
            self.params['UsedTargetCombination'] = used_combination
            self.Targets = self.get_targets(self.Target_values)
            if len(self.Targets) == 0:
                print(f"\n{self.TargetCombination} not have Targets (e.g. target pathway)")
                exit()
            self.params['Targets'] = self.Targets

    # set initial state
    def set_initial_state(self):
        
        # get target infomartion
        self.get_targets_info()

        # initial state
        self.data = self.optimize_data
        
        self.datasize = len(self.data)
        self.state.combination = random.sample(self.data.keys(), self.LimitNum)
        self.objs = []
        self.state.values = self.get_values(self.state.combination)
        self.calc_eval_func()
        self.best_state = copy.deepcopy(self.state)
        self.state.initial = False
        
        
        
        
    # select change type
    def select_change_type(self):
        flag = random.choice([0,1])
        if flag == 0:
            return "remove"
        else:
            return "add"
    
    # add change
    def add_change(self):
        selected_keys = list(set(self.data.keys()) - set(self.state.combination))
        if len(selected_keys) == 0:
            pass
        else:
            add_key = random.choice(selected_keys)
            self.state.combination.append(add_key)
            self.state.values = self.get_values(self.state.combination)
            self.calc_eval_func()

    # remove change
    def remove_change(self):
        if len(self.state.combination) > 1:    
            remove_key = random.randint(0,len(self.state.combination)-1)
            self.state.combination.pop(remove_key)
            self.state.values = self.get_values(self.state.combination)
            self.calc_eval_func()
    
    def optimization(self):
        start = time.time()
        with tqdm() as pbar:
            while self.MaxIteration > self.state.iteration and self.MaxTime > (time.time() - start):
                
                pbar.update(1)
                
                # initialization
                if self.state.initial:
                    self.set_initial_state()
                
                else:
                    self.state.iteration += 1
                    self.tmp_state = copy.deepcopy(self.state)
                    change_type = self.select_change_type()

                    if change_type == 'add':
                        self.add_change()

                    elif change_type == 'remove':
                        self.remove_change()

                    # judge update
                    p = self.prob()
                    self.Ps.append(p)
                    if random.random() <= p:
                        self.Changes.append(True) #update state
                        if self.state.obj > self.best_state.obj:
                            self.best_state = copy.deepcopy(self.state) #update best state
                    else:
                        self.state = copy.deepcopy(self.tmp_state) #not update state
                        self.Changes.append(False)
        
        self.params['EndIteration'] = self.state.iteration
        self.params['EndTime'] = time.time() - start

        return self.best_state
    
    def save_info(self, path = None):
        
        def get_time_path(out_put_path = ""):
            now = datetime.datetime.now()
            if out_put_path != "":
                path = os.path.join("../results" ,out_put_path)
            else:
                new = "{0:%Y%m%d_%H%M%S}".format(now)
                path = os.path.join("../results" ,new)
            return path
        
        def makefile(path=None):
            if path is not None:
                path = get_time_path(path)
                if os.path.exists(path) == False:
                    os.makedirs(path)
                    print(f'Create {path}')
                else:
                    path = get_time_path()
                    os.makedirs(path)
                    print('The specified file exists')
                    print(f'Create {path}')
            else:
                path = get_time_path()
                os.makedirs(path)
                print(f'Create {path}')
            return path
            
            
            
            
        
        def save_state(state, file, flag):
            if flag == 'final':
                state_path = os.path.join(file, 'final_state.json')
            elif flag == 'best':
                state_path = os.path.join(file, 'best_state.json')
            with open(state_path, 'wt') as f:
                json.dump(vars(state), f, indent=2, ensure_ascii=False)
            print(f'Create {state_path}')
            
                          
        output_path = makefile(path)
        SA_info_path = os.path.join(output_path, 'SA_info.json')
        with open(SA_info_path, 'wt') as f:
            json.dump(self.params, f, indent=2, ensure_ascii=False)
        print(f'Create {SA_info_path}')
        
        prob_path = os.path.join(output_path, 'probability.txt')
        with open(prob_path, 'w') as f:
            for p in self.Ps:
                f.write(f'{p}\n')
        print(f'Create {prob_path}')
                
        change_path = os.path.join(output_path, 'change.txt')
        with open(change_path, 'w') as f:
            for c in self.Changes:
                f.write(f'{c}\n')
        print(f'Create {change_path}')
        
        obj_path = os.path.join(output_path, 'obj.txt')
        with open(obj_path, 'w') as f:
            for o in self.objs:
                f.write(f'{o}\n')
        print(f'Create {obj_path}')
        
        for i in range(self.EvalNum):
            score_path = os.path.join(output_path, f'f{i+1}.txt')
            with open(score_path, 'w') as f:
                for s in eval('self.f{}s'.format(i+1)):
                    f.write(f'{s}\n')
            print(f'Create {score_path}')
        
       
        save_state(self.state, output_path, 'final')
        
        save_state(self.best_state, output_path, 'best')
        