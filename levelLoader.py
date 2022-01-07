class LevelLoader:
    level = 0

    def __init__(self, level):              # писала софия (1-16)
        self.level = level

    def load(self):
        map1 = list()
        f = open(f"""data\\level{self.level}.txt""", encoding="utf8")
        for number, line in enumerate(f):
            line1 = [int(line[0]), int(line[1]), int(line[2])]
            map1.append(line1)

        f.close()
        # вот эта функция должна будет по имени текстового файла вернуть список
        return map1
