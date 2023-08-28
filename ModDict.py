import json
import os.path

modDict = {}
freqDict = {}

def createModDict():
    print("Processing lexicon...")

    with open('dict.txt', 'r') as data_file:
        for word in data_file:
            word = word.strip().lower()
            if len(word) in modDict:
                wordsOfSpecificLength = modDict[len(word)]
                wordsOfSpecificLength.append(word)
                modDict[len(word)] = wordsOfSpecificLength
            else:
                wordsOfSpecificLength = [word]
                modDict[len(word)] = wordsOfSpecificLength

    with open('ModDict.json', 'w', encoding='utf-8') as outfile:
        json.dump(modDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print("Finished!")

def loadAllDicts():
    global modDict, freqDict

    modDictFile = "./ModDict.json"
    freqDictFile = "./FreqDict.json"

    if not os.path.isfile(modDictFile):
        try:
            createModDict()
        except Exception as e:
            print("Error creating ModDict:", str(e))
            return False

    with open(modDictFile, 'r', encoding='utf-8') as data_file:
        modDict = json.load(data_file)

    if not os.path.isfile(freqDictFile):
        try:
            parseFreqDict()
        except Exception as e:
            print("Error parsing FreqDict:", str(e))
            return False

    with open(freqDictFile, 'r', encoding='utf-8') as data_file:
        freqDict = json.load(data_file)

    return True

def parseFreqDict():
    print("Processing word frequency dictionary...")

    with open('freq.txt', 'r') as data_file:
        for line in data_file:
            freqLine = list(map(lambda x: x.strip(), line.lower().split()))
            freqDict[freqLine[0]] = freqLine[1]

    with open('FreqDict.json', 'w', encoding='utf-8') as outfile:
        json.dump(freqDict, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    print("Finished!")

if __name__ == '__main__':
    loadAllDicts()  # Example usage to load dictionaries
