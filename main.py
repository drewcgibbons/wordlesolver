from Tile import Tile
import re
import pandas as pd
from db import run_query
from guessed_letter_map import guessed_letters as letter_map
from guessed_letter_map import impossible_letters as impossible_map

def run(num_recs):
    board = []
    for i in range(0,5):
        board.append(Tile())

    guesses = 1
    occupied_indices = []
    
    match_arr = ['N', 'N', 'N', 'N', 'N']
    word_match_arr = ['N', 'N', 'N', 'N', 'N']

    while guesses <= 6:
        print("Guess #" + str(guesses))
        print("Enter guess")
        guessed_str = input()
        guessed_arr = [*(guessed_str.upper())]
        # Eliminate guessed word

        print("Enter matches. G for green, Y for yellow, N for no match")
        match_str = input()
        match_arr = [*(match_str.upper())]

        if match_arr == ['G', 'G', 'G', 'G', 'G']:
            print("Correct Answer!")
            exit()

        # print(match_arr)

        eliminate_missed_letters(match_arr, guessed_arr, occupied_indices)

        # Update board
        board = update_board(board, match_arr, guessed_arr)

        # Eliminate letters missed from map
        suggestions = get_suggestions(board, num_recs, occupied_indices)

        print(suggestions)

        guesses += 1

def eliminate_missed_letters(match, guess, occ_ix):
    for guess_letter, match_letter, i in zip(guess, match, list(range(0, len(guess)))):
        if match_letter.upper() == "N" and letter_map[guess_letter] == 0:
            letter_map[guess_letter] = -1

        if match_letter.upper() == "N" and impossible_map[guess_letter] == 0:

            if not isinstance(impossible_map[guess_letter], set):
                impossible_map[guess_letter] = {i}
            else:
                impossible_map[guess_letter].add(i)
        
        elif match_letter.upper() == "G": 
            if letter_map[guess_letter] == 0:
                letter_map[guess_letter] = {i}
            else:
                # print(guess_letter)
                # print(i)

                if not isinstance(letter_map[guess_letter], set):
                    letter_map[guess_letter] = {i}
                letter_map[guess_letter].add(i)
                occ_ix.append(i)
    
        elif match_letter.upper() == "Y":
            potential_indices_set = {0,1,2,3,4}
            occ_ix_set = set(occ_ix)
            potential_indices_set = potential_indices_set - occ_ix_set - {i}
            letter_map[guess_letter] = potential_indices_set
            
            if not isinstance(impossible_map[guess_letter], set):
                impossible_map[guess_letter] = {i}
            else:
                impossible_map[guess_letter].add(i)
    print(impossible_map)
    print(letter_map)

def update_board(board, match_arr, guessed_arr):
    for tile, match, guess in zip(board, match_arr, guessed_arr):
        if match == 'G':
            tile.set_correct_place(True)
            tile.set_in_word(True)
            tile.set_char(guess)
        elif match == 'Y':
            tile.set_correct_place(False)
            tile.set_in_word(True)
            tile.set_char(guess)

    return board

def get_suggestions(board, num_suggestions, occ_ix):
    base_sql = "select * from english.five_letter_words "
    
    like_str = ""

    # build like string with wildcards
    for tile in board:
        if tile.get_correct_place() is True:
            like_str = like_str + tile.get_char().lower()
        # elif tile.get_in_word is True and tile.get_correct_place is False:
        #     pass
        #     #TODO: filter potential words based on this
        #     # f
        else:
            like_str = like_str + "[a-z]"

    query = base_sql + "WHERE word REGEXP \'" + like_str + "\' order by frequency desc limit " + str(num_suggestions)

    df = run_query(query)

    df = remove_eliminated_letters(df, board, occ_ix)

    return df
    

def remove_eliminated_letters(df, board, occ_ix):

    # Permanently changes the pandas settings
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    ix_list = []
    # print(letter_map)
    for letter in letter_map:
        if letter_map[letter] == -1:
            for word in df['Word']:
                if word.__contains__(letter.lower()):
                    ix = df[df['Word'] == word.lower()].index
                    ix_list.append(ix[0])
        
        elif letter_map[letter] != 0:
            # print(letter)
            for word in df['Word']:
                valid = False
                # print(letter_map)
                # print(letter_map[letter])
                for ix in letter_map[letter]:
                    if word[ix].lower() == letter.lower():
                        # print(word)
                        valid = True
                
                if valid == False:
                    ix = df[df['Word'] == word.lower()].index
                    ix_list.append(ix[0])
                
                valid = True

                if (isinstance(impossible_map[letter], set)):
                    for ix in impossible_map[letter]:
                        if word[ix].lower() == letter.lower():
                            # print(word)
                            valid = False
                            break
                    
                    if valid == False:
                        ix = df[df['Word'] == word.lower()].index
                        ix_list.append(ix[0])

    df = df.drop(df.index[ix_list])
    
    return df

if __name__ == "__main__":
    run(num_recs= 5000)
