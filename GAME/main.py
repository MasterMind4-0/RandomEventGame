import time
import random

def generate_healing():
    healing = random.randint(1, 5)
    return healing

weapons_data = {
    'iron_shortsword': {'name': 'iron_shortsword', 'Damage': 2, 'Durability': 15, 'price': 15},
    'crossbow': {'name': 'crossbow', 'Damage': 3, 'Durability': 10, 'price': 15},
}

item_data = {
    'health_potion': {'Healing': generate_healing(), 'price': 5}
}

bar_drinks = {
    'rum': {'name': 'Rum', 'drunk_effective': .7, 'price': 3},
    'dragons_blood': {'name': "Dragon's Blood", 'drunk_effective': .99, 'price': 6}
}

player_stats = {
    'strength': 0,
    'constitution': 0
}

name = None
health = 20
dev_mode_enabled = True
inventory = ["health_potion ", "chain_mail"]
weapon = 'iron_shortsword'
weapon_durability = 15
coin  = 100

bartalk_name = None

def wait():
    print('.\n')
    time.sleep(1)
    print('..\n')
    time.sleep(1)
    print('...\n')
    time.sleep(1)

def healthcap():
    global health
    if health > 20:
        health = 20


class battle:
    def __init__(self, attackers_name: str, attackers_health: int, attackers_damage: int):
        self.attackers_name: str = attackers_name
        self.attackers_health: int = attackers_health
        self.attackers_damage: int = attackers_damage

    def fight(self):
        global health, weapon_durability, inventory, weapon, healthp_amount
        done_durability = 0

        while health >= 1:
            weapon_durability -= done_durability
            done_durability = 0

            if self.attackers_health <= 0:
                print("You won the fight!")
                break

            time.sleep(1)

            X = input(f"""
            Your health: {health}

            Inventory: {inventory}
            Weapon: {weapon}

            You have {healthp_amount} health potions. use one? (Type hp)

            Type W to continue the battle\n""")

            if X.lower() == 'hp':
                health += item_data['health_potion']['Healing']
                inventory.remove('health_potion')
                healthcap()
                print("Consuming one health potion...")
                time.sleep(1)
                print(f"You now have {health} health and {healthp_amount} health potions.")
            else:
                print("\n")

            print(f"The {self.attackers_name} charges towards you,")
            time.sleep(.5)
            hitq = random.randint(1, 10)
            if hitq > 5:
                self.attacker_health -= weapons_data[weapon]['Damage']
                done_durability = done_durability - 2
                print(f"The {self.attackers_name} missed! Giving you the opportunity to attack!")
                time.sleep(1)
                if dev_mode_enabled:
                    print(f"The {self.attackers_name} has {self.attacker_health} left!")
                    print(f"Done durability: {done_durability}\nweapon durability: {weapon_durability}")
            else:
                health -= self.attackers_damage
                print(f"The {self.attackers_name} hit you!")
                time.sleep(.5)
                print(f"You have {health} health left!")

        if health >= 1:
            print("Victory!")
        else:
            print("You died!")


def random_event_picker():
    global healthp_amount, inventory, weapon, health, weapon_durability
    wait()
    while 1 == 1:
        healthcap()
        healthp_amount = inventory.count('health_potion')
        if type(weapon_durability) is float:
            weapon_durability.round()

        X = input(f'''


health: {health}
health potions: {healthp_amount}

equiped weapon: {weapon}
inventory: {inventory}
coin amount: {coin}

Actions:
1. Continue walking
2. Take health potion\n
''')
        if X == '1':
            events = [tavern, kidnappers]
            random.choice(events)()
        elif X == '2':
            health += item_data['health_potion']['Healing']
            inventory.remove('health_potion')
            healthcap()
            print('Consuming one health potion...')
            time.sleep(1)

def start():
    global name
    print('Hello!')
    time.sleep(.5)
    print('Are you ready for an adventure??')
    time.sleep(.5)
    print('Yeah, I thought you were.')
    print("Ok, first, let's create your character:")
    name = input("What will your character's name be?\n")
    print(f"That's not a bad name, {name}!")
    time.sleep(.5)
    print('Well, that is all, let us begin!')
    random_event_picker()

