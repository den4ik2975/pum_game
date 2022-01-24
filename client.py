import sys

import requests

import time
import copy
import os


'''def is_valid_addr(ip):
    if ip.count(':') == 1:
        if ip[:ip.index(':')].count('.') == 3:
            for i in ip[:ip.index(':')].split('.'):
                if 0 <= int(i) <= 255:
                    pass
                else:
                    return False
            return True
    return False


while True:
    ip = input('Enter ip and port like: 0.0.0.0:0000\n')
    if is_valid_addr(ip):
        print('Succes')
        break
    else:
        print('Try again')'''

ip = '127.0.0.1:5000'
url = f"http://{ip}/"
name = input('Enter your name\n')
claimed = {'raw': False, 'sell': False, 'produce': False, 'build': False}

while True:
    response = requests.post(f'{url}connect', json={'name': name})
    print(response.json()['data'])
    if response.json()['status'] == 'ok':
        break
    time.sleep(1)


def order(op_type, info):
    inp = ['raw', 'buy'] if op_type == 'raw' else ['plane', 'sell']
    req = 'buy_raw' if op_type == 'raw' else 'sell_planes'
    while True:
        print(info)
        raw = input(f"How much {inp[0]} you want to {inp[1]}? Input number and price separated by a space If you don't want to buy just press Enter\n")
        if raw == '':
            break
        raw = raw.split()
        if len(raw) == 2:
            response = requests.post(f'{url}{req}', json={'number': raw[0], 'price': raw[1]})
            print(response.json()['data'])
            time.sleep(1.5)
            os.system('CLS')
            if response.json()['status'] == 'ok':
                break
        else:
            print('Incorrect input')
            time.sleep(1)
            os.system('CLS')
    return None


os.system('CLS')
while True:
    claimed_copy = copy.deepcopy(claimed)
    response = requests.get(f'{url}user_info')
    plants, cash, fighters, raw = response.json()['plants'], response.json()['cash'], response.json()['fighters'], response.json()['raw']
    info = f"Plants: {plants}\nCash: {cash}\nFighters: {fighters}\nRaw: {raw}\n"
    while True:
        print(info)
        message = f"1 - buy raw. Done: {claimed_copy['raw']}\n" \
                  f"2 - sell planes. Done: {claimed_copy['sell']}\n" \
                  f"3 - produce material. Done: {claimed_copy['produce']}\n" \
                  f"4 - buy raw. Done: {claimed_copy['build']}\n" \
                  f"5 - Finish turn\n"
        inp = input(message)
        if inp == '1':
            order('raw', info)
            claimed_copy['raw'] = True
        if inp == '2':
            order('plane', info)
            claimed_copy['sell'] = True
        if inp == '6':
            sys.exit()
        os.system('CLS')






#o = requests.get(f'http://{ip}/connect')
print('o')