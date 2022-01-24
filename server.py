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
players_profiles = dict()
players_raw_orders = dict()
game = Game(players, 3, market_levels, market_chances, month)
game.calculate_values()


@server.post('/connect')
def index():
    global players_profiles
    data = request.get_json()
    if game.is_started is False and len(players_profiles) < game.players:
        player = Player(request.remote_addr, data['name'])
        players_profiles[request.remote_addr] = player
        return jsonify(data=f'{data["name"]} you succesfully joined the game', status='ok')
    else:
        return jsonify(data='Game has already started or lobby is full', status='no')


@server.get('/user_info')
def user_info():
    plants = players_profiles[request.remote_addr].plant_num
    cash = players_profiles[request.remote_addr].cash
    fighters = players_profiles[request.remote_addr].fighter_num
    raw = players_profiles[request.remote_addr].material_num
    return jsonify(plants=plants, cash=cash, fighters=fighters, raw=raw)


@server.post('/buy_raw')
def purchase():
    data = request.get_json()
    if int(data['price']) >= int(game.min_material_price):
        players_raw_orders[request.remote_addr] = [data['number'], data['price']]
        print(players_raw_orders)
        return jsonify(data=f'{players_profiles[request.remote_addr].name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{players_profiles[request.remote_addr].name}, you order was not accepted', status='no')


@server.post('/sell_planes')
def get_order():
    data = request.get_json()
    if int(data['price']) <= int(game.max_fighter_price):
        players_raw_orders[request.remote_addr] = [data['number'], data['price']]
        print(players_raw_orders)
        return jsonify(data=f'{players_profiles[request.remote_addr].name}, you order was accepted', status='ok')
    else:
        return jsonify(data=f'{players_profiles[request.remote_addr].name}, you order was not accepted', status='no')


@server.route('/info', methods=["GET"])
def send_info():
    print(jsonify(data=players_profiles))
    return jsonify(data=players_profiles)



if __name__ == "__main__":
    server.run(ip, port=port)