#!/usr/bin/python

from __future__ import print_function
import random
import curses
import sys

def stringize_board(board):
  b = 0
  result = "|----+----+----+----|\n"
  for i in range(4):
    result += "|"
    for j in range(4):
      if board[b]:
        result += " %2d |"%board[b]
      else:
        result += "    |"
      b += 1
    result += "\n|----+----+----+----|\n"
  return result

def print_board(board):
  print(stringize_board(board),end="")

def count_inversions(sequence,size):
  if size <= 1:
    return (0,sequence)
  if size == 2:
    if sequence[0] <= sequence[1]:
      return (0,sequence)
    else:
      t = sequence[0]
      sequence[0] = sequence[1]
      sequence[1] = t
      return (1,sequence)
  left = size/2
  right = size - left
  (left_inv, sequence[:left]) = count_inversions(sequence[:left], left)
  (right_inv, sequence[left:]) = count_inversions(sequence[left:], right)
  l = 0
  r = left
  invers = 0
  new_merge = []
  while r < size:
    while sequence[r] > sequence[l] and l < left:
      new_merge.append(sequence[l])
      l += 1
    if l < left:
      invers += (left - l)
      new_merge.append(sequence[r])
      r += 1
    else:
      break;
  if l == left and r < size:
    new_merge.extend(sequence[r:])
  elif r == size and l < left:
    new_merge.extend(sequence[l:left])
  sequence[0:size] = new_merge
  result =  left_inv + right_inv + invers
  return (result, sequence)

def is_valid_board(board):
  copy_board = board[:]
  #where is 0 the hole
  holeAt = copy_board.index(0)
  holeAt = holeAt/4
  if holeAt == 0 or holeAt == 2:
    toAdd = 1
  else:
    toAdd = 0
  copy_board.remove(0)  # remove 0 off the board
  (inversions, copy_board) = count_inversions(copy_board,len(copy_board))
  if ( inversions + toAdd ) % 2 == 0:
    return 1
  else:
    return 0

def generate_board():
  attempts = 0
  max_attempts = 5
  while attempts < max_attempts:
    board = range(15,-1,-1)
    random.shuffle(board)
    valid = is_valid_board(board)
    if valid:
      break
  if attempts > max_attempts:
    raise(Exception("Couldn't get a valid board after 5 attempts"))
  return board

def draw_board_and_user_input(stdscr, board_str, moves):
  stdscr.clear()
  stdscr.move(5,0);
  stdscr.addstr(board_str, curses.color_pair(1))
  stdscr.move(15,5);
  stdscr.addstr("Moves So Far:%d"%moves, curses.color_pair(1))
  stdscr.move(16,5);
  stdscr.addstr("Your Move (Press any arrow keys or ctrl-C):", curses.color_pair(1))
  stdscr.refresh()

def valid_user_input(input_key):
  operation = None
  if input_key == curses.KEY_RIGHT:
    operation = 'R'
  elif input_key == curses.KEY_LEFT:
    operation = 'L'
  elif input_key == curses.KEY_UP:
    operation = 'U'
  elif input_key == curses.KEY_DOWN:
    operation = 'D'
  else:
    return (0,None)
  return (1,operation)

def curses_print_and_input_function(stdscr, board_str, moves, user_input_result):
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
  attempt = 0
  got = 0
  draw_board_and_user_input(stdscr, board_str, moves)
  while not got and attempt < 3:
    result = stdscr.getch()
    (ok,op) = valid_user_input(result)
    if ok:
      got = 1
      user_input_result.append(op)
      break;
    attempt += 1
    stdscr.move(17,5);
    stdscr.addstr("That was not a valid input:%d, attempt:%d"%(result,attempt))
    stdscr.move(16,48);
    stdscr.refresh()
  if not got:
    user_input_result.append('B')
  return

winning_board = []
def is_board_won(board):
  global winning_board
  if not winning_board:
    winning_board = list(range(1,16))
    winning_board.extend([0])
  if board == winning_board:
    return True
  return False

def operate_on_board(board, operation):
  ''' Operation
       'L','R','U','D'
      Respectively refer left,right,up,down

      When left is done, the number moves left. That is hole moves right.
  '''
  holeAt = board.index(0)
  LeftNotOk  = [3,7,11,15]
  RightNotOk = [0,4,8,12]
  UpNotOk    = [12,13,14,15]
  DownNotOk  = [0,1,2,3]
  if operation == 'L':
    notAllowedPositions = LeftNotOk
    swapIndex = holeAt + 1
  elif operation == 'R':
    notAllowedPositions = RightNotOk
    swapIndex = holeAt - 1
  elif operation == 'U':
    notAllowedPositions = UpNotOk
    swapIndex = holeAt + 4
  elif operation == 'D':
    notAllowedPositions = DownNotOk
    swapIndex = holeAt - 4
  else:
    raise Exception("Invalid operation:%s"%operation)
  if holeAt in notAllowedPositions:
    return 0;
  board[holeAt] = board[swapIndex]
  board[swapIndex] = 0
  return 1;

def main():
  board = generate_board()
  won = False
  moves = 0
  while not won:
    op = []
    board_str = stringize_board(board)
    curses.wrapper(curses_print_and_input_function, board_str, moves, op)
    if op[0] == 'B':
      print("Too many bad inputs..Terminating")
      sys.exit(1)
    operate_on_board(board,op[0])
    won = is_board_won(board)
    moves += 1
  print_board(board)
  print("You did it in %d moves"%moves)

if __name__ == '__main__':
    main()

