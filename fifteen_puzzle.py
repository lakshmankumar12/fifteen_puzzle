#!/usr/bin/python

from __future__ import print_function
import random

def debug_print(string):
  #print(string)
  pass

allowed_opeartions=['L','R','U','D']

def print_board(board):
  b = 0
  print("|----+----+----+----|")
  for i in range(4):
    print("|",end="")
    for j in range(4):
      if board[b]:
        print(" %2d |"%board[b],end="")
      else:
        print("    |",end="")
      b += 1
    print("\n|----+----+----+----|")

def count_inversions(sequence,size):
  debug_print("Got sequence %s and size:%d"%(sequence, size))
  if size <= 1:
    return (0,sequence)
  if size == 2:
    if sequence[0] <= sequence[1]:
      return (0,sequence)
    else:
      t = sequence[0]
      sequence[0] = sequence[1]
      sequence[1] = t
      debug_print("Transformed to sequence %s and size:%d and returning result %d"%(sequence, size, 1))
      return (1,sequence)
  left = size/2
  right = size - left
  (left_inv, sequence[:left]) = count_inversions(sequence[:left], left)
  (right_inv, sequence[left:]) = count_inversions(sequence[left:], right)
  debug_print("Starting with left:%s and right:%s"%(sequence[:left], sequence[left:]))
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
  debug_print("Transformed to sequence %s and size:%d and returning result %d"%(sequence, size, result))
  return (result, sequence)

def is_valid_board(board):
  copy_board = board[:]
  #where is 0 the hold
  holeAt = copy_board.index(0)
  holeAt = holeAt/4
  if holeAt == 0 or holeAt == 2:
    toAdd = 1
  else:
    toAdd = 0
  copy_board.remove(0)  # remove 0 off the board
  (inversions, copy_board) = count_inversions(copy_board,len(copy_board))
  print("Inverstions was %d"%inversions)
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

def get_user_input():
  got = 0
  attempts = 1
  allowed_opeartions
  while not got:
    op1 = raw_input("Enter your choice (L/R/U/D):")
    op = op1.upper()
    if op not in allowed_opeartions:
      print("Enter one of L/R/U/D. You did %s"%op1)
    else:
      break;
    attempts += 1
    if attempts > 3:
      print("Too many attempts")
      sys.exit(1)
  return op

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
    print_board(board)
    print("Moves so far: %d"%moves)
    op = get_user_input()
    operate_on_board(board,op)
    won = is_board_won(board)
    moves += 1
  print_board(board)
  print("You did it in %d moves"%moves)

if __name__ == '__main__':
    main()

