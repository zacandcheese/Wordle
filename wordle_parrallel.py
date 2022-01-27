from string import ascii_lowercase as alphabet
from itertools import permutations


words = set()
words_left = set()
set_of_words = set()
list_of_sets = [set() for _ in range(26)]
position_sets = [[set() for _ in range(26)] for _ in range(5)]

green = ""
yellow = ""
guesses = []
move = 0

letters_in_word = [set() for _ in range(26)]
positions_in_word = [[set() for _ in range(26)] for _ in range(5)]
yellow_in_word = [[set () for _ in range(26)] for _ in range(5)]

def set_context(grn, ylw, gss):
	global green
	green = grn
	global yellow
	yellow = ylw
	global guesses
	guesses = gss
	global move
	move = len(gss)

def set_words():
# -------------- 
# Load Documents
# --------------
	#print("Load Documents")
	word_set = set()
	with open("words.txt", "r") as f:
    		data = f.read().split()
    		word_set = set(data)
    		f.close()

	exclude_words = set()
	with open("exclude.txt", "r") as f:
    		data = f.read().replace("\n", " ").split()
    		exclude_words = set(data)
    		f.close()

# ----------------
# Preprocess Words
# ----------------
	#print("Preprocess Words")
	global list_of_sets
	global position_sets
	all_words = set()
	for word in word_set:
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
	global words
	words = word_set.difference(exclude_words)

# ---------------------------------------------------------
# Eliminate Words because they include/don't include a letter
# ---------------------------------------------------------
	#print("Eliminate Words")
	global words_left
	words_left = words
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
	global set_of_words
	set_of_words = list(words)
	if move > 1:
                set_of_words = list(words_left)
	print("words_left: ", len(words_left))


# -----------------
# Postprocess Words
# -----------------
	global letters_in_word
	global positions_in_word
	for word in words_left:
    		for pos, char in enumerate(word):
        		i = ord(char) - ord("a")
        		letters_in_word[i].add(word)
        		positions_in_word[pos][i].add(word)

	global yellow_in_word
	for i in range(26):
    		for pos in range(5):
        		temp_yellow_words = letters_in_word[i].difference(positions_in_word[pos][i])
        		yellow_in_word[pos][i] = temp_yellow_words

def join_sets(i_sets, d_sets):
    global words_left
    i_sets.sort(key=lambda x: len(x))
    if len(i_sets) > 0:
        start = i_sets[0]
        for d in d_sets:
            start = start.difference(d)
        for i in i_sets[1:]:
            start = start.intersection(i)
    else:
        start = words_left
        for d in d_sets:
            start = start.difference(d)
        for i in i_sets[1:]:
            start = start.intersection(i)
    return len(start) ** 2

def compute_score(word):
    temp = "000001111122222"
    ternary = permutations(temp, 5)
    outcomes = []
    global words_left
    for p in set(ternary):
        worst_case = words_left
        i_sets = []
        d_sets = []
        for pos, action in enumerate(p):
            action = int(action)
            char = word[pos]
            i = ord(char) - ord('a')
            if (action == 0):
                # Black
                d_sets.append(letters_in_word[i])
            elif (action == 1):
                # Green
                i_sets.append(positions_in_word[pos][i])
            else:
                # Yellow (NOT GREEN)
                yellow_words = yellow_in_word[pos][i]
                i_sets.append(yellow_words)
        
        outcomes.append(join_sets(i_sets, d_sets))
    score = sum(outcomes)
    return (score / len(words_left), word)

# MULTIPROCESSING DATA #

def get_set_of_words():
    global set_of_words
    return set_of_words

