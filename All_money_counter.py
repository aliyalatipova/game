import pygame           # писала Алия(1-31)


class AllMoneyCounter:
    def __init__(self):
        self.name = 'all_money'
        self.full_file_name = f"""data\\{self.name}.txt"""
        self.money_at_start_of_race = 0
        self.money_in_one_race = 0

    def load_from_txt(self):
        money = 0
        f = open(self.full_file_name, encoding="utf8")
        for number, line in enumerate(f):
            if number == 0:
                money = int(line)
        f.close()
        self.money_at_start_of_race = money

    def print_all_money(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.money_in_one_race + self.money_at_start_of_race), True, 'White')
        screen.blit(text, (70, 10))

    def load_to_txt(self):
        f = open(self.full_file_name, 'w')
        should_be_writen = str(self.money_in_one_race + self.money_at_start_of_race)
        f.write(should_be_writen)
        f.close()
        self.money_at_start_of_race = self.money_in_one_race + self.money_at_start_of_race
        self.money_in_one_race = 0

    def get_money_at_start_of_race(self):       # писала София (33-46)
        return self.money_at_start_of_race

    def set_money_at_start_of_race(self, money_at_start_of_race):
        self.money_at_start_of_race = money_at_start_of_race

    def get_money_in_one_race(self):
        return self.money_in_one_race

    def set_money_in_one_race(self, money_in_one_race):
        self.money_in_one_race = money_in_one_race

    def get_all_money(self):
        return self.money_in_one_race + self.money_at_start_of_race
