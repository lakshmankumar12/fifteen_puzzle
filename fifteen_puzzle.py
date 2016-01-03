#!/usr/bin/python

from __future__ import print_function
import random

def debug_print(string):
  #print(string)
  pass

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

def main():
  a = range(15,-1,-1)
  random.shuffle(a)
  print_board(a)
  valid = is_valid_board(a)
  print("valid is %d"%valid)

if __name__ == '__main__':
    main()

