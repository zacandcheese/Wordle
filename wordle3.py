from string import ascii_lowercase as alphabet
from random import choice
from itertools import permutations
from tqdm import tqdm
from heapq import *

#word_list = ["happy", "spire", "point", "print", "doggy"]
# -------------- 
# Load Documents
# --------------
word_list = set()
with open("words.txt", "r") as f:
    data = f.read().split()
    word_list = set(data)
    f.close()

exclude_words = set()
with open("exclude.txt", "r") as f:
    data = f.read().replace("\n", " ").split()
    exclude_words = set(data)
    f.close()

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

def wordle(green, yellow, guesses):
    # ---------------------------------------------------------
    # Elimate Words because they include/don't include a letter
    # ---------------------------------------------------------
    #green = "*ro*e"
    #yellow = "t" # set of characters
    #guesses = ["raise", "court", "trope"]
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

    for char in set(yellow).intersection(set(green)): # Remove Doubles
        i = ord(char) - ord('a')
        doubles = set()
        for idx in range(5):
            for idx2 in range(idx+1, 5):
                temp = position_sets[idx][i].intersection(positions_sets[idx2][i])
                doubles = doubles.union(temp)
        words_left = words_left.intersection(doubles)

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



    # ------------------
    # Find the Best Word
    # ------------------
    best_word = []
    best_score = float('inf') 


    set_of_words = all_words
    if move > 1:
        set_of_words = words_left



    temp = "000001111122222"
    all_scores = []
    heapify(all_scores)

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
        
        # ------------------
        # Keep Track of Best
        # ------------------
        if (len(all_scores) < 10):
            heappush(all_scores, (-1*score, word))
        elif (-1* score > all_scores[0][0]):
            heapreplace(all_scores, (-1*score, word))

        if (score < best_score):
            best_word = [word]
            best_score = score
        elif (score == best_score):
            best_word.append(word)

    print(f"----------------------------------\nTHE BEST WORD: {choice(best_word)} \nExpected Number of Returns: {best_score/len(words_left)}\n----------------------------------")
    print("Equivalent Words: ", best_word)
    print("Other Options: ", list(map(lambda x: ("{:.2f}".format(-1*x[0] / len(words_left)), x[1]), all_scores)))
    if (len(words_left) < 20):
        print("Words Left: ", words_left)
