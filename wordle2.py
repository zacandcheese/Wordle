from nltk.corpus import words
word_list = words.words()
print(len(word_list))
from string import ascii_lowercase as alphabet
from random import choice
#word_list = ["happy", "spire", "point", "print", "doggy"]

exclude_words = set(["dhoul", "essie", "assis", "braham", "beman", "humbo", "biham", "unhot", "domer", "rexen", "reneg", "breek", "neger", "reese", "meece", "meese", "hamel", "esere", "pombo", "wramp", "whamp", "scind", "teasy", "casey", "smoos", "byron", "myron", "benda", "buddh", "dubhe", "bolti", "serta", "tarse", "chiot", "islot", "cordy", "todus", "bibio", "samir", "tarin", "ranty", "coony", "boily", "coiny", "doigt", "piotr", "moity", "raiae", "sairy", "barie", "tarie", "sinae", "sadie", "saite", "aueto", "aoife", "kioea", "heiau", "ouabe", "toity", "conoy", "solea"])
# ----------------
# Preprocess Words
# ----------------
list_of_sets = [set() for _ in range(26)]
position_sets = [[set() for _ in range(26)] for _ in range(5)]
all_words = set()
for word in word_list:
    if (len(word) != 5 or not word.isalpha()):
        continue
    word = word.lower()
    all_words.add(word)
    for pos, char in enumerate(word):
        i = ord(char) - ord("a")
        if (i < 0 or i > 25):
            print(i, char, word)
        list_of_sets[i].add(word)
        position_sets[pos][i].add(word)

all_words = all_words.difference(exclude_words)
# ---------------------------------------------------------
# Elimate Words because they include/don't include a letter
# ---------------------------------------------------------
green = "*****"
yellow = "re" # set of characters
guesses = ["raise"]
words_left = all_words
move = len(guesses)


for pos,char in enumerate(green):
    if (char != "*"):
        i = ord(char) - ord("a")
        words_left = position_sets[pos][i].intersection(words_left)

for char in yellow:
    i = ord(char) - ord("a")
    words_left = words_left.intersection(list_of_sets[i])

for word in guesses:
    for pos, char in enumerate(word):
        i = ord(char) - ord("a")

        if (char in yellow and char != green[pos]):
            words_left = words_left.difference(position_sets[pos][i])

        elif (char in green and char != green[pos]):
            words_left = words_left.difference(position_sets[pos][i])

        elif (not char in green and not char in yellow):
            words_left = words_left.difference(list_of_sets[i])

print("words_left: ", len(words_left))

# -----------------
# Postprocess Words
# -----------------
letters_in_word = [set() for _ in range(26)] #The main one
positions_in_word = [[set() for _ in range(26)] for _ in range(5)] #The tiebreak
for word in words_left:
    for pos, char in enumerate(word):
        i = ord(char) - ord("a")
        letters_in_word[i].add(word)
        positions_in_word[pos][i].add(word)


# REMOVE DOUBLES
for char in set(yellow).intersection(set(green)):
    i = ord(char) - ord('a')
    doubles = set()
    for idx in range(5):
        for idx2 in range(idx+1, 5):
            temp = positions_in_word[idx][i].intersection(positions_in_word[idx2][i])
            doubles = doubles.union(temp)
    words_left = words_left.intersection(doubles)

# ------------------
# Find the Best Word
# ------------------
best_word = []
best_score = float('inf') 



set_of_words = all_words
if move > 1:
    set_of_words = words_left



from itertools import permutations
from tqdm import tqdm
temp = "000001111122222"
for word in tqdm(set_of_words):
    ternary = permutations(temp, 5)
    outcomes = []
    for p in set(ternary):

        worst_case = words_left
        for pos, action in enumerate(p):
            action = int(action)
            char = word[pos]
            i = ord(char) - ord('a')
            if (action == 0):
                # Black
                worst_case = worst_case.difference(letters_in_word[i])
            elif (action == 1):
                # Green
                worst_case = worst_case.intersection(positions_in_word[pos][i])
            else:
                # Yellow (NOT GREEN)
                yellow_words = letters_in_word[i].difference(positions_in_word[pos][i])
                worst_case = worst_case.intersection(yellow_words)
        outcomes.append(len(worst_case)**2)
    score = sum(outcomes)

    # Keep Track of Best
    if (score < best_score):
        best_word = [word]
        best_score = score
    elif (score == best_score):
        best_word.append(word)

print(f"----------------------------------\nTHE BEST WORD: {choice(best_word)} \nExpected Number of Returns: {best_score/len(words_left)}\n----------------------------------")
print(best_word)
if (len(words_left) < 20):
    print(words_left)
