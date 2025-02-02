# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Greyson Acker
#               Arda Arikan
#               Lucas Raymond
#               Luke Shull
# Section:      ENGR 102-213
# Assignment:   Lab 13
# Date:         01 December 2023
import turtle
from math import sqrt
import numpy as np
from playsound import playsound  #MAKE SURE YOU HAVE PLAYSOUND VERSION 1.2.2, THE LATEST VERSION IS VERY UNRELIABLE

play_counter = [1]
erased = [0]
p1_pieces = []
p2_pieces = []
removed_piece = [[]]
turtle.clearscreen()
t = turtle.Turtle()
t.ht()
s = turtle.Screen()
p1 = turtle.Turtle()
p1.ht()
t.speed(0)
p1.speed(0)

rules = input("Do you want to hear the rules? (y/n): ")
if rules == "y":
  print()
  with open("instructions.txt", "r") as file: print(file.read())
  playsound('DIRECTIONS_BETTER.mp3',False) #Volume up
if rules != "y":
  print(":(")

board = np.zeros((5, 5)) + 2

def play_game(x, y):
  '''Main function for game including conditionals for determining piece replacement'''
  if exit(x,y):
    turtle.bye()
    print("Game ended.")
  elif erased[0] == 1:
    if main_game(x, y):
      if not (win_condition(board)):
        erased[0] = 0
      else:
        color = "red" if (play_counter[0] - 1) % 2 == 1 else "blue"
        if color == 'red':
          playsound('Red_wins.mp3',False)
        else:
          playsound('Blue_wins.mp3',False)
        print(f"Game Over: {color} wins! Click anywhere to exit")
        turtle.exitonclick()
  elif len(p1_pieces) == 4 and len(p2_pieces) == 4:
    erased[0] = erase_piece(x, y)
  elif len(p1_pieces) < 4 or len(p2_pieces) < 4:
    int_draw_piece(x, y)
    if (win_condition(board)):
      color = "red" if (play_counter[0] - 1) % 2 == 1 else "blue"
      if color == 'red':
        playsound('Red_wins.mp3',False)
      else:
        playsound('Blue_wins.mp3',False)
      print(f'Game Over: {color} wins! Click anywhere to exit')
      turtle.exitonclick()

def getnum(why):
  dict = {"red": 0, "blue": 1, "white": 2}
  return dict[why]

def main_game(x, y):
  '''Place pieces after the inital 4 placements. Included checking valid     palcement'''
  p1.penup()
  circlelocs = []
  for a in range(-240, 360, 120):
    for b in range(-240, 360, 120):
      circlelocs += [[a, b]]
  for loc in circlelocs:
    if sqrt((loc[0] - x)**2 + (loc[1] - y)**2) < 40:
      if validmove(removed_piece[0], loc):
        if ([loc[0], loc[1]] in p1_pieces or [loc[0], loc[1]] in p2_pieces):
          playsound("BAD_BETTER.mp3",False)
          print('Invalid move. Try again.')
          break
        if play_counter[0] % 2 != 0:
          loc += [getnum('red')]
          p1_pieces.append([loc[0], loc[1]])
          board[boardtomat([loc[1], loc[0]])] = getnum("red")
          play_counter[0] = play_counter[0] + 1
        else:
          loc += [getnum('blue')]
          p2_pieces.append([loc[0], loc[1]])
          board[boardtomat([loc[1], loc[0]])] = getnum("blue")
          play_counter[0] = play_counter[0] + 1
        p1.goto(loc[0], loc[1])
        p1.pendown()
        p1.begin_fill()
        if loc[2] == 0:
          p1.pencolor('crimson')
          p1.fillcolor('red')
        elif loc[2] == 1:
          p1.pencolor('navy')
          p1.fillcolor('blue')
        elif loc[2] == 2:
          p1.pencolor('black')
          p1.fillcolor('white')
        p1.dot(78)
        p1.penup()
        p1.end_fill()
        return True
      else:
        playsound("BAD_BETTER.mp3",False)
        print('Invalid move. Try again.')
        return False


def int_draw_piece(x, y):
  '''Initial 4 piece placement'''
  p1.penup()
  circlelocs = []
  #Make lists of valid circle locations
  for a in range(-240, 360, 120):
    for b in range(-240, 360, 120):
      circlelocs += [[a, b]]
  #Loop through circle locations
  for loc in circlelocs:
    #Check if click inside circle
    if sqrt((loc[0] - x)**2 + (loc[1] - y)**2) < 40:
      #Check if valid location
      if [loc[0], loc[1]] in p1_pieces or [loc[0], loc[1]] in p2_pieces:
        break
      #If red's turn
      if play_counter[0] % 2 != 0:
        #Assign color to blue
        loc += [getnum('red')]
        board[boardtomat([loc[1], loc[0]])] = getnum('red')
        p1_pieces.append([loc[0], loc[1]])
        play_counter[0] = play_counter[0] + 1
      #If blue's turn
      else:
        #Assign color to blue
        loc += [getnum('blue')]
        board[boardtomat((loc[1], loc[0]))] = getnum('blue')
        p2_pieces.append([loc[0], loc[1]])
        play_counter[0] = play_counter[0] + 1
      #place dot on circle
      p1.goto(loc[0], loc[1])
      p1.pendown()
      p1.begin_fill()
      if loc[2] == 0:
        p1.pencolor('crimson')
        p1.fillcolor('red')
      elif loc[2] == 1:
        p1.pencolor('navy')
        p1.fillcolor('blue')
      elif loc[2] == 2:
        p1.pencolor('black')
        p1.fillcolor('white')
      p1.dot(78)
      p1.penup()
      p1.end_fill()


