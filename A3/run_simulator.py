from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

def next_state_2(state,x1,y1):
    action_steer = None
    action_acc = None
    x,y,velocity, angle = state

    if angle<0:
        angle+=360
    correct_angle = np.arctan2(y1-y,x1-x)*(180/np.pi)
    #print(correct_angle)
    if correct_angle<0:
        correct_angle += 360
    #print(correct_angle,x,y,velocity,angle)
    if abs(correct_angle-angle)<3 or abs(correct_angle-angle)>357:
        action_acc = 4
        action_steer = 1
    elif correct_angle ==0:
        if angle>=3 and angle<=180:
            action_steer=0
            action_acc =0
        elif angle>=180 and angle<=357:
            action_steer = 2
            action_acc = 0
        if velocity==0:
            action_acc = 3
    elif correct_angle<=180:
        if angle<=correct_angle:
            action_steer = 2
            action_acc = 0
        elif angle <= correct_angle+90:
            action_steer = 0
            action_acc = 0
        elif angle <= correct_angle+180:
            action_steer = 0
            action_acc = 0
        elif angle <= correct_angle+270:
            action_steer = 2
            action_acc = 0
        elif angle <= correct_angle+360:
            action_steer = 2
            action_acc = 0
        if velocity==0:
            action_acc = 3
    elif correct_angle>=270:
        if angle>=correct_angle:
            action_steer = 0
            action_acc = 0
        elif angle>=correct_angle-90:
            action_steer = 2
            action_acc = 0
        elif angle >= correct_angle-180:
            action_steer = 2
            action_acc = 0
        elif angle >= correct_angle-270:
            action_steer = 0
            action_acc = 0
        elif angle >= correct_angle-360:
            action_steer = 0
            action_acc = 0
        if velocity==0:
            action_acc = 3

    if velocity==0:
        action_acc=3
    action = np.array([action_steer, action_acc])  
    #print(action)

    return action

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None
        x,y,velocity, angle = state

        if angle<0:
            angle+=360
        #print(state)
        correct_angle = np.arctan2(-y,350-x)*(180/np.pi)
        if correct_angle<0:
            correct_angle += 360
        # print(correct_angle,x,y,velocity,angle)
        if abs(correct_angle-angle)<3 or abs(correct_angle-angle)>357:
            action_acc = 4
            action_steer = 1
        elif correct_angle ==0:
            if angle>=3 and angle<=180:
                action_steer=0
                action_acc = 2 #2
            elif angle>=180 and angle<=357:
                action_steer = 2
                action_acc = 2 #2
            if velocity==0:
                action_acc = 2 #3
        elif correct_angle<=180:
            if angle<=correct_angle:
                action_steer = 2
                action_acc = 2 #2
            elif angle <= correct_angle+90:
                action_steer = 0
                action_acc = 2 # 3
            elif angle <= correct_angle+180:
                action_steer = 0
                action_acc = 2 # 1
            elif angle <= correct_angle+270:
                action_steer = 2
                action_acc =2 # 1
            elif angle <= correct_angle+360:
                action_steer = 2
                action_acc = 0 #2
            if velocity==0:
                action_acc = 2 #3
        elif correct_angle>=270:
            if angle>=correct_angle:
                action_steer = 0
                action_acc = 2 #4
            elif angle>=correct_angle-90:
                action_steer = 2
                action_acc = 2 #3
            elif angle >= correct_angle-180:
                action_steer = 2
                action_acc = 2 #1
            elif angle >= correct_angle-270:
                action_steer = 0
                action_acc = 2 #0
            elif angle >= correct_angle-360:
                action_steer = 0
                action_acc = 2
            if velocity==0:
                action_acc = 2 #3

        if velocity==0:
            action_acc=3

        
        action = np.array([action_steer, action_acc])  
        # print(state,correct_angle,action)
        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state, ran_cen_list):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """
        x,y,velocity, angle = state
        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None
        y_neg_Max = -1000
        y_pos_min = 1000
        centre_list = []
        for l in ran_cen_list:
            if l[1]<0:
                y_neg_Max = max(y_neg_Max,l[1])
                if y<0:
                    centre_list.append([l[0]-75,l[0]+75])
            else:
                y_pos_min = min(y_pos_min,l[1])
                if y>0:
                    centre_list.append([l[0]-75,l[0]+75])
        if y>(y_neg_Max+75) and y<(y_pos_min-75):
            agents = Task1()
            return agents.next_action(state)

        centre_list.sort()
        # print(centre_list,x,y,velocity,angle)
        # print(next_state_2(state,0,y))

        if (x>=centre_list[0][0] and x<=centre_list[0][1]):
            return next_state_2(state,0,y)
        elif (x>=centre_list[1][0] and x<=centre_list[1][1]):
            return next_state_2(state,315,y)
        
        
        return next_state_2(state,x,0)
        


        #  action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                # agents = Task1()
                # action = agents.next_action(state)
                action = self.next_action(state,ran_cen_list)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps
    

    random.seed(random_seed)
    np.random.seed(random_seed)
    

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
