import string

class WordleSolver:
    def __init__(self, WordListPath, UsedListPath, ScoreListPath, WordLength):
        # ? with ascii 63 will mark incorrect letters
        self.LTR_WRONG = '?'
        # ! with ascii 33 will mark correct letters
        self.LTR_RIGHT = '!'
        # * with ascii 42 will mark displaced letters
        self.LTR_CLOSE = '*'

        self.words = []
        self.allWords = []
        self.WordLength = WordLength

        self.lastGuessed = ""
        self.solution = [self.LTR_WRONG]*self.WordLength
        self.numCorrect = 0
        self.inSolution = {}
        self.misplacedLetters = []
        self.noMoreInSolution = set()        
        for c in string.ascii_lowercase:
            self.inSolution[c] = []
        self.buildWordList(WordListPath, UsedListPath, ScoreListPath)
    
    # Create the word list that will be used for guessing
    def buildWordList(self, WordListPath, UsedListPath, ScoreListPath):
        # initialize letter statistics for scoring
        commonLetters = {}
        for c in string.ascii_lowercase:
            commonLetters[c] = [0]*self.WordLength

        # File Processing
        words = {}
        wordFile = open(WordListPath, "r")
        for word in wordFile:
            # initialize the word common score
            word = word.lower().rstrip()
            words[word] = 0
            # count the word-space occurances 
            for i in range(self.WordLength):
                commonLetters[word[i]][i] += 1
        wordFile.close()

        self.allWords = words.keys()

        # compute the scoring of each word (include usage scroing, which I have found to not be useful)
        # scoreFile = open(ScoreListPath, "r")
        # i = 0
        # wordKeys = list(words.keys())
        # for score in scoreFile:
        #     words[wordKeys[i]] = int(score)/2
        #     if len(set(word)) == len(word):
        #         words[wordKeys[i]] += 100
        #     for j in range(self.WordLength):
        #         words[wordKeys[i]] += commonLetters[word[j]][j]
        #     i+=1
        # scoreFile.close()

        # remove words which are already guessed from the word list
        usedFile = open(UsedListPath, "r")
        wordKeys = list(words.keys())
        for word in usedFile:
            word = word.lower().rstrip()
            # if the word has been used before it should not be used for guessing
            if word in wordKeys:
                del words[word]
        usedFile.close()

        # letter commonality scoring
        for word in words:
            for j in range(self.WordLength):
                words[word] += commonLetters[word[j]][j]

        # created a sorted list of the words for picking priority
        self.words = sorted(words, key=words.get, reverse=True)

        self.lastGuessed = self.findFirstGuess()

    # findFirstGuess chooses the first word withotu duplicates to maximize info gained
    def findFirstGuess(self):
        for word in self.words:
            if len(set(word)) == len(word):
                return word
        return self.words[0]

    # checkDone checks if the game has finished (ie the wordle has been guessed)
    def checkDone(self):
        numCorrect = 0
        for i in range(self.WordLength):
            if self.solution[i] != self.LTR_WRONG:
                numCorrect+=1
        self.numCorrect = numCorrect
        return numCorrect == self.WordLength
    
    # tryNext picks the next guess for the game
    def tryNext(self, mask):
        # update vars
        for i in range(5):
            # The letter os not in the word
            if mask[i] == self.LTR_WRONG:
                self.noMoreInSolution.add(self.lastGuessed[i])
                # add to misplaced letter as well for cases where word has multiple of the same letter
                self.inSolution[self.lastGuessed[i]].append(i)
            # the letter is in the word
            elif mask[i] == self.LTR_CLOSE:
                self.inSolution[self.lastGuessed[i]].append(i)
                self.misplacedLetters.append(self.lastGuessed[i])
            # the letter is in the right place in the word
            if mask[i] == self.LTR_RIGHT:
                self.solution[i] = self.lastGuessed[i]
                if self.lastGuessed[i] in self.misplacedLetters:
                    self.misplacedLetters.remove(self.lastGuessed[i])

        # check if we can exit since we are done
        if self.checkDone():
            return "".join(self.solution)

        # pick a new guess
        if self.numCorrect == self.WordLength - 1 and len(self.words) > 2:
            # despite having nearly solved the word, there are too many options left. Knock out multiple in one guess by guessing an unrelated word
            # find the unknown index in the solution
            unknownIndex = 0
            for c in self.solution:
                if c == self.LTR_WRONG:
                    break
                unknownIndex+=1
            # pick the letters that are in the word options but not in the solution
            letters = set()
            for word in self.words:
                letters.add(word[unknownIndex])
            # further processing may be useful in the case where the solution has a duplicate letter
            # find the word that knocks out the most possible guesses
            maxInWord = 0
            maxWord = ""
            for word in self.allWords:
                inWord = 0
                for c in word:
                    if c in letters:
                        inWord+=1
                if inWord > maxInWord:
                    maxInWord = inWord
                    maxWord = word
            self.lastGuessed = maxWord
            return maxWord 
        else:
            # guess as normal
            for word in self.words:
                valid = True
                for i in range(self.WordLength):
                    if word[i] in self.noMoreInSolution and not (word[i] in self.misplacedLetters) and not (self.solution[i] == word[i]):
                        valid = False
                        break
                    # if this word has a letter in a wrong position that was already guessed
                    if i in self.inSolution[word[i]]:
                        valid = False
                        break
                    # if this position is in the solution the guessword should match
                    if self.solution[i] != self.LTR_WRONG and self.solution[i] != word[i]:
                        valid = False
                        break
                # ensure all misplaced letters are in the word
                for c in self.misplacedLetters:
                    if not c in word:
                        valid = False
                if valid:
                    self.lastGuessed = word
                    return word
                else:
                    self.words.remove(word)
        # all guesses have been exhausted
        return "This wordle is unkown"