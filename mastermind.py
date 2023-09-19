import random
import sys
from collections import Counter

import urllib.request


def get_wordlist(length):
  url = "https://www.mit.edu/~ecprice/wordlist.10000"
  with urllib.request.urlopen(url) as f:
    words_blob = f.read().decode('utf-8')
    words = words_blob.split("\n")
  return [w for w in words if len(w) == length]


def calc_match(word, guess, counts):
  black = sum([a == b for a, b in zip(guess, word, strict=True)])
  white = 0
  for c, n in Counter(guess).items():
    white += min(n, counts[c])
  white -= black
  return black, white


def main():
  # alphabet = "abcde"
  # word = ''.join([random.choice(alphabet) for _ in range(4)])

  dictionary = get_wordlist(4)
  print(f"The dictionary has {len(dictionary)} words")
  word = random.choice(dictionary)

  counts = Counter(word)

  length = len(word)
  print(f"The length of the word is {length}")
  # print(f'{word=}')

  seen_characters = set()

  pruned_dictionary = dictionary

  for step in range(5, 0, -1):
    while True:
      print(f'You have {step} attempts left')
      if seen_characters:
        print(f"Seen characters: {seen_characters}")

      # prompt and accept guess
      guess = input("Guess: ")
      print(f"Your guess: '{guess}'")
      if len(guess) != length:
        print(f"Your guess must be of length {length}")
      # elif not all(l in alphabet for l in set(guess)):
      #   print(f'Your guess must be in the {alphabet=}')
      else:
        break

    # evaluate
    if guess == word:
      print("You win!")
      return

    # print response
    black, white = calc_match(word, guess, counts)
    print(f"You get {black} blacks, {white} whites")

    tmp_dict = set()
    for g in pruned_dictionary:
      b, w = calc_match(g, guess, Counter(g))
      if b == black and w == white:
        tmp_dict.add(g)
    pruned_dictionary = tmp_dict
    print(f"Size of search space: {len(pruned_dictionary)}")
    print()

    seen_characters |= set(guess)

  print(f"You lose! The word was '{word}'")


if __name__ == "__main__":
  # get_wordlist()
  main()
