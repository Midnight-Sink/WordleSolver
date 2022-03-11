from model import WordleSolver

wordsPath = "Data/wordle.txt"
scoresPath = "Data/commonScores.txt"
usedPath = "Data/pastWords.txt"

print("========== WORDLE SOLVER ==========")
solver = WordleSolver(wordsPath, usedPath, scoresPath, 5)
print("Keys: ")
print("?: Character is not in the wordle")
print("*: Character is in the wordle")
print("!: Character is in the wordle in the right spot")
print("Guess 1: "+solver.lastGuessed)

for i in range(4):
    mask = input("Enter the response mask: ")
    
    if len(mask) != 5:
        # assume quit
        quit()
    if mask == "!!!!!":
        # word is correct
        print("Guess is correct!")
        quit()

    print("Guess " + str(i + 2) + ": "+solver.tryNext(mask))

print("Out of attempts, quitting...")

    