import subprocess
import os
import random
from enum import Enum

class FILETYPE(Enum):
    IMAGE=0
    SOUND=1
    MOVIE=2
    TEXT=3
    JSON=4
    SOURCE=5
    MODEL=6

def getRequirements():
    proc = subprocess.Popen(
        ['pip', 'freeze'],
        stdout=subprocess.PIPE
    )

    out, err = proc.communicate()
    requirements = out.decode('utf-8')
    return requirements

def create_experiment_name():
    adjectives = ['brilliant', 'adorable', 'shy', 'beautiful', 'popular', 'huge', 'curious', 'confident', 'assured', 'eager', 'energetic', 'loyal', 'nervous', 'careful', 'relaxed', 'calm', 'component', 'capable', 'talented', 'kind', 'wise', 'bright', 'busy', 'cool', 'cute', 'fair', 'fine', 'fresh', 'funny', 'grand', 'great', 'glad', 'humorous', 'lucky', 'nice', 'perfect', 'polite', 'proud', 'powerful', 'pretty', 'pure', 'quick', 'quiet', 'real', 'rich', 'right', 'royal', 'social', 'soft', 'safe', 'serious', 'simple', 'still', 'strong', 'thin', 'tiny', 'tired', 'virtual', 'weak', 'wide', 'warm', 'wild','young', 'lazy', 'lonely', 'large', 'angry', 'asleep', 'brave', 'active']
    objectives = ['crocodile', 'ant' ,'eater', 'bat', 'beaver', 'buffalo', 'camel', 'chameleon', 'cheetah', 'squirrel', 'chinchilla', 'cormorant', 'coyote', 'crow', 'dinosaur', 'dolphin', 'duck', 'elephant', 'fox', 'weasel', 'frog', 'giraffe', 'bear', 'hedgehog', 'hippo', 'hyena', 'iguana', 'koala', 'leopard', 'liger', 'llama', 'monkey', 'whale', 'cat', 'orangutan', 'otter', 'panda', 'penguin', 'platypus', 'raccoon', 'rhinoceros', 'sheep', 'skunk', 'turtle', 'wolf', 'badger', 'gorilla', 'snail', 'dog', 'pig', 'chicken']
    
    experiment_name : str = random.choice(adjectives) + "-" + random.choice(objectives) + "-"
    numbers = "0123456789"
    for i in range(0, 4):
            experiment_name += random.choice(numbers)

    return experiment_name