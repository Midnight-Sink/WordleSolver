from model import WordleSolver

# simulate the entire game and try to guess every word

wordsPath = "Data/wordle.txt"

words = []
wordFile = open(wordsPath)
for word in wordFile:
    words.append(word.lower())
usedWords = []
wordFile.close()

def compareWord(guess, ans):
    mask = list("?????")
    for i in range(5):
        if guess[i] == ans[i]:
            mask[i] = '!'
        elif guess[i] in ans:
            mask[i] = '*'
    return "".join(mask)

ngames = 0
scores = 0
nwon = 0
typeScores = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}

for word in words:
    solver = WordleSolver(wordsPath, usedWords, 5)
    won = False
    for i in range(6):
        mask = compareWord(solver.lastGuessed, word)
        
        if mask == "!!!!!":
            # the game is finished, log stats
            scores += i+1
            typeScores[i+1] += 1
            nwon += 1
            #print(word+": "+str(i))
            won = True
            break

        solver.tryNext(mask)
    if not won:
        print(word)
        typeScores[7] += 1
        scores += 7

    ngames+=1
    usedWords.append(word)

print("games: "+str(ngames))
print("games won: "+str(nwon))
print("lost: "+str(ngames - nwon))
print("win %: "+str(nwon/ngames))
print("avg score: "+str(scores/nwon))
for i in range(7):
    print(str(i+1)+": "+str(typeScores[i+1]))
    print(str(i+1)+": "+str(typeScores[i+1]/ngames))
