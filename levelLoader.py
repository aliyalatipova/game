class LevelLoader:
    level = 0

    def __init__(self, level):              # писала софия (1-16)
        self.level = level

    def load(self):
        map1 = list()
        f = open(f"""data\\level{self.level}.txt""", encoding="utf8")
        for number, line in enumerate(f):
            line1 = [str(line[0]), str(line[1]), str(line[2])]
            map1.append(line1)

        f.close()
        return map1


