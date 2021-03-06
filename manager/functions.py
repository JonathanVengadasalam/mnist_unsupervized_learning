# -*- coding: utf-8 -*-
import random
from time import time
import numpy as np

def play(rootenv, ai, envlist=[], verbose=0):
    env, node = rootenv.clone(), None
    manturn = random.choice([1,-1])
    print("Man is the player {}".format(manturn) + "\n" + str(env))
    continue_game = True
    order = ""
    
    while continue_game:
        envlist.append(env.clone())
        if env.playerJustMoved != manturn:
            ask_order = True
            while ask_order: 
                order = input("Saisissez une commande : ")
                if order == "q":
                    continue_game = False
                    ask_order = False
                    continue
                move = env.convertmove(order)
                if type(move) != type(None):
                    node = ai.updatenode(node, move)
                    env.domove(move)
                    ask_order = False
        else:
            node = tree = ai.getnode(rootenv=env, rootnode=node)
            move = tree.move
            env.domove(move)

        if order != "q":
            print("\nMove: " + str(move+1) + "\n" + str(env))
        else:
            print("Vous avez quittez")
        if env.getmoves() == []: continue_game = False

    if order != "q":
        if env.value() == 1.0:
            st = "Man" if manturn == env.playerJustMoved else "Computer"
            print(st + " wins!")
        else:
            print("Nobody wins!")

    return node

def selfplay(rootenv, iteration, ai1, ai2, xlist=[], ylist=[], resultlist=[], envlist=[], verbose=3):
    
    d1 = time()

    for i in range(iteration):

        d2 = time()

        #initialize ais and variables
        ai2.turn = random.choice([1,-1])
        ai1.turn = -1*ai2.turn
        len0 = len(xlist)
        env = rootenv.clone()
        node1, node2 = None, None

        #play game, collect x and policy
        while (env.getmoves() != []):
            if env.playerJustMoved == ai2.turn:
                tree = node1 = ai1.getnode(rootenv=env, rootnode=node1)
                node2 = ai2.updatenode(node2, tree.move)
                if ai1.add_data:
                    xlist.append(env.x())
                    ylist.append(env.y(tree.move))
            else:
                tree = node2 = ai2.getnode(rootenv=env, rootnode=node2)
                node1 = ai1.updatenode(node1, tree.move)
                if ai2.add_data:
                    xlist.append(env.x())
                    ylist.append(env.y(tree.move))
            env.domove(tree.move)
        
        #collect value
        value, pjm = env.value(), env.state[0,0,-1]
        for j in range(len0,len(xlist)):
            ylist[j][-1] = value if pjm == xlist[j][0,0,-1] else 1 - value
        
        #collect result
        result = ai2.turn*env.playerJustMoved if env.value() == 1.0 else 0
        envlist.append(env)
        resultlist.append(result)
        if verbose & 1 == 1: print(i, round(time()-d2,2), result)
    
    if verbose & 2 == 2: print(iteration, round(time()-d1,2), getresult(ai1,ai2,resultlist))

def testposition(env, ai, move, iteration=50, verbose=1):
    k = []
    d = time()
    for i in range(iteration):
        s = 1 if ai.getnode(env,None).move == move else 0
        k.append(s)
    d = round(time() - d,2)
    if verbose & 1 == 1: print(d, len(k), sum(k))

def getresult(ai1, ai2, resultlist):
    res = np.array(resultlist)
    return {ai1.name:res[res==-1].shape[0], "draw":res[res==0].shape[0], ai2.name:res[res==1].shape[0]}
