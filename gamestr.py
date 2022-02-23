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


    def raw_handling(self):
        self.sorted_players_raw_orders = sorted(self.players_raw_orders.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)
        self.spread_players_raw_orders = []
        cur_price = self.sorted_players_raw_orders[0][1][1]
        hlp = []
        for order in self.sorted_players_raw_orders:
            if order[1][1] == cur_price:
                hlp.append(order)
            elif order[1][1] != cur_price:
                self.spread_players_raw_orders += [hlp[:]]
                hlp.clear()
                hlp.append(order)
                cur_price = order[1][1]
        self.spread_players_raw_orders += [hlp[:]]
        for order_pack in self.spread_players_raw_orders:
            for order in order_pack:
                if order[1][0] <= self.material_bank:
                    self.material_bank -= order[1][0]
                    self.players_profiles[order[0]].cash -= order[1][0] * order[1][1]
                    self.players_profiles[order[0]].material_num += order[1][0]
                else:
                    break

        for i in self.players_profiles.values():
            print(i.cash, i.material_num)