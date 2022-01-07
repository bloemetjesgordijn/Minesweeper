from selenium import webdriver
import time
import random
import essentials
import pandas as pd
import numpy as np

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome() # Target browser
driver.get('https://minesweeper.online')

mode = "Beginner"
boardID = 'A43'
modeClass = ''
moves = 0
width = 0
height = 0
board = 0
board_df = 0
finished = False
moved = False
did_second_corner = False

def select_game_mode(mode):
    global width
    global height
    if mode == "Beginner":
        print('Mode: Beginner')
        width = 9
        height = 9
        modeClass = 'homepage-level-1'
    elif mode == "Intermediate":
        print('Mode: Intermediate')
        width = 16
        height = 16
        modeClass = 'homepage-level-2'
    elif mode == "Expert":
        print('Mode: Expert')
        width = 30
        height = 16
        modeClass = 'homepage-level-3'
    else: 
        print('dont understand mode')
    
    if essentials.check_exists_by_class_name(driver, modeClass):
        print("found button for mode", mode)
        mode_btn = driver.find_element_by_class_name(modeClass)
        mode_btn.click()
    else:
        print('Did not find button ', modeClass, 'for mode', mode)
            
def get_board():
    global board
    b = True
    while b:
        if essentials.check_exists_by_id(driver, boardID):
            b = False
            board = driver.find_element_by_id(boardID)
            print('Found board', boardID, '!')
        else:
            print("Searching for board", boardID, '...')
    
def analyze_board():
    global board_df
    board_df = pd.DataFrame(index=range(height + 2),columns=range(width + 2))
    for x in range(height):
        for y in range(width):
            currID = 'cell_' + str(y) + '_' + str(x)
            currEL = board.find_element_by_id(currID)
            currClassName =  currEL.get_attribute("class")
            i = x + 1
            j = y + 1
            if currClassName == 'cell size24 hd_closed':
                board_df.iloc[i,j] = "X"
            elif currClassName == 'cell size24 hd_opened hd_type0':
                board_df.iloc[i,j] = '0'
            elif currClassName == 'cell size24 hd_opened hd_type1':
                board_df.iloc[i,j] = '1'
            elif currClassName == 'cell size24 hd_opened hd_type2':
                board_df.iloc[i,j] = '2'
            elif currClassName == 'cell size24 hd_opened hd_type3':
                board_df.iloc[i,j] = '3'
            elif currClassName == 'cell size24 hd_opened hd_type4':
                board_df.iloc[i,j] = '4'
            elif currClassName == 'cell size24 hd_opened hd_type5':
                board_df.iloc[i,j] = '5'
            elif currClassName == 'cell size24 hd_opened hd_type6':
                board_df.iloc[i,j] = '6'
            elif currClassName == 'cell size24 hd_opened hd_type7':
                board_df.iloc[i,j] = '7'
            elif currClassName == 'cell size24 hd_opened hd_type8':
                board_df.iloc[i,j] = '8'
            elif currClassName == 'cell size24 hd_opened hd_type10':
                board_df.iloc[i,j] = 'BOMB'
            elif currClassName == 'cell size24 hd_opened hd_type11':
                board_df.iloc[i,j] = 'BOMB'
            elif currClassName == 'cell size24 hd_closed hd_flag':
                board_df.iloc[i,j] = 'FLAG'
    # print("==== CURRENT BOARD ====")
    # print(board_df)
    # print("=======================")

def first_move(x, y):
    # get_board()
    squareID = 'cell_' + str(y) + '_' + str(x)
    if essentials.check_exists_by_id(board, squareID):
        square = board.find_element_by_id(squareID)
        square.click()
        analyze_board()

def check_flags(i,j):
    flag_count = 0
    if board_df.iloc[i-1,j-1] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i-1,j] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i-1,j+1] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i,j-1] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i,j+1] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i+1,j-1] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i+1,j] == 'FLAG':
        flag_count += 1
    if board_df.iloc[i+1,j+1] == 'FLAG':
        flag_count += 1
    return flag_count

def check_X(i,j):
    X_count = 0
    if board_df.iloc[i-1,j-1] == 'X':
        X_count += 1
    if board_df.iloc[i-1,j] == 'X':
        X_count += 1
    if board_df.iloc[i-1,j+1] == 'X':
        X_count += 1
    if board_df.iloc[i,j-1] == 'X':
        X_count += 1
    if board_df.iloc[i,j+1] == 'X':
        X_count += 1
    if board_df.iloc[i+1,j-1] == 'X':
        X_count += 1
    if board_df.iloc[i+1,j] == 'X':
        X_count += 1
    if board_df.iloc[i+1,j+1] == 'X':
        X_count += 1
    return X_count

