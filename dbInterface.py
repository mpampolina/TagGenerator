import sqlite3

conn = sqlite3.connect('wordTree.db')
c = conn.cursor()


def insert_word(root_word, branch_word_list):
    branchWordString = ",".join(branch_word_list)
    with conn:
        c.execute("INSERT INTO wordTree VALUES (:rootWord, :branchWords)",
                  {"rootWord": root_word, "branchWords": branchWordString})
    print(f"Root Word - {root_word} - has been added to the database with Branch Words - {branchWordString}")


def get_branch_words(root_word):
    c.execute("SELECT * FROM wordTree WHERE rootWord=:rootWord", {"rootWord": root_word})

    return c.fetchall()


def change_branch_words(root_word, branch_word_list):
    branchWordString = ",".join(branch_word_list)
    with conn:
        c.execute("""UPDATE wordTree SET branchWords=:branchWords
        WHERE rootWord=:rootWord""", {"rootWord": root_word, "branchWords": branchWordString})
    print(f"Root Word - {root_word} - has been updated in the database with Branch Words - {branchWordString}")


def delete_root_word_entry(root_word):
    with conn:
        c.execute("DELETE from wordTree WHERE rootWord=:rootWord", {"rootWord": root_word})


if __name__ == "__main__":
    # EDIT THE DATABASE FROM HERE
    print(get_branch_words("to"))
    # functionWords = ["the", "a", "of", "at", "how", "to"]
    # for word in functionWords:
    #     insert_word(word, [word])






