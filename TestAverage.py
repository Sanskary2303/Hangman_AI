import Hangman
import sys

def getAverage():
    TOTAL_TESTS = 200
    correct = 0
    try:
        for x in range(TOTAL_TESTS):
            hangman_instance = Hangman.Hangman(getAvg=True)  # Create an instance with getAvg set to True
            tries = hangman_instance.TRIES
            if tries != 0:
                correct += 1
            print("\rTests Done: %d/%d" % (x + 1, TOTAL_TESTS), end='')
            sys.stdout.flush()
    except Exception as e:
        print(str(e))

    return correct / float(TOTAL_TESTS)

if __name__ == '__main__':
    avg = getAverage()
    print("\nAverage:", "%.4f%%" % (avg * 100))
