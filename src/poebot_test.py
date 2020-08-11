from src.poebot.poems.PoemBase import PoemBase

poem = PoemBase()
poem.word_rand_generate(structure=[(9, 2), (8, 3), (9, 0), (8, 1)])
poem.word_rand_generate(structure=[(9, 2), (8, 3), (9, 0), (8, 1)])

print(poem.to_print())
