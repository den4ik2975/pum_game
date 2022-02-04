from flask import Flask, jsonify, request
from const import market_levels, market_chances
from gamestr import Game, Player
import sys


def is_valid_addr(ip):
    if ip.count('.') == 3:
        for i in ip.split('.'):
            if 0 <= int(i) <= 255:
                pass
            else:
                return False
        return True


def set_params():
    if len(sys.argv) == 4:
        if is_valid_addr(sys.argv[1]):
            return [sys.argv[1], sys.argv[2], sys.argv[3], -1]
        else:
            print('wrong ip')
    elif len(sys.argv) == 5:
        if is_valid_addr(sys.argv[1]):
            return [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
        else:
            print('wrong ip')
    else:
        print('Try again')
    return [False]


params = set_params()
if len(params) == 4:
    ip, port, players, month = params[0], params[1], int(params[2]), int(params[3])
else:
    sys.exit()


server = Flask(__name__)
game = Game(players, 3, market_levels, market_chances, month)
game.calculate_values()


@server.post('/connect')
def index():
    data = request.get_json()
    if game.is_started is False and len(game.players_profiles) < game.players_num:
        player = Player(request.remote_addr, data['name'])
        game.players_profiles[request.remote_addr] = player
        return jsonify(data=f'{data["name"]} you succesfully joined the game', status='ok')
    else:
        return jsonify(data='Game has already started or lobby is full', status='no')


@server.get('/user_info')
def user_info():
    plants = game.players_profiles[request.remote_addr].plant_num
    cash = game.players_profiles[request.remote_addr].cash
    fighters = game.players_profiles[request.remote_addr].fighter_num
    raw = game.players_profiles[request.remote_addr].material_num
    return jsonify(plants=plants, cash=cash, fighters=fighters, raw=raw)


@server.post('/buy_raw')
def purchase():
    cur_player = game.players_profiles[request.remote_addr]
    data = request.get_json()
    if int(data['price']) >= int(game.min_material_price):
        game.players_raw_orders[request.remote_addr] = [data['number'], data['price']]
        print(game.players_raw_orders)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/sell_planes')
def get_order():
    cur_player = game.players_profiles[request.remote_addr]
    data = request.get_json()
    if int(data['price']) <= int(game.max_fighter_price):
        game.players_plane_orders[request.remote_addr] = [data['number'], data['price']]
        print(game.players_plane_orders)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/produce')
def plane_order():
    data = request.get_json()['amount']
    cur_player = game.players_profiles[request.remote_addr]
    if cur_player.plant_num >= data and cur_player.material_num >= data and cur_player.cash >= (data * 2000):
        cur_player.material_num -= data
        cur_player.cash -= (data * 2000)
        cur_player.plane_ordered = data
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/build')
def build_order():
    data = request.get_json()['amount']
    cur_player = game.players_profiles[request.remote_addr]
    if cur_player.plant_num + len(cur_player.plants_building) + data <= 6 and cur_player.cash >= data * 4000:
        cur_player.plants_building += [0] * data
        cur_player.cash -= (data * 4000)
        return jsonify(data=f'{cur_player.name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{cur_player.name}, you order was not accepted', status='no')


@server.post('/finish')
def finish_turn():
    cur_player = game.players_profiles[request.remote_addr]
    cur_player.is_finished = True
    game.players_finished += 1
    return jsonify(data=f'Finished')


if __name__ == "__main__":
    server.run(ip, port=port)


while True:
    if len(game.players_profiles) == game.players_num:
        game.is_started = True
        break
