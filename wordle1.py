from nltk.corpus import words
word_list = words.words()
print(len(word_list))
from string import ascii_lowercase as alphabet
from random import choice
#word_list = ["happy", "spire", "point", "print", "doggy"]

exclude_words = set(["essie", "assis", "braham", "beman", "humbo", "biham", "unhot", "domer", "rexen", "reneg", "breek", "neger", "reese", "meece", "meese", "hamel", "esere", "pombo", "wramp", "whamp", "scind", "teasy", "casey", "smoos", "byron", "myron", "benda", "buddh", "dubhe", "bolti", "serta", "tarse", "chiot", "islot", "cordy", "todus", "bibio", "samir", "tarin", "ranty", "coony", "boily", "coiny", "doigt", "piotr", "moity", "raiae", "sairy", "barie", "tarie", "sinae", "sadie", "saite", "aueto", "aoife", "kioea", "heiau", "ouabe", "toity", "conoy", "solea"])
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
green = "****e"
yellow = "is" # set of characters
guesses = ["arise"]
words_left = all_words
move = 3#len(guesses)


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

tuples = [[set() for _ in range(26)] for _ in range(26)]
for i in range(26):
    for j in range(i, 26):
        tuples[i][j] = letters_in_word[i]
        tuples[i][j] = tuples[i][j].intersection(letters_in_word[j])


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
print(len(tuples[0][1]))
best_word = []
best_score = float('inf') 
best_tie_score = float('inf')

set_of_words = all_words
if move > 1:
    set_of_words = words_left

for word in set_of_words: #words_left or all_words
    score = 0

    # How many will remain if I only get one letter?
    for pos, char in enumerate(word):
        if (green[pos] == char or char in yellow):
            continue
        others = word[:pos] + "*" + word[pos+1:]
        i = ord(char) - ord("a")
        worst_case_y = letters_in_word[i] # Yellow
        worst_case_g = positions_in_word[pos][i] # Green
        worst_case_y = worst_case_y.difference(worst_case_g)
        for pos2, char2 in enumerate(others):
            if (green[pos2] == char2 or char2 in yellow or char2 == "*"):
                continue
            j = ord(char2) - ord("a")
            worst_case_y = worst_case_y.difference(letters_in_word[j])
            worst_case_g = worst_case_g.difference(letters_in_word[j])
        if ((len(worst_case_y) + len(worst_case_g)) == 0):
            continue
        temp_score = (len(worst_case_y)**2  + len(worst_case_g)**2) / (len(worst_case_y) + len(worst_case_g))  
        score += temp_score
    
    # How many will remain if I only get two yellows?
    temp = sorted(enumerate(word), key=lambda x: x[1])
    for idx, (pos, char) in enumerate(temp):
        if (green[pos] == char or char in yellow):
            continue

        for idx2 in range(idx+1, len(temp)):
            (pos2, char2) = temp[idx2]
            if (green[pos2] == char2 or char2 in yellow):
                continue
            i = ord(char) - ord("a")
            j = ord(char2) - ord("a")
            worst_case = tuples[i][j]

            others = word[:pos]    + "*" + word[pos+1:]
            others = others[:pos2] + "*" + others[pos2+1:]
            for pos3, char3 in enumerate(others):
                if (green[pos3] == char3 or char3 in yellow or char3 == "*"):
                    continue
                k = ord(char3) - ord("a")
                worst_case = worst_case.difference(letters_in_word[k])
            score += len(worst_case)**2
   
    # How many will remain if I get 3 yellows?

    # How many will remain if I get 4 yellows?

    # How many will remain if I get no letters?
    temp_set = set()
    for pos, char in enumerate(word):
        if (char == green[pos] or char in yellow):
            continue
        i = ord(char) - ord("a")
        temp_set = temp_set.union(letters_in_word[i])
    no_hit = len(words_left) - len(temp_set)
    
    score += no_hit**2
    if (score == 0): # uses all known words FIXME
        continue

    # Keep Track of Best
    if (score < best_score):
        best_word = [word]
        best_score = score
    elif (score == best_score):
        best_word.append(word)

print(best_word, best_score)
print(choice(best_word))
if (len(words_left) < 20):
    print(words_left)
