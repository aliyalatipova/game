import pygame


class AllMoneyCounter:
    def __init__(self):
        self.name = 'all_money'
        self.money_at_start_of_race = 0

    def load_from_txt(self):
        money = 0
        f = open(f"""data\\{self.name}.txt""", encoding="utf8")
        for number, line in enumerate(f):
            if number == 0:
                money = int(line)
        f.close()
        self.money_at_start_of_race = money

    def print_all_money(self, screen, money_in_one_race):
        font = pygame.font.Font(None, 50)
        text = font.render(str(money_in_one_race + self.money_at_start_of_race), True, 'White')
        screen.blit(text, (70, 10))
