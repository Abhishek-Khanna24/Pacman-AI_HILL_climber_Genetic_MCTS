# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math


class Node:
    def __init__(self, parent, listofactions, action, legal):
        if (action != []):
            self.listofactions = listofactions.append(action)
        self.listofactions = []
        self.action = action
        self.parent = parent
        self.leftaction = legal
        self.childlist = []
        self.score = 0
        self.number = 1


    def left(self, used):
        self.leftaction.remove(used)

    def findstate(self, tstate):
        for i in range(0, len(self.listofactions)):
            tstate = tstate.generatePacmanSuccessor(self.listofactions[i])
            if tstate == None:
                return None
            elif tstate.isWin():
                return 1
            elif tstate.isLose():
                return 0
        return tstate


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0, 10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0, len(self.actionList)):
            self.actionList[i] = possible[random.randint(0, len(possible) - 1)];
        tempState = state;
        for i in range(0, len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];


class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def __init__(self, index=0):
        Agent.__init__(self, index=0)

    def registerInitialState(self, state):

        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        possible = state.getAllPossibleActions()
        actionList = []
        loseflag = False
        Sflag = True

        for i in range(0, 5):
            actionList.append(possible[random.randint(0, len(possible) - 1)])
        maxs = [actionList[0], 0]

        while Sflag:
            tempstate = state

            for i in range(0, 5):
                r = random.randint(0, 1)
                if r == 1:
                    actionList[i] = possible[random.randint(0, len(possible) - 1)]

            for i in range(0, 5):
                tempstate = tempstate.generatePacmanSuccessor(actionList[i])
                if tempstate is None:
                    Sflag = False
                    break
                elif tempstate.isWin():
                    return actionList[0]
                elif tempstate.isLose():
                    loseflag = True
                    break

            if Sflag is False:
                break
            elif loseflag:
                loseflag = False
                continue
            else:
                tempvalue = gameEvaluation(state, tempstate)
                if tempvalue > maxs[1]:
                    maxs = [actionList[0], tempvalue]

        # print maxs
        return maxs[0]


class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def rankSelection(self):
        i = random.randint(1, 36)

        if i == 1:
            return 1
        elif i < 4:
            return 2
        elif i < 7:
            return 3
        elif i < 11:
            return 4
        elif i < 16:
            return 5
        elif i < 22:
            return 6
        elif i < 29:
            return 7
        elif i < 37:
            return 8

    # GetAction Function: Called with every frame
    def getAction(self, state):
        possible = state.getAllPossibleActions()
        # initial populations and its initializations

        population = []
        flag = True
        for i in range(0, 8):
            tempstate = state
            actionList = []
            for j in range(0, 5):
                actionList.append(possible[random.randint(0, len(possible) - 1)])

            for j in range(0, 5):
                tempstate = tempstate.generatePacmanSuccessor(actionList[j])
                if tempstate.isWin():
                    return actionList[0]
                elif tempstate.isLose():
                    break

            tempvalue = gameEvaluation(state, tempstate)

            population.append([actionList, tempvalue])

        while flag:
            population.sort(key=lambda population: population[1])

            temppopulation = []
            # rankselection and crossover
            for q in range(0, 4):

                rank1 = self.rankSelection() - 1
                rank2 = self.rankSelection() - 1
                if random.randint(1, 100) <= 70:
                    tempactionlist1 = []
                    tempactionlist2 = []
                    # TODO pair will generate two children by crossing- over. and save it in tempactionlist
                    for i in range(0, 5):
                        if random.randint(1, 100) < 50:
                            temp = (population[rank1][0])
                            tempactionlist1.append(temp[i])
                        else:
                            temp = (population[rank2][0])
                            tempactionlist1.append(temp[i])

                        if random.randint(1, 100) < 50:
                            temp = (population[rank1][0])
                            tempactionlist2.append(temp[i])
                        else:
                            temp = (population[rank2][0])
                            tempactionlist2.append(temp[i])

                    temppopulation.append(tempactionlist1)
                    temppopulation.append(tempactionlist2)
                else:
                    temppopulation.append(population[rank1][0])
                    temppopulation.append(population[rank2][0])

            # mutation

            for i in range(0, 8):
                if random.randint(1, 100) <= 10:
                    place = random.randint(0, 4)
                    temp = temppopulation[i]
                    temp[place] = possible[random.randint(0, len(possible) - 1)]
                    temppopulation[i] = temp

            # score evaluation
            for i in range(0, 8):
                tempstate = state
                actionList = temppopulation[i]

                for j in range(0, 5):
                    tempstate = tempstate.generatePacmanSuccessor(actionList[j])
                    if tempstate is None:
                        flag = False
                        break
                    elif tempstate.isWin():
                        return actionList[0]
                    elif tempstate.isLose():
                        break

                if flag:
                    tempvalue = gameEvaluation(state, tempstate)
                else:
                    break

                population[i] = [actionList, tempvalue]

        population.sort(key=lambda population: population[1])
        actionListbest = population[7][0]

        return actionListbest[0]


class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def Expand(self, node, state):

        untriedaction = node.leftaction[random.randint(0, len(node.leftaction) - 1)]
        node.left(untriedaction)
        tempstate = node.findstate(state)
        if tempstate is not None and tempstate is not 0 and tempstate is not 1:
            child = Node(node, node.listofactions, untriedaction, tempstate.getLegalPacmanActions())
            node.childlist.append(child)
            return child
        else:
            return tempstate

    def backpropagation(self, node,temps):
        while node.parent != None:
            node.score += temps
            node.number += 1
            node = node.parent

    def Select(self, node):
        max = -500

        for i in node.childlist:
            temp = (i.score / i.number) + math.sqrt((2 * (math.log(node.number))) / i.number)
            # math.log2()
            if max < temp:
                maxchild = i
                max = temp

        return maxchild

    def treepolicy(self, node, state):

        while True:
            if node is not None and node is not 0 and node is not 1:
                if node.leftaction:
                    return self.Expand(node, state)
                else:
                    node = self.Select(node)

        return node

    def Defaultpolicy(self, node, state):
        tempstate = node.findstate(state)
        # print tempstate

        for i in range(0, 5):
            if tempstate is not None and tempstate is not 0 and tempstate is not 1:
                tempaction = tempstate.getLegalPacmanActions()
                temp = gameEvaluation(state, tempstate)
                if tempaction:
                    tempstate = tempstate.generatePacmanSuccessor(random.choice(tempaction))
                else:
                    break
        return temp

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        flag = True
        # root = Node(None, [], state, state.getLegalPacmanActions())
        root = Node(None, [], [], state.getLegalPacmanActions())

        while flag:
            node = self.treepolicy(root, state)
            if node is not 0 and node is not 1 and node is not None:
                delta = self.Defaultpolicy(node, state)
                self.backpropagation(node,delta)
            else:
                flag = False
                break

        maxno = 0



        scores =[]
        for i in root.childlist:

            scores.append(i.number)

        best_score = max(scores)
        best_child = [root.childlist[i] for i, score in enumerate(scores) if score == best_score]

        return (random.choice(best_child)).action