def erase_piece(x, y):
  '''Function for erasing a selected piece'''
  p1.penup()
  circlelocs = []
  for a in range(-240, 241, 120):
    for b in range(-240, 241, 120):
      circlelocs += [[a, b]]
  #Loop through circle locations
  for loc in circlelocs:
    #Check if valid location
    if sqrt((loc[0] - x)**2 + (loc[1] - y)**2) < 40:
      #Determine player and check if piece on clicked circle
      if play_counter[0] % 2 != 0:
        try:
          p1_pieces.remove([loc[0], loc[1]])
        except:
          return 0
      else:
        try:
          p2_pieces.remove([loc[0], loc[1]])
        except:
          return 0
      removed_piece[0] = [loc[0], loc[1]]
      p1.goto(loc[0], loc[1])
      p1.dot(78, "white")
      p1.goto(loc[0], loc[1])
      board[boardtomat([loc[1], loc[0]])] = getnum("white")
      return 1


def print_board():
  '''Print an empty Teeko Board'''
  #Print name of game
  t.penup()
  t.goto(0, 300)
  t.pendown()
  t.write('TEEKO', align='center', font=('Ariel', 50, 'bold'))
  #Print stop button
  t.penup()
  t.goto(-40,-340)
  t.pendown()
  t.fillcolor('red')
  t.begin_fill()
  for i in range(2):
    t.forward(80)
    t.left(90)
    t.forward(40)
    t.left(90)
  t.right(90)
  t.end_fill()
  t.penup()
  t.left(90)
  t.goto(0,-330)
  t.pendown()
  t.write("STOP",align = 'center',font=('Ariel',10, 'bold'))
  t.penup()
  #Print circles
  for i in range(5):
    for j in range(5):
      t.penup()
      t.setpos(-240 + (120 * j), -240 + (120 * i))
      t.dot(80, "black")
      t.dot(78, "white")
  #Print connecting horizontal/vertical lines
  for i in range(4):
    for j in range(5):
      t.penup()
      t.setpos(-200 + 120 * i, -240 + 120 * j)
      t.pendown()
      t.forward(40)
      t.left(90)
      t.penup()
      t.setpos(-240 + 120 * j, -200 + 120 * i)
      t.pendown()
      t.forward(40)
      t.right(90)
  t.left(135)
  #print connecting diagonal lines
  for i in range(4):
    for j in range(4):
      t.right(90)
      t.penup()
      t.setpos(-211.716 + 120 * i, -211.716 + 120 * j)
      t.pendown()
      t.forward(89.7)
      t.left(90)
      t.penup()
      t.setpos(211.716 - 120 * i, -211.716 + 120 * j)
      t.pendown()
      t.forward(89.7)

def boardtomat(coords):
  '''Make coordinates on turtle canvas matrix indeces'''
  return abs(coords[1] // 120 + 2), abs(coords[0] // 120 - 2)

def win_condition(board):
  '''Checks board for win conditions'''
  color = "red" if (play_counter[0] - 1) % 2 == 1 else "blue"
  pieces = np.where(board == getnum(color))
  if len(pieces[0]) == 4:
    if pieces[0][1] == pieces[0][0] + 1 and pieces[1][1] == pieces[1][0] + 1:
      #negative diagonal
      if pieces[0][2] == pieces[0][1] + 1 and pieces[1][2] == pieces[1][1] + 1:
        if pieces[0][3] == pieces[0][2] + 1 and pieces[1][
            3] == pieces[1][2] + 1:
          return True
    if pieces[0][3] == pieces[0][0] + 1 and pieces[1][3] == pieces[1][0] + 1:
      #square
      if pieces[0][2] == pieces[0][1] + 1 and pieces[1][2] == pieces[1][1] - 1:
        return True
    if pieces[0][1] == pieces[0][0] and pieces[1][1] == pieces[1][0] + 1:
      #vertical stack
      if pieces[0][2] == pieces[0][1] and pieces[1][2] == pieces[1][1] + 1:
        if pieces[0][3] == pieces[0][2] and pieces[1][3] == pieces[1][2] + 1:
          return True
    if pieces[0][1] == pieces[0][0] + 1 and pieces[1][1] == pieces[1][0]:
      #horizontal row
      if pieces[0][2] == pieces[0][1] + 1 and pieces[1][2] == pieces[1][1]:
        if pieces[0][3] == pieces[0][2] + 1 and pieces[1][3] == pieces[1][2]:
          return True
    if pieces[0][1] == pieces[0][0] + 1 and pieces[1][1] == pieces[1][0] - 1:
      #postive diagonal
      if pieces[0][2] == pieces[0][1] + 1 and pieces[1][2] == pieces[1][1] - 1:
        if pieces[0][3] == pieces[0][2] + 1 and pieces[1][
            3] == pieces[1][2] - 1:
          return True
  else:
    return False

def validmove(prev, nex):
  '''Check if a move for replacing piece is valid'''
  if boardtomat(nex) != boardtomat(prev): #ensure cannot replace piece in space you took it out of
    if boardtomat(nex)[0] >= boardtomat(prev)[0] - 1 and boardtomat(nex)[
        0] <= boardtomat(prev)[0] + 1 and boardtomat(nex)[1] >= boardtomat(
            prev)[1] - 1 and boardtomat(nex)[1] <= boardtomat(prev)[1] + 1:
      return True
  return False

def exit(x,y):
  return x >= -40 and x <= 40 and y >= -340 and y <= -300

print_board()
turtle.onscreenclick(play_game)
turtle.done()