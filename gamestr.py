import random


class Player:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.plant_num = 2
        self.material_num = 4
        self.fighter_num = 2
        self.cash = 10000
        self.plane_oredered = 0
        self.plants_building = []
        self.is_finished = False

class Game:
    def __init__(self, players, market_level, market_levels, market_chances, month_num):
        self.players_profiles = dict()
        self.players_raw_orders = dict()
        self.players_plane_orders = dict()
        self.players_num = players
        self.market_level = market_level
        self.market_levels = market_levels
        self.market_chances = market_chances
        self.month_num = month_num
        self.cur_month = 0
        self.is_started = False
        self.players_finished = 0

    def calculate_values(self):
        self.material_bank = int(self.market_levels[str(self.market_level)][0] * self.players_num)
        self.min_material_price = self.market_levels[str(self.market_level)][1]
        self.fighter_bank = int(self.market_levels[str(self.market_level)][2] * self.players_num)
        self.max_fighter_price = self.market_levels[str(self.market_level)][3]


    def sorting_orders(self, current_ind, hlp):
        last = self.sorted_players_raw_orders[current_ind:hlp]
        chance = []
        while len(last) != 0:
            for order in last:
                if order[1][0] <= self.material_bank:
                    chance.append(order)
            if len(chance) == 0:
                break
            lucky_man = random.choice(chance)
            self.material_bank -= lucky_man[1][0]
            self.players_profiles[lucky_man[0]].cash -= lucky_man[1][1] * lucky_man[1][0]
            self.players_profiles[lucky_man[0]].material_num += lucky_man[1][0]
            del chance[chance.index(lucky_man)]
            last = chance[:]
            chance.clear()

    def raw_handling(self):
        self.sorted_players_raw_orders = sorted(self.players_raw_orders.items(), key=lambda item: item[1][1], reverse=True)
        print(self.sorted_players_raw_orders)

        counter = 0
        current_ind = 0
        hlp_counter = 0
        hlp = 0
        for order in self.sorted_players_raw_orders:
            if counter == 0:
                current_price = order[1][1]
            if order[1][1] == current_price:
                counter += order[1][0]
                hlp += 1
            elif order[1][1] != current_price:
                if self.material_bank >= counter:
                    self.material_bank -= counter
                    counter = 0
                    current_ind = hlp
                    hlp_counter = hlp
                else:
                    self.sorting_orders(current_ind, hlp)
                    hlp_counter = len(self.sorted_players_raw_orders)
                    break
        self.sorting_orders(hlp_counter, hlp)
        for order in self.sorted_players_raw_orders[:current_ind]:
            self.players_profiles[order[0]].cash -= order[1][1] * order[1][0]
            self.players_profiles[order[0]].material_num += order[1][0]
        for i in self.players_profiles.values():
            print(i.cash, i.material_num)