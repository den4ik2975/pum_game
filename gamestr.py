class Player:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.plant_num = 2
        self.material_num = 4
        self.fighter_num = 2
        self.cash = 10000


class Game:
    def __init__(self, players, market_level, market_levels, market_chances, month_num):
        self.players = players
        self.market_level = market_level
        self.market_levels = market_levels
        self.market_chances = market_chances
        self.month_num = month_num
        self.cur_month = 0
        self.is_started = False

    def calculate_values(self):
        self.material_bank = int(self.market_levels[str(self.market_level)][0] * self.players)
        self.min_material_price = self.market_levels[str(self.market_level)][1]
        self.fighter_bank = int(self.market_levels[str(self.market_level)][2] * self.players)
        self.max_fighter_price = self.market_levels[str(self.market_level)][3]