from os import listdir

# Calculate how common a 5 letter word is in use
totalWords = 0
words = {}
wordFile = open("sgb-words.txt", "r")
for word in wordFile:
    word = word.rstrip()
    totalWords+=1
    words[word] = 0
wordFile.close()

filesToRead = listdir("Text")
for f in filesToRead:
    file = open("Text/"+f, "r", encoding="utf8")
    for line in file:
        line = line.rstrip().lower()
        tokens = line.split()
        for t in tokens:
            if t in words:
                words[t] += 1
    file.close()

out = open("commonScores.txt", "w")
for w in words:
    out.write(str(words[w])+"\n")
out.close()
