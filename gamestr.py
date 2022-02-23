import random


class Player:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name
        self.plant_num = 2
        self.material_num = 4
        self.fighter_num = 2
        self.cash = 10000
        self.fighter_ordered = 0
        self.plants_building = []
        self.is_finished = False

class Game:
    def __init__(self, players, market_level, market_levels, market_chances, month_num):
        self.players_profiles = dict()
        self.players_raw_orders = dict()
        self.players_fighter_orders = dict()
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

    @staticmethod
    def spreading(spreading_obj):
        result = []
        cur_price = spreading_obj[0][1][1]
        hlp = []
        for order in spreading_obj:
            if order[1][1] == cur_price:
                hlp.append(order)
            elif order[1][1] != cur_price:
                result += [hlp[:]]
                hlp.clear()
                hlp.append(order)
                cur_price = order[1][1]
        result += [hlp[:]]
        return result

    def raw_handling(self):
        self.sorted_players_raw_orders = sorted(self.players_raw_orders.items(), key=lambda item: (item[1][1], item[1][0]), reverse=True)

        self.spread_players_raw_orders = self.spreading(self.sorted_players_raw_orders)

        for order_pack in self.spread_players_raw_orders:
            for order in order_pack:
                if self.material_bank == 0:
                    break
                if order[1][0] <= self.material_bank:
                    self.material_bank -= order[1][0]
                    self.players_profiles[order[0]].cash -= order[1][0] * order[1][1]
                    self.players_profiles[order[0]].material_num += order[1][0]
                elif order[1][0] >= self.material_bank:
                    self.players_profiles[order[0]].cash -= self.material_bank * order[1][1]
                    self.players_profiles[order[0]].material_num += self.material_bank
                    break

        for i in self.players_profiles.values():
            print(i.cash, i.material_num)

    def plane_handling(self):
        self.sorted_players_fighter_orders = sorted(self.players_fighter_orders.items(), key=lambda item: (-1 * item[1][1], item[1][0]), reverse=True)

        self.spread_players_fighter_orders = self.spreading(self.sorted_players_fighter_orders)

        for order_fighter in self.spread_players_fighter_orders:
            for order in order_fighter:
                if self.material_bank == 0:
                    break
                if order[1][0] <= self.fighter_bank:
                    self.fighter_bank -= order[1][0]
                    self.players_profiles[order[0]].cash += order[1][0] * order[1][1]
                    self.players_profiles[order[0]].fighter_num -= order[1][0]
                elif order[1][0] >= self.fighter_bank:
                    self.players_profiles[order[0]].cash += self.material_bank * order[1][1]
                    self.players_profiles[order[0]].fighter_num -= self.fighter_bank
                    break

    def fighter_produce(self):
        for player in self.players_profiles.values():
            player.fighter_num += player.fighter_ordered
            player.fighter_ordered = 0

    def plant_checker(self):
        for player in self.players_profiles.values():
            player.plants_building = [month + 1 for month in player.plants_building]
            analys = player.plants_building[:]
            for month in analys:
                if month == 4:
                    player.plant_num += 1
                    player.cash -= 2500
                    del player.plants_building[player.plants_building.index(4)]

    def calculate_taxes(self):
        pass