def tavern():
    global bartalk_name
    namelist = ['Sophia', 'Timmy', 'Alex', 'Steve', 'Boldimore']
    print('You entered tavern.')
    time.sleep(2)
    print('As you enter, the whiff of alcohol and sweat fills your nose,')
    time.sleep(1)
    print('\033[3mBartender\033[0m: Welcome!')
    time.sleep(1)
    Choice = input('Walk to the bartender or talk to some folk (1 or 2? L for leave.)\n')

    if Choice == '1':
        print('\033[3m"Let me see what the bartender offers."\033[0m')
        bartender()

    elif Choice == "2":
        un = '\033[3mUnknown\033[0m'
        bartalk_name = random.choice(namelist)
        print(f"{name}: Hey! You there!")
        time.sleep(2)
        print(f'{un} looks at you.')
        time.sleep(2)
        print(f'{un}: What do you want?')
        bartalk()

    else:
        print('\033[3m"Nope, not today."\033[0m')
        time.sleep(2)
        print('You turn around and walk straight out.')
        random_event_picker()

def bartalk():
    wait()
    print(f'You sit next to {bartalk_name}.')
    time.sleep(1)
    print(f'\033[3m{bartalk_name}\033[0m: The name is {bartalk_name} you know...')
    time.sleep(2)

    while True:
        y1 = input('Where am I, who are you, what do they sell, or leave? (1, 2, 3, or 4?)\n')

        if y1 == "1":
            print(f"\033[3m{bartalk_name}\033[0m: Welcome to \033[3mTishun Village\033[0m.")
            time.sleep(2)
            print(f'\033[3m{bartalk_name}\033[0m: I guess it is pretty cool...')

        elif y1 == "2":
            print(f"\033[3m{bartalk_name}\033[0m: As I said, it's \033[3m{bartalk_name}\033[0m.")
            if bartalk_name.lower() == "sophia":
                print(f"\033[3m{name}\033[0m: Hey I know someone as Sophia!")
                time.sleep(1)
                print(f'\033[3m{bartalk_name}\033[0m: Cool?')

        elif y1 == "3":
            print(f"\033[3m{bartalk_name}\033[0m looks you dead in the eyes.")
            time.sleep(2)
            print(f"\033[3m{bartalk_name}\033[0m: BEER")
            time.sleep(2)
            print(f"\033[3m{bartalk_name}\033[0m: ...And some food.")
            time.sleep(2)
            print(f"\033[3m{bartalk_name}\033[0m: I heard he is even looking for a hire.")

        elif y1 == "4":
            print(f'{name}: Thanks for the talk.\nYou say as you leave.')
            wait()
            tavern()

        else:
            print('Invalid')

