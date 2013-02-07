from brisk import *
from brisk.bots import *
import argparse
from pprint import pprint
from time import sleep

def main(args):
    # if args.game_id:
    #     brisk = Brisk(game_id=args.game_id)
    brisks = []
    brisks.append(Brisk('bot A'))
    brisks.append(Brisk('bot B'))

    brisks[0].create_new_game()
    brisks[1].join_game(brisks[0].game_id)

    map_layout = brisks[0].get_map_layout()
    initial_game_state = brisks[0].get_game_state()

    bots = []
    bots.append(BriskBotB(map_layout=map_layout, initial_game_state=initial_game_state))
    bots.append(SimpleBot(map_layout=map_layout, initial_game_state=initial_game_state))

    brisk_observer = BriskObserver()

    i = 0
    while True:

        bot = bots[i]
        brisk = brisks[i]

        player_status = brisk.get_player_status()

        if player_status['eliminated']:
            print 'Player eliminated'
            break

        if not player_status['current_turn']:
            i = (i + 1) % 2
            sleep(1)
            continue

        action, params = bot.compute_next_action(brisk.player_id, brisk.get_player_status(), brisk.get_game_state())

        print 'bot ', i, 'does', action, params

        if action == 'place_armies':
            brisk.place_armies(params['territory_id'], params['num_armies'])
        elif action == 'attack':
            brisk.attack(params['attacker_territory_id'], params['defender_territory_id'], params['num_attacker_armies'])
        elif action == 'transfer_armies':
            i = (i + 1) % 2
            brisk.transfer_armies(params['from_territory_id'], params['to_territory_id'], params['num_armies'])
        elif action == 'end_turn':
            i = (i + 1) % 2
            brisk.end_turn()
        
        brisk_observer.update(brisk)


parser = argparse.ArgumentParser()
parser.add_argument('-g', '--game-id', dest='game_id', type=int)
parser.set_defaults(func=main)

args = parser.parse_args()
args.func(args)
