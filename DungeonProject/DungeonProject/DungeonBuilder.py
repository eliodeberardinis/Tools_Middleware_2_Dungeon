import sys
import random

class DungeonBuilder:

    # Generates a tree graph that represents the high level structure of the dungeon
    # Nodes are represented by each letter character
    # Two nodes connected by one path are represented by two consecutive letters: XX
    # A node branching out into multiple paths is represented by X[path1, path2, ..., pathN]
    # The character '_' represents the points where the grammar will be expanding the tree on each iteration
    @staticmethod
    def buildGraph(numIter, difficultyLevel):
        g = "O_" #Axiom of the grammar
        prevExpansions = 1
        prevSplits = 0
        numSubIter = -1
        num2Splits = 0
        num3Splits = 0
        mylist = range(5) # list of integers from 0 to 4 
        random.shuffle(mylist)

        for i in range(numIter): #Generate iterations
            g_ = ""
            numSubIter += 1
            prevSplits = 0
            if numSubIter > 4:
                numSubIter = 0
                random.shuffle(mylist)
                num2Splits = 0
                num3Splits = 0
                   
            numNewExpansions = 0
            for c in g:
                if c == "_": #If it is an expansion character, apply the rules
                    #Decide on how many paths will branch out from this point (0 through 3)
                    #Only allow for 0 when there is at least another expansion character in the current iteration
                    #(meaning that at least one branch of the tree will reach the maximum number of iterations)

                    #Very Easy
                    if difficultyLevel == 1:
                        branches = 1
                    #Easy   
                    elif difficultyLevel == 2:
                        if numSubIter == mylist[0] and prevSplits < 1:  # Use prevSplit parameter if you want to count the splits globally
                            branches = 2
                            prevSplits += 1

                        elif prevExpansions > 1:
                                branches = random.randint(0,1)
                        else:
                                branches = 1                     
                    #Medium
                    elif difficultyLevel == 3:
                         if numSubIter in mylist[:2] and prevSplits < 2: # Use prevSplit parameter if you want to count the splits globally
                            if num3Splits < 1:
                               branches = random.randint(2,3)
                            else:
                                branches = 2
                           
                            prevSplits += 1
                            
                         elif prevExpansions > 1:
                                branches = random.randint(0,1)
                         else:
                            branches = 1

                         if branches == 2:
                               num2Splits += 1
                         elif branches == 3:
                               num3Splits += 1
                    #Hard
                    elif difficultyLevel == 4:
                         if numSubIter in mylist[:3] and prevSplits < 3: # Maybe change the rules to add minmum 2 1:2 splits
                            if num2Splits + num3Splits < 2:
                               branches = random.randint(2,3)
                            else:
                                branches = random.randint(0,2)

                            prevSplits += 1
                            
                         elif prevExpansions > 2:
                                branches = random.randint(0,1)
                         else:
                            branches = 1

                         if branches == 2:
                               num2Splits += 1
                         elif branches == 3:
                               num3Splits += 1
                
                    #VeryHard
                    elif difficultyLevel == 5:
                         if numSubIter in mylist[:4] and prevSplits < 4: # Maybe change the rules to add minmum 2 1:3 splits
                            if num2Splits + num3Splits < 3:
                               branches = random.randint(2,3)
                            else:
                                branches = random.randint(0,3)

                            prevSplits += 1
                            
                         elif prevExpansions > 3:
                                branches = random.randint(0,1)
                         else:
                            branches = 1

                         if branches == 2:
                               num2Splits += 1
                         elif branches == 3:
                               num3Splits += 1
                

                    prevExpansions -= 1
                    numNewExpansions += branches

                    if branches == 1:
                        #Expand the tree with one sequencial node
                        g_ += "X_"
                    elif branches > 1:
                        #Expand the tree with a branching structure
                        g_ += "[X_"
                        for j in range(branches-1):
                            g_ += ",X_"
                        g_ += "]"

                else: #If it is any other character, copy it to the string
                    g_ += c
            g = g_
            prevExpansions = numNewExpansions

        #Remove the expanding characters ('_') from the final graph string
        g_ = ""
        for c in g:
            if c != "_":
                g_ += c
        return g_



