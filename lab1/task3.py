import regex as re
import glob


def for_one(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    main = re.findall(r'(\bustaw(a|y|ie|om|ę|ą|ami|ach|o)?\b)', content, flags=re.M | re.I)
    return len(main)


COUNTER = 0
for filename in glob.glob("../ustawy/*.txt"):
    COUNTER += for_one(filename)

print(COUNTER)
