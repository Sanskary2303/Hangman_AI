import sys
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
from HangmanInputProcessor import HangmanInputProcessor
import Automate
import ModDict

class Hangman:
    def __init__(self, getAvg=False):
        self.weighted_list = []
        self.fill_factor_list = []
        self.indices_list = []
        self.toAvg = False
        self.TRIES = 6
        self.res_list = None

        if getAvg:
            self.toAvg = True

        self.setupGraphViz()
        self.rerunGame()

    def setupGraphViz(self):
        self.graphviz = GraphvizOutput()
        self.graphviz.output_file = 'flow_graph.png'
        with PyCallGraph(output=self.graphviz):
            isPassed = ModDict.loadAllDicts()
            if not isPassed:
                sys.exit("File not found in the current directory")

    def rerunGame(self):
        self.Inp = HangmanInputProcessor(self.toAvg)
        self.runGame()

    def runGame(self):
        self.res_list = []
        self.TRIES = 6
        Automate.clearAll()
        self.weighted_list = [None] * len(self.Inp.split_input_list)

        self.weighted_list = list(map(lambda x: list(ModDict.modDict.get(str(len(x)))), self.Inp.split_input_list))
        Automate.calculateLetterWeightOfList(self.weighted_list, True)

        self.fill_factor_list = [0] * len(self.Inp.split_input_list)
        self.indices_list = [[] for _ in range(len(self.Inp.split_input_list))]

        self.initializeState()
        if not self.toAvg:
            self.printState()
        self.playGame()

    def printState(self):
        print("".join(self.res_list))

    def displayStats(self):
        print("\nTRIES LEFT:", str(self.TRIES) + " out of 6\n")

    def initializeState(self):
        list_len = sum(map(len, self.Inp.split_input_list)) + (len(self.Inp.split_input_list) - 1)
        self.res_list = ["_"] * list_len

        inc = 0
        for x in self.Inp.split_input_list:
            inc += len(x)
            if inc < len(self.res_list):
                self.res_list[inc] = " "
                inc += 1

    def playGame(self):
        while self.TRIES != 0:
            ret = self.updateState()
            if not self.toAvg:
                self.printState()
            if ret == 1 or (ret == -1 and self.TRIES == 0):
                if not self.toAvg:
                    if ret == -1:
                        print("DEAD -- Game Over")
                    else:
                        print("ALL COMPLETED! SOLVED!")
                    self.displayStats()
                    self.rerunGame()
                break

            if len(Automate.sortedList) == 0 or (Automate.sortedList[-1][0] != 2 and Automate.sortedList[-1][0] != 1.5):
                Automate.calculateLetterWeightOfList(self.weighted_list, False)

    def updateState(self):
        prev_inc = 0
        letter_found = False

        guess = Automate.popMaxWeightChar()

        if not self.toAvg:
            print("Guess:", guess)

        if guess is not None:
            guess = guess.lower()

            for index, word in enumerate(self.Inp.split_input_list):
                if self.fill_factor_list[index] == 1.0:
                    prev_inc += len(word) + 1
                    continue

                idx_list = [x for x, val in enumerate(word) if val == guess]
                self.indices_list[index] = self.indices_list[index] + idx_list

                for x in idx_list:
                    self.res_list[prev_inc + x] = guess

                if len(idx_list) > 0:
                    letter_found = True

                    temp_weighted_list = []

                    for i in self.weighted_list[index]:
                        idx_matches = all(i[idx_num] == guess for idx_num in idx_list)
                        if idx_matches:
                            temp_weighted_list.append(i)

                    self.weighted_list[index] = temp_weighted_list
                    self.fill_factor_list[index] = len(self.indices_list[index]) / float(len(word))

                    if len(self.weighted_list[index]) == 1 and self.fill_factor_list[index] < 1:
                        Automate.prepForValidFoundSet(set(self.weighted_list[index][0]))

                else:
                    letter_found = False

                    for i in self.weighted_list[index][:]:
                        if guess in i:
                            self.weighted_list[index].remove(i)

                prev_inc += len(word) + 1
        else:
            print("no guess")
            if not self.toAvg:
                print("Cannot generate any more guesses.")
                self.rerunGame()

        not_filled_list = [i for i, val in enumerate(self.fill_factor_list) if val < 1]

        dirty_list = [x for i, x in enumerate(self.indices_list) if len(self.Inp.split_input_list[i]) - len(x) <= 2]
        if self.Inp.input_choice != "1" and len(dirty_list) == 0 and len(not_filled_list) != 0:
            if len(Automate.sortedList) == 0 or Automate.sortedList[-1][0] != 2:
                for x in not_filled_list:
                    idxLeft = (set(range(len(self.Inp.split_input_list[x]))) - set(self.indices_list[x])).pop()
                    maxFreqSet = Automate.createWordFreqSortedList(self.weighted_list[x])
                    Automate.addMostUniqueCharToList(maxFreqSet[-1][1][idxLeft])

        if len(not_filled_list) == 0:
            return 1

        if not letter_found:
            self.TRIES -= 1
            if not self.toAvg:
                self.displayStats()
            return -1

        return 0

if __name__ == '__main__':
    Hangman()
