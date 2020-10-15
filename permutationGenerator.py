import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from morphAdorner2 import pluralizer, conjugator
lemmatizer = WordNetLemmatizer()
import sqlite3

testInput = "Approve Capital Project Expenses"

conn = sqlite3.connect('wordTree.db')
c = conn.cursor()
# RUN IF NO DATABASE IS CURRENTLY PRESENT
# c.execute("""CREATE TABLE wordTree ( rootWord text, branchWords text )""")


# Cleans input string and separates words into a word list
def cleaner(string):
    removeChars = [":", ",", ".", "-", "–", ";", "(", ")", "‘", "’", "&"]

    cleanString = string.lower()

    for char in removeChars:
        cleanString = cleanString.replace(char, "")
    cleanString = cleanString.replace("/", " ")

    # remove empty string list entries
    cleanStringList = list(filter(None, cleanString.split(" ")))

    return cleanStringList


# Returns a dictionary containing the rootword and a list for parts-of-speech
def get_root_words(string):
    wordList = cleaner(string)
    rootWordList = []

    for word in wordList:
        rootWord = lemmatizer.lemmatize(word)                   # nltk's best guess as to what the rootWord is
        posSet = set()                                          # Set for Parts-Of-Speech
        for synset in wordnet.synsets(rootWord):                # List of synonyms for the rootWord as synset Objects
            synsetComponents = synset.name().split(".")         # Synset("process.n.01").name() = process.n.01
            if synsetComponents[0] == rootWord:
                posSet.add(synsetComponents[1])                 # Add POS for the word
        if not posSet:                                          # If the set is empty
            posSet.add("n")     # If no match, we are going to assume that the word is a noun
        if not any(rootWord in Entry["rootWord"]
                   for Entry in rootWordList):                  # Checks if root word is in rootWordList
            rootWordList.append({"rootWord": rootWord, "wordType": list(posSet)})

    return rootWordList


# Inserts the root word and a comma-delimited string of branch words into the database
def insert_word(root_word, branch_word_list):
    branchWordString = ",".join(branch_word_list)
    with conn:
        c.execute("INSERT INTO wordTree VALUES (:rootWord, :branchWords)",
                  {"rootWord": root_word, "branchWords": branchWordString})
    print(f"Root Word - {root_word} - has been added to the database with Branch Words - {branchWordString}")


# Returns a list containing a 2-entry tuple of the root word and a comma-delimited string of branch words.
# Returns an empty list if no matches are found for the root word.
def get_branch_words(root_word):
    c.execute("SELECT * FROM wordTree WHERE rootWord=:rootWord", {"rootWord": root_word})

    return c.fetchall()


# Applies the conjugator() or pluralizer() functions depending on whether the word added is a noun or a verb
def noun_verb(root_word, function, foreign_word):
    # retrieves the comma-delimited string of branch words from the database
    branchWords = get_branch_words(root_word)
    # if the root_word is not in the database
    if not branchWords:
        foreign_word = True
        newBranchWordsList = function(root_word)
        return newBranchWordsList, foreign_word
    else:
        branchWordsList = branchWords[0][1].split(",")
    return branchWordsList, foreign_word


def get_variations_list(sentence):
    root_wordList = get_root_words(sentence)
    variationsList = []

    for entry in root_wordList:
        if not "n" and "v" in entry["wordType"]:
            variationsList.append(entry["rootWord"])
        else:
            foreignWord = False
            nounBranchList = []
            verbBranchList = []
            if "n" in entry["wordType"]:
                nounBranchList, foreignWord = noun_verb(entry["rootWord"], pluralizer, foreignWord)
                variationsList += nounBranchList
            if "v" in entry["wordType"]:
                verbBranchList, foreignWord = noun_verb(entry["rootWord"], conjugator, foreignWord)
                variationsList += verbBranchList
            if foreignWord:
                insert_word(entry["rootWord"], list(set(nounBranchList + verbBranchList)))

    return list(set(variationsList))


if __name__ == "__main__":
    print(get_root_words(testInput))
    print(get_variations_list(testInput))