def locate_bomb(i,j):
    if board_df.iloc[i-1,j-1] == 'X':
        mark_bomb(i-1,j-1)
    if board_df.iloc[i-1,j] == 'X':
        mark_bomb(i-1,j)
    if board_df.iloc[i-1,j+1] == 'X':
        mark_bomb(i-1,j+1)
    if board_df.iloc[i,j-1] == 'X':
        mark_bomb(i,j-1)
    if board_df.iloc[i,j+1] == 'X':
        mark_bomb(i,j+1)
    if board_df.iloc[i+1,j-1] == 'X':
        mark_bomb(i+1,j-1)
    if board_df.iloc[i+1,j] == 'X':
        mark_bomb(i+1,j)
    if board_df.iloc[i+1,j+1] == 'X':
        mark_bomb(i+1,j+1)

def mark_bomb(i,j):
    x = i - 1
    y = j - 1
    squareID = 'cell_' + str(y) + '_' + str(x)
    if essentials.check_exists_by_id(board, squareID):
        square = board.find_element_by_id(squareID)
        squareClassName =  square.get_attribute("class")
        if squareClassName != 'cell size24 hd_closed hd_flag':
            action = ActionChains(driver)
            print('Mark',x,y)
            action.context_click(square).perform()
            moved = True
            analyze_board()
        else:
            print('Already marked flag')

def locate_all_squares(i,j):
    if board_df.iloc[i-1,j-1] == 'X':
        click_square(i-1,j-1)
    if board_df.iloc[i-1,j] == 'X':
        click_square(i-1,j)
    if board_df.iloc[i-1,j+1] == 'X':
        click_square(i-1,j+1)
    if board_df.iloc[i,j-1] == 'X':
        click_square(i,j-1)
    if board_df.iloc[i,j+1] == 'X':
        click_square(i,j+1)
    if board_df.iloc[i+1,j-1] == 'X':
        click_square(i+1,j-1)
    if board_df.iloc[i+1,j] == 'X':
        click_square(i+1,j)
    if board_df.iloc[i+1,j+1] == 'X':
        click_square(i+1,j+1)

def click_square(i,j):
    x = i - 1
    y = j - 1
    squareID = 'cell_' + str(y) + '_' + str(x)
    if essentials.check_exists_by_id(board, squareID):
        square = board.find_element_by_id(squareID)
        squareClassName =  square.get_attribute("class")
        if squareClassName == 'cell size24 hd_closed':
            print('Click',x,y)
            square.click()
            moved = True
            analyze_board()
        else:
            print('Error clicking square')

def calc_move():
    global did_second_corner
    board_df_copy = board_df.copy()
    for i in range(height):
        for j in range(width):
            if board_df.iloc[i,j] == '1':
                TotalCount = check_flags(i,j) + check_X(i,j)
                if TotalCount == 1:
                    locate_bomb(i,j)
                elif TotalCount > 1:
                    if check_flags(i,j) == 1:
                        locate_all_squares(i,j)
            if board_df.iloc[i,j] == '2':
                TotalCount = check_flags(i,j) + check_X(i,j)
                if TotalCount == 2:
                    locate_bomb(i,j)
                elif TotalCount > 2:
                    if check_flags(i,j) == 2:
                        locate_all_squares(i,j)
            if board_df.iloc[i,j] == '3':
                TotalCount = check_flags(i,j) + check_X(i,j)
                if TotalCount == 3:
                    locate_bomb(i,j)
                elif TotalCount > 3:
                    if check_flags(i,j) == 3:
                        locate_all_squares(i,j)
            if board_df.iloc[i,j] == '4':
                TotalCount = check_flags(i,j) + check_X(i,j)
                if TotalCount == 4:
                    locate_bomb(i,j)
                elif TotalCount > 4:
                    if check_flags(i,j) == 4:
                        locate_all_squares(i,j)
    print(board_df.equals(board_df_copy))
    if board_df.equals(board_df_copy):
        if did_second_corner == False:
            print("Cannot continue, marking bottom right")
            first_move(width-1,height-1)
            did_second_corner = True
        else:
            print("Cannot continue, marking random square")
            found = False
            for b in range(8,-1,-1):
                if not found:
                    for i in range(height):
                        for j in range(width):
                            if board_df.iloc[i,j] == 'X':
                                TotalCount = check_flags(i,j) + check_X(i,j)
                                print(b)
                                if TotalCount == b:
                                    click_square(i,j)
                                    print('found for', b)
                                    found = True
            
select_game_mode(mode)
get_board()
analyze_board()
first_move(0,0)

while not finished:
    calc_move()
    if essentials.check_exists_by_css_selector(driver, '.top-area-face.zoomable.hd_top-area-face-win'):
        finished = True
        print("Finished game!!!!")
    if essentials.check_exists_by_css_selector(driver, '.top-area-face.zoomable.hd_top-area-face-lose'):
        finished = True
        print("Lost game ):")
        
