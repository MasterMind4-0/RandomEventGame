from os import stat
import random
import sys
import time
import json

to_be_saved = {
  "health": 20,
  "max_health": 20,
  "cclass": None,
  "name": None,
  'stats': {'strength': 1, 'dexterity': 1, 'charisma': 1, 'intelligence': 1, 'defense': 1, 'wisdom': 1},
  'inventory': []  
}

def start():
  global to_be_saved
  print('Welcome!')
  time.sleep(.5)
  print("To begin the game, we first must create a character, if you have already created one, simply enter that character's name.")
  time.sleep(1)
  to_be_saved['name'] = input("What will be your character's name?\n")
  print('Select your class below:\n')
  to_be_saved['cclass'] = input('''
        Knight - Press K to Select
        - Iron Armor - +.2 Defense
        - Mace - +2 Attack
        - Shield - +.1 Defense
        - Max Health - +2
        - Strength - +.2
        - 15 Coins
        \n
        ''')

  if to_be_saved['cclass'].lower() == 'k':
    to_be_saved['cclass'] = 'Knight'
    to_be_saved['stats']['strength'] += .2
    to_be_saved["max_health"] += 2
    to_be_saved['inventory'] = ['Iron Armor', 'Mace', 'Shield']
    to_be_saved['stats']['defense'] += .3
    print('You have chosen the Knight!')
    print(to_be_saved)
    with open(f'{to_be_saved["name"]}.json', 'w') as file:
      json.dump(to_be_saved, file)

  print('Now that you have your character... Let us begin!')
  random_event_picker()

def random_event_picker():
  events = [(tavern, travling_merchant)]
  random.choice(events)

def tavern():
  print('You entered tavern.')

def travling_merchant():
  print('A merchant, with his backpack filled to the brim with items, comes toward you.')
  time.sleep(1)
  t = input('"Well hello there! Care to look in my shop?" (Y/N)\n')
  if t.lower() == 'y':
    print('The merchant smiles,')
    time.sleep(.25)
    print('"Wonderful! See what you like."')
    time.sleep(1)
    merchant_shop()
  else:
    if to_be_saved['stats']['wisdom'] >= 2:
      print("You see the merchant's smile fade subtly as you continue your travels.")
      
start()