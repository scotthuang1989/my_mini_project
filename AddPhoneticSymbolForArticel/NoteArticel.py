import re
import sqlite3
import os
import nltk
from AddPhoneticSymbolForArticel import youdao
import os

modulePath=os.path.dirname(__file__)

DB_NAME = os.path.join(modulePath,'database.db')

# symbol_data_base = None
# db_cur = None

#if update punctuation and space list, please update the regular express accordingly
# list of punctuation
punctuation_list = [r'\n','.','!',',']
#list of space
space_list=[' ']


def main():
    # Read article file
    try:
        fh = open(os.path.join(modulePath,"article.txt"), 'r',encoding='UTF-8')
        content = fh.read()
    except Exception as ex:
        print("Read article error: " + str(ex))

    # Connect to database
    if not os.path.isfile(DB_NAME):
        # database don't exist
        # 1. create table
        symbol_data_base = sqlite3.connect(DB_NAME)
        db_cur = symbol_data_base.cursor()
        db_cur.execute('''CREATE TABLE English_Symbol (word text primarykey,symbol text)''')
    else:
        symbol_data_base = sqlite3.connect(DB_NAME)
        db_cur = symbol_data_base.cursor()

    # word_list = re.findall(r"\b\w+\b",content)
    # todo: punctuation list is not complete. finalize it over time.
    # word_list = re.findall(r"[a-zA-z’']+|[\n,!.]|[\s]",content)
    # print(word_list)
    # use nltk to extract word.
    word_list=nltk.word_tokenize(content)
    noted_article = ""
    word_count = 0
    last_is_space = False
    for word in word_list:
        if word in punctuation_list:
            last_is_space = False
            noted_article += word
            continue
        if word in space_list:
            if not last_is_space:
                noted_article += word
                last_is_space = True
            continue
        word_tuple = (word,)
        select_result = db_cur.execute(
            "SELECT * FROM English_Symbol WHERE word = ?",
            word_tuple).fetchone()
        noted_article += " "
        noted_article += word
        # word_count += 1
        # if word_count % 10 == 0:
        #     noted_article += "\r\n"
        if not (select_result is None):
            symbol = select_result[1]
            # print("Found in database: ",word)
            noted_article += " "
            noted_article += "("+symbol+")"
            continue
        symbol = youdao.CheckSymbolFromYoudao(word)
        # print("symbol is:",symbol)
        # print("Get from network: ", word)
        if symbol:
            noted_article += " "
            noted_article += symbol
            db_cur.execute("INSERT INTO English_Symbol VALUES (?,?)", (word, symbol ) )
            print("Insert To database")
        else:
            db_cur.execute("INSERT INTO English_Symbol VALUES (?,?)", (word, "" ) )
            print("Insert To database: with null")
    noted_fh = open("output.txt", 'w',encoding="UTF-8")
    noted_fh.write(noted_article)
    noted_fh.close()
    # clean up database
    symbol_data_base.commit()
    symbol_data_base.close()

if __name__ == '__main__':
    main()
