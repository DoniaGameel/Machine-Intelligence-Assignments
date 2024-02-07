# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0.2,
        "discount_factor": 1,  
        "living_reward": -3 # large negative number so it refers the neares terminal
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 0.3,
        "living_reward": -0.1  # small penalty so it prefer avoiding the dangerous path
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1.1, # greater than 1 so it avoids the near terminal and keep going till the far terminal
        "living_reward": -3
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,
        "discount_factor": 0.7,
        "living_reward": -2
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.0,
        "discount_factor": 0.9,
        "living_reward": 11 # greater than the max reward so it prefer keep the episode going on forever.
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -21 # so -10 is higher than  living_reward + 10 so it always avoids +10 path
    }