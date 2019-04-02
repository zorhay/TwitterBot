import poebot
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

poem = poebot.poems.PoemBase(structure=[(9, 1), (8, 0), (9, 3), (8, 2)], source=os.path.join(current_dir, 'poebot/source.txt'))
for line in poem.word_rand_generate():
    print(line)
