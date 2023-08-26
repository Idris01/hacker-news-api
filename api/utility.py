import re
from string import punctuation


def tokenize(data):
    pattern = "[{}]".format(punctuation)
    token = re.sub(pattern, " ", data).split()
    return [item.lower() for item in token if len(item) > 1]
