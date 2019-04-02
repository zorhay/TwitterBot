import poebot

poem = poebot.poems.PoemBase(structure=[(9, 1), (8, 0), (9, 3), (8, 2)], source='poebot/source.txt')
for line in poem.word_rand_generate():
    print(line)
