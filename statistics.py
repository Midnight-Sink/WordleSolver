dataPath = "Data/"

commonLetters = {}
for i in range(97, 123):
    commonLetters[i] = []
    for j in range(5):
        commonLetters[i].append(0)

# File Processing
totalWords = 0
words = {}
wordFile = open(dataPath+"wordle.txt", "r")
for word in wordFile:
    totalWords+=1
    word = word.lower().rstrip()
    words[word] = 0
    for i in range(5):
        commonLetters[ord(word[i])][i] += 1
wordFile.close()

# scoreFile = open(dataPath+"commonScores.txt", "r")
# i = 0
# for score in scoreFile:
#     words[list(words.keys())[i]] = int(score)
#     i+=1
# scoreFile.close()

# Other Processing
scores = {}
for word in words.keys():
    score = 0
    for i in range(5):
        score += commonLetters[ord(word[i])][i]
    scores[word] = words[word] + score
scores = sorted(scores, key=scores.get, reverse=True)

# Output
print("Total Words: "+str(totalWords))
for i in range(97, 123):
    print(chr(i) + ": [", end='')
    commonSum = 0
    for j in range(5):
        n = 100*commonLetters[i][j]/totalWords
        commonSum+=n
        print(str(round(n, 2)), end=', ')
    print("] "+str(round(commonSum, 2)))

print(scores[:10])

while True:
    guess = input("Give a word to score: ")
    if len(guess) != 5:
        quit()
    sum = 0
    for i in range(5):
        sum += commonLetters[ord(guess[i])][i]
    print(sum)