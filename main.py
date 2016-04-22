#!/usr/sbin/python3
import json
import random
import settings


def save_json(names, args):
    f = open("data/" + args + ".json", "w+")
    f.write(json.dumps(names[args]))
    f.close()


def load_json():
    names = {}
    for file_name in settings.DATA_FILE_NAMES:
        f = open("data/" + file_name + ".json", "r")
        names[file_name] = json.loads(f.read())
        f.close()
    return names


def generate_name(names, attr, lang):
    print(random.choice(names[attr][lang]), random.choice(names["surname"][lang]))


def main():
    names = load_json()
    chosen = "female"
    lang = "polish"
    generate_name(names, chosen, lang)


if __name__ == "__main__":
    main()
