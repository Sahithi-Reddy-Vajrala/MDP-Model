import argparse
import numpy as np
from pulp import *



class Mdp:
    def __init__(self, mdptype, numStates, numActions, end, transition, rewards, discount):
        self.mdptype = mdptype
        self.numStates = numStates #s
        self.numActions = numActions #a
        self.end = end
        self.transition = transition # shape: sxaxs
        self.rewards = rewards #shape: sxaxs
        self.discount = discount

    def evalPolicy(self,given_policy):
        given_policy = np.reshape(given_policy,(self.numStates,))
        A = np.identity(self.numStates) - (self.discount)*(self.transition[np.arange(self.numStates),given_policy])
        B = np.sum(np.multiply(self.transition[np.arange(self.numStates),given_policy],self.rewards[np.arange(self.numStates),given_policy]),axis=1)
        B = np.reshape(B,(self.numStates,))
        values = np.linalg.solve(A,B)
        return values

    def value_iteration(self):
        optimal_policy = np.zeros((self.numStates,),dtype='int')
        old_values = self.evalPolicy(optimal_policy)
        old_values = np.array(old_values,dtype='float64')
        new_values = np.zeros((self.numStates,),dtype='float64')
        while True:
            trv = np.sum(np.multiply(self.transition,self.rewards+self.discount*np.resize(old_values,self.transition.shape)),axis=2)
            new_values = np.max(trv,axis=1)
            optimal_policy = np.argmax(trv,axis=1)
            if np.all(new_values==old_values):
                return new_values,optimal_policy
            old_values = np.copy(new_values)
        return new_values, optimal_policy

    def linearProgramingFormulation(self):
        prob = pulp.LpProblem('MdpSolver', LpMaximize)
        desicion_variables = []
        for i in range(self.numStates):
            variable = str('V' + str(i))
            variable = pulp.LpVariable(str(variable))
            desicion_variables.append(variable)
        value = ""
        for variable in desicion_variables:
            value += -1*variable
        prob += value
        for s in range(self.numStates):
            for a in range(self.numActions):
                l = []
                for s_ in range(self.numStates):
                    if s==s_:
                        l.append((desicion_variables[s_],1-1*self.discount*self.transition[s,a,s_]))
                    else:
                        l.append((desicion_variables[s_],-1*self.discount*self.transition[s,a,s_]))
                sum_ = np.sum(np.multiply(self.transition[s,a,:],self.rewards[s,a,:]))
                prob += LpAffineExpression(l) >= sum_
        optimization_result = prob.solve(PULP_CBC_CMD(msg=0))
        #PULP_CBC_CMD(msg=0)
        V = np.zeros((self.numStates,))
        for v in prob.variables():
            # V.append(v.varValue)
            V[int(str(v)[1:])] = v.varValue
        optimal_policy = np.argmax(np.sum(np.multiply(self.transition,self.rewards+self.discount*np.resize(V,self.transition.shape)),axis=2),axis=1)
        return V,optimal_policy


    def policyIteration(self):
        old_policy = np.zeros((self.numStates,),dtype='int')
        V = self.evalPolicy(old_policy)
        new_policy = np.argmax(np.sum(np.multiply(self.transition,self.rewards+self.discount*np.resize(V,self.transition.shape)),axis=2),axis=1)
        while np.any(new_policy!=old_policy):
            old_policy = np.copy(new_policy)
            V = self.evalPolicy(old_policy)
            new_policy = np.argmax(np.sum(np.multiply(self.transition,self.rewards+self.discount*np.resize(V,self.transition.shape)),axis=2),axis=1)
        return V,new_policy

        



# mdptype = 'episodic'
# numStates = 3
# numActions = 2
# end = -1
# transition = np.array([[[1.0,0,0],[0.5,0.5,0]],[[1,0,0],[0.25,0,0.75]],[[1, 0, 0],[0,0.5,0.5]]])
# rewards = np.array([[[1.0,0,0],[0,-1,0]],[[2,0,0],[-1,0,-2]],[[1, 0, 0],[0,3,3]]])
# given_policy = np.array([0, 0, 1]) 
# discount = 0.9
# obj = Mdp(mdptype,numStates,numActions,end,transition,rewards,discount)
# print(obj.evalPolicy(given_policy))
# print(obj.value_iteration())
# print(obj.linearProgramingFormulation())
# print(obj.policyIteration())

if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp",type=str,required=True)
    parser.add_argument("--algorithm",type=str,required=False)
    parser.add_argument("--policy",type=str,required=False)
    args = parser.parse_args()
    try:
        f = open(args.mdp,"r")
    except IOError:
        print("Please check the path of mdp file")
        exit(1)
    if args.algorithm != None and args.policy!=None:
        print("you cannot provide both algorithm and policy together")
        exit(1)
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    mdptype,numStates, numActions, end, transition, rewards, discount = 0,0,0,0,0,0,0
    for x in lines:
        x = x.split(" ")
        x = list(filter(None, x))
        if x[0]== "numStates":
            numStates = int(x[1])
        elif x[0] == "numActions":
            numActions = int(x[1])
            transition = np.zeros((numStates,numActions,numStates))
            rewards = np.zeros((numStates,numActions,numStates))
        elif x[0]=="end":
            end = int(x[1])
        elif x[0] == "transition":
            transition[int(x[1]),int(x[2]),int(x[3])] = float(x[5])
            rewards[int(x[1]),int(x[2]),int(x[3])] = float(x[4])
        elif x[0]=="mdptype":
            mdptype= x[1]
        elif x[0] == "discount":
            discount = float(x[1])
    f.close()
    obj = Mdp(mdptype,numStates, numActions, end, transition, rewards, discount)
    if args.policy != None:
        try:
            f = open(args.policy,"r")
        except IOError:
            print("Please check the path of policy file")
            exit(1)
        lines = f.readlines()
        lines = [int(x.strip()) for x in lines]
        lines = np.array(lines)
        V = obj.evalPolicy(lines)
        for i in range(numStates):
            print(str('%.6f'% V[i]) + " "+ str(lines[i]))
        f.close()
    elif args.algorithm==None:
        V, optimal_policy = obj.value_iteration()
        for i in range(numStates):
            print(str('%.6f'% V[i])+" "+str(optimal_policy[i]))
    elif args.algorithm=="vi":
        V, optimal_policy = obj.value_iteration()
        for i in range(numStates):
            print(str('%.6f'% V[i])+" "+str(optimal_policy[i]))
    elif args.algorithm=="hpi":
        V, optimal_policy = obj.policyIteration()
        for i in range(numStates):
            print(str('%.6f'% V[i])+" "+str(optimal_policy[i]))
    elif args.algorithm=="lp":
        V, optimal_policy = obj.linearProgramingFormulation()
        for i in range(numStates):
            print(str('%.6f'% V[i])+" "+str(optimal_policy[i]))
        
    
