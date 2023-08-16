import argparse
import numpy as np

#probability that b wins before giving striker back to a or balls becoming zero
def Bwin(start_ball,runs_needed,q):
    max_runs = (start_ball-1)//6 + 1
    if runs_needed > max_runs:
        return 0
    if runs_needed == 1:
        n = start_ball%6
        if n==0:
            n=6
        prob = 0
        step = (1-q)/2
        for i in range(n):
            prob += step
            step *= (1-q)/2
        return prob
    if runs_needed == 2:
        n = start_ball%6
        if n==0:
            n=6
        prob = 0
        step = np.power((1-q)/2,n)
        for i in range(6):
            step *= (1-q)/2
            prob += step
        return prob
    if runs_needed == 3:
        n = start_ball%6
        prob = 0
        step = np.power((1-q)/2,n+6)
        for i in range(6):
            step *= (1-q)/2
            prob += step
        return prob
    return 0




    

#if ball1 is stricked by a, then given that ball2 stricked by A, and remaining balls between them are stricked by B
#check possible A_score and B_score
def check(balls1,balls2,A_score, B_score):
    if balls2==balls1-1:
        if balls1%6==1:
            if (A_score==1 or A_score==3) and B_score==0:
                return True 
        else:
            if (A_score==0 or A_score==2 or A_score==4 or A_score==6 ) and B_score==0:
                return True
    else:
        if balls1%6==1:
            if A_score==0 or A_score==2 or A_score==4 or A_score==6:
                if balls2%6==0:
                    if B_score== 0 :                  
                        return True
                else:
                    if B_score == balls1//6 - balls2//6:
                        return True    
        else:
            if A_score==1 or A_score==3:
                if balls1>13 and balls2%6==0:
                    if B_score==balls1//6 - balls2//6:
                        return True
                elif balls1<=12 and balls2%6==0 and B_score==0:
                    return True
                elif balls2%6!=0 and B_score == (balls1-1)//6 - balls2//6 + 1:
                    return True
    return False


def encoderMdp(p1_parameters,q, states):
    d = dict()
    numStates = 0
    for i in range(states.shape[0]):
        d[states[i]] = i 
        numStates += 1
    state_win = numStates
    numStates += 1
    state_out = numStates
    numStates += 1
    numActions = 5
    transition = np.zeros((numStates,numActions,numStates))
    rewards = np.zeros((numStates,numActions,numStates))
    rewards[:,:,state_win] = 1
    for s in d:
        balls = s//100
        runs = s%100
        for i in range(1,balls):
            for j in range(1,runs+1):
                score = runs-j
                for A_score in range(min(7,score+1)):
                    if A_score!=5:
                        B_score = score-A_score
                        if (check(balls,i,A_score,B_score)) is True:
                            transition[d[s],:,d[i*100+j]] += p1_parameters[:,A_score]*np.power((1-q)/2,balls-i-1)

        #winning probability...
        if balls==1:
            if runs<=6:
                for i in range(runs,7):
                    if(i!=5) :
                        transition[d[s],:,state_win] += p1_parameters[:,i]
        else:
            for i in range(7):
                if i != 5:
                    if i< runs:
                        if (balls%6==1 and (i==0 or i==2 or i==4 or i==6)) or (balls%6!=1 and (i==1 or i==3)):
                            transition[d[s],:,state_win] += p1_parameters[:,i]*Bwin(balls-1,runs-i,q)
                    else:
                        transition[d[s],:,state_win] += p1_parameters[:,i]
        #loosing probability
        transition[d[s],:,state_out] += 1- np.sum(transition[d[s]],axis=1)

    end = 0
    print("numStates "+ str(numStates))
    print("numActions " + str(5))
    print("end " + str(0))
    for s0 in range(numStates):
        for a in range(numActions):
            for s1 in range(numStates):
                if(transition[s0,a,s1] != 0):
                    s00 = s0
                    s11=s1
                    # if s00< states.shape[0]:
                    #     s00 = str(states[s0])
                    # if s11 < states.shape[0]:
                    #     s11 = str(states[s1])
                    print("transition " + str(s00)  + " " + str(a) + " " + str(s11)+ " " + str(rewards[s0,a,s1]) + " "+ str(transition[s0,a,s1]))
    print("mdptype episodic")
    print("discount 1")
    return



if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--states",type=str,required=True)
    parser.add_argument("--parameters",type=str,required=True)
    parser.add_argument("--q",type=str,required=True)
    args = parser.parse_args()

    q = float(args.q)
    try:
        statefile = open(args.states,'r')
        parameterfile = open(args.parameters,'r')
    except IOError:
        print("Please check the path of the provided files")
        exit(1)
    states_ = []
    lines_ = statefile.readlines()
    states_ = [int(x.strip()) for x in lines_]
    states_ = np.array(states_)
    lines = parameterfile.readlines()
    lines = [x.strip() for x in lines]
    p1_parameters = np.zeros((5,8))
    for i in range(5):
        num = lines[i+1].split()
        # for j in range(7):
        #     p1_parameters[i][j] = float(num[j+1])
        p1_parameters[i,0] = float(num[2])
        p1_parameters[i,1] = float(num[3])
        p1_parameters[i,2] = float(num[4])
        p1_parameters[i,3] = float(num[5])
        p1_parameters[i,4] = float(num[6])
        p1_parameters[i,5] = float(0)
        p1_parameters[i,6] = float(num[7])
        p1_parameters[i,7] = float(num[1])
    # print(p1_parameters)
    encoderMdp(p1_parameters,q,states_)

        

            

        
            


        

                
                    
                 
        
            

            


        
                

            



    
     

    