def bartender():
    btgreetings = ['How are you doing today?', 'What can I get you?', "We don't have virgin here for the record.", "I feel sorry for people who don't drink. When they wake up in the morning, that's as good as they're going to feel all day."]
    btbuydrink = ['That there is a good drink.', 'You vomit outside, not on me, got it?', 'Your order.']
    btleave = ['Pleasure doing business.', 'Hope to see you again.', 'Until you order again.']
    choice_of_greeting = random.choice(btgreetings)
    bt = '\033[3mBartender\033[0m'

    print(f'{bt}: {choice_of_greeting}')
    wait()
    while True:
        choice_of_leave = random.choice(btleave)
        choice_of_buydrink = random.choice(btbuydrink)

        menu_entry = input('''
Bartender's menu

1. Rum
2. Wine

HS. HOUSE SPECIAL: Dragon Blood

This ale is dark and thick and a little bitter with a smoky after taste, an acquired taste for many. The bartender warns you that this drink will certainly leave you wasted.
                       
L for leave\n''')
    
        if menu_entry == '1':
            print(f'{bt}: {choice_of_buydrink}')
            time.sleep(1)

            print('You take hold of your drink,')
            time.sleep(1)
            t = input('\033[3m"Should I drink it, or should I take it with me?"\033[0m (Take or drink?)')
            if t == 'drink':
                print('You lift you chin and gulp the liquor to the last drop.')
                time.sleep(1)
            else:
                inventory.append('Rum')
                print(f"\033[3m{name}\033[0m: I'll take this to go.")
                time.sleep(1)
                print(f'{bt}: As long as you use your own glass am fine with it.')
                time.sleep(1)
        
        elif menu_entry == '2':
            print(f'{bt}: {choice_of_buydrink}')
            time.sleep(1)

            print('You take hold of your drink,')
            time.sleep(1)
            t = input('\033[3m"Should I drink it, or should I take it with me?"\033[0m (Take or drink?)')
            if t == 'drink':
                print('You sip your wine gently, soaking in the flavor and aroma.')
                time.sleep(1)
            else:
                inventory.append('Wine')
                print(f"\033[3m{name}\033[0m: I'll take this to go.")
                time.sleep(1)
                print(f'{bt}: As long as you use your own glass am fine with it.')
                time.sleep(1)

        elif menu_entry.lower() == 'hs':
            if coin < 6:
                print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
            else:
                drunk_chance = bar_drinks['dragons_blood']['drunk_effective'] - (player_stats['constitution'] / 10)
                random_value = random.random()
                if random_value < drunk_chance:
                    wasted = True
                    if dev_mode_enabled:
                        print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")
                else:
                    wasted = False
                    if dev_mode_enabled:
                        print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")


                print(f'{bt}: {choice_of_buydrink}')
                time.sleep(1)

                print('You take hold of your drink,')
                time.sleep(1)
                print('You shakely bring the glass to your lips, as you take the first sip, and instant sharp flavor bursts in your mouth.')
                time.sleep(1)
                print('Over time, the drink becomes more tame, and you notice more of the smoky flavor profile.')
                time.sleep(1)
                if wasted:
                    print('But, alas, it still hits your stomach with such force, you can barely finish.')
                    time.sleep(1)
                    print('Before you know it, your in the back alley of the tavern.')
                else:
                    player_stats['constitution'] += .02
                    print(f"{bt}: Well, I would not have guessed you'd be able to stand after that,")
        
        elif menu_entry.lower() == 'l':
            print(f'\033[3m{name}\033[0m: Thank you, but I think I am OK.')
            time.sleep("1")
            print(f'{bt}: {choice_of_leave}')
            tavern()
            

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
        print('The merchant wonders away in solom.')

def merchant_shop():
    global coin
    trader_prompts = ['What can I do you for?', 'What will it be today?', 'Anything catching your eye?']
    weapons_list = list(weapons_data.values())
    item1 = random.choice(weapons_list)
    item2 = random.choice(weapons_list)
    item3 = random.choice(weapons_list)
    while 1 > 0:
        trader_prompt = random.choice(trader_prompts)
        print('1. Buy items')
        print('2. Sell items')
        print('3. Leave')
        t = input('')
        if t == '1':
            traded = True
            print(trader_prompt)
            print(f'''
Merchant's shop
            
1. {item1['name']}

2. {item2['name']}

3. {item3['name']}


Coin: {coin}

Inventory: {inventory}\n
''')
        elif t =='2':
            traded = True
            print(trader_prompt)
            sell = input(f'''
Selling

Inventory: {inventory}

Type the name of the item you'd like to sell\n
''')
            if sell in inventory:
                item = weapons_data[sell]
                original_price = item['price']
                durability_percentage = (item['Durability'] / weapon_durability) * 100
                selling_price = original_price * (durability_percentage / 100)
                coin += selling_price
                inventory.remove(sell)
                print(f"You sold {sell} for {selling_price} coins.")
            else:
                print("You don't have that item.")
        
        elif t == '3' or t.lower() == 'l':
            if traded:
                print('The merchant waves goodbye as you leave.')
            else:
                print('You leave as the merchant sighs.')

def kidnappers():
    print('As you walk along the weaving path in the forest,')
    time.sleep(1)
    print('A group of thugs jumps from the bushes.')
    time.sleep(1)
    print("THUG: Get em boys!")
    thug_fight()

def thug_fight():
    thug_fight = battle('Thugs', 10, 2)

    thug_fight.fight()

start()