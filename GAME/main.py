import time
import random


def generate_healing():
    healing = random.randint(1, 5)
    return healing


items = {
    'weapons': {
        'iron_shortsword': {
            'name': 'iron_shortsword',
            'Damage': 2,
            'price': 15
        },
        'crossbow': {
            'name': 'crossbow',
            'Damage': 3,
            'price': 15
        },
    },
    'items': {
        'health_potion': {
            'name': 'health_potion',
            'Healing': generate_healing(),
            'price': 5
        },
    },
    'drinks': {
        'rum': {
            'name': 'Rum',
            'drunk_effective': .7,
            'price': 3
        },
        'dragons_blood': {
            'name': "Dragon's Blood",
            'drunk_effective': .99,
            'price': 6
        }
    }
}

player_stats = {'strength': 0.0, 'constitution': 0.0}

name = None
health = 20
dev_mode_enabled = True
inventory = ["health_potion", "chain_mail"]
weapon = 'iron_shortsword'
coin = 100

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

class shop():
    def __init__(self, name: str, item_pool: list = None):
        self.name: str = name

        if item_pool:
            self.item_pool = item_pool
        else:
            self.item_pool = []

            shop_type = random.choice(list(items.keys()))
            self.item_pool.extend(items[shop_type].values())

            while len(self.item_pool) < 3:
                additional_shop_type = random.choice(list(items.keys()))
                self.item_pool.extend(items[additional_shop_type].values())

        self.item1 = random.choice(self.item_pool)
        self.item2 = random.choice(self.item_pool)
        self.item3 = random.choice(self.item_pool)

        while self.item2 == self.item1:
            self.item2 = random.choice(self.item_pool)
        while self.item3 in (self.item1, self.item2):
            self.item3 = random.choice(self.item_pool)


    def shop_menu(self):
        global coin, inventory
        traded = False
        trader_prompts = ['What can I do you for?', 'What will it be today?', 'Anything catching your eye?']

        while True:
            trader_prompt = random.choice(trader_prompts)
            print(f'''
             {self.name}

            1. {self.item1['name']} ({self.item1['price']} coins)
            2. {self.item2['name']} ({self.item2['price']} coins)
            3. {self.item3['name']} ({self.item3['price']} coins)

            Coin: {coin}

            Inventory: {inventory}\n
            ''')
            print('1. Buy items')
            print('2. Sell items')
            print('\nPress ENTER to leave')
            t = input('')
            if t == '1':
                print(trader_prompt)
                time.sleep(1)
                bought_item = input(
                    'What would you like to buy? (1, 2, or 3?)\n')

                if bought_item == '1' and coin >= self.item1['price']:
                    traded = True
                    coin -= self.item1['price']
                    inventory.append(self.item1['name'])
                    print(f'You bought a {self.item1["name"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')

                elif bought_item == '2' and coin >= self.item2['price']:
                    traded = True
                    coin -= self.item2['price']
                    inventory.append(self.item2['name'])
                    print(f'You bought a {self.item2["name"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')

                elif bought_item == '3' and coin >= self.item3['price']:
                    traded = True
                    coin -= self.item3['price']
                    inventory.append(self.item2['name'])
                    print(f'You bought a {self.item3["name"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')

                else:
                    print('You do not have enough money to buy that item.')

            elif t == '2':
                print(trader_prompt)
                sell = input(f'''
        Selling

        Inventory: {inventory}

        Type the name of the item you'd like to sell\n
            ''')
                sell = sell.strip().lower().replace(" ", "")

                if sell in inventory:
                    traded = True

                    for item_category in items.items():
                        if sell in item_category:
                            item = item_category[sell]
                            original_price = item['price']
                            selling_price = original_price / 2

                            coin += selling_price
                            inventory.remove(sell)
                            print(
                                f"You sold {sell} for {selling_price} coins.")
                            break
                    else:
                        print("ERROR: Item doesn't exist in items.")
                else:
                    print("You don't have that item.")

            elif X == '':
                if traded:
                    print('The merchant waves goodbye as you leave.')
                    random_event_picker()
                else:
                    print('You leave as the merchant sighs.')
                    random_event_picker()
            else:
                pass


class battle:

    def __init__(self, attackers_name: str, attackers_health: int, attackers_damage: int, reward_gold: int, reward_item: str, exp: float, type_exp: str):
        self.attackers_name: str = attackers_name
        self.attackers_health: int = attackers_health
        self.attackers_damage: int = attackers_damage
        self.reward_gold: int = reward_gold
        self.reward_item: str = reward_item
        self.exp: float = exp
        self.type_exp: str = type_exp

    def fight(self):
        global health, inventory, weapon, healthp_amount, coin, player_stats

        while health >= 1:

            if self.attackers_health <= 0:
                player_stats[self.type_exp] += self.exp
                print("You won the fight!")
                if self.reward_item:
                    inventory.append(self.reward_item)
                    print(f'You are award with a {self.reward_item}')
                else:
                    pass
                if self.reward_gold:
                    coin += self.reward_gold
                    print(f"You are award with {self.reward_gold} coins!")
                else:
                    pass
                break

            time.sleep(1)

            X = input(f"""
        Your health: {health}

        Inventory: {inventory}
        Weapon: {weapon}

        Actions:

        Hit ENTER to continue walking

        1. Take health potion (You have {healthp_amount})
        2. Switch equiped weapon\n
""")

            if X.lower() == '1':
                health += items['items']['health_potion']['healing']
                inventory.remove('health_potion')
                healthcap()
                print("Consuming one health potion...")
                time.sleep(1)
                print(f"You now have {health} health and {healthp_amount} health potions.")
            elif X.lower() == '2':
                switched_weapon = input(
                    'What weapon would you like to switch to?\n')
                switched_weapon = switched_weapon.strip().lower()
                if switched_weapon in inventory:
                    inventory.append(weapon)
                    weapon = switched_weapon
                else:
                    print("You don't have that weapon.")
            elif X == '':
                print(f"The {self.attackers_name} charges towards you,")
                time.sleep(.5)
                hitq = random.randint(1, 10)
                if hitq > 5:
                    self.attackers_health -= items['weapons'][weapon]['Damage']
                    print(f"The {self.attackers_name} missed! Giving you the opportunity to attack!")
                    time.sleep(1)
                    if dev_mode_enabled:
                        print(f"The {self.attackers_name} has {self.attackers_health} left!")
                else:
                    health -= self.attackers_damage
                    print(f"The {self.attackers_name} hit you!")
                    time.sleep(.5)
                    print(f"You have {health} health left!")
            else:
                pass

        if health >= 1:
            print("Victory!")
        else:
            print("You died!")


def random_event_picker():
    global healthp_amount, inventory, weapon, health
    wait()
    while True:
        healthcap()
        healthp_amount = inventory.count('health_potion')
        X = input(f'''


        Health: {health}
        Health potions: {healthp_amount}

        Equiped weapon: {weapon}

        Inventory: {inventory}
        Coin amount: {coin}

        Actions:

        Hit ENTER to continue walking

        1. Take health potion
        2. Switch equiped weapon\n
''')
        if X == '1':
            health += items['items']['health_potion']['healing']
            inventory.remove('health_potion')
            healthcap()
            print('Consuming one health potion...')
            time.sleep(1)
        elif X == '2':
            switched_weapon = input(
                'What weapon would you like to switch to?\n')
            if switched_weapon in inventory:
                inventory.append(weapon)
                weapon = switched_weapon
            else:
                print("You don't have that weapon.")
        elif X == '':
            events = [travling_merchant, tavern, kidnappers, town]
            random.choice(events)()
        else:
            pass
            

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
    print('You entered tavern.')
    time.sleep(2)
    print('As you enter, the whiff of alcohol and sweat fills your nose,')
    time.sleep(1)
    print('\033[3mBartender\033[0m: Welcome!')
    time.sleep(1)
    Choice = input(
        'Walk to the bartender or talk to some folk (1 or 2? L for leave.)\n')

    if Choice == '1':
        print('\033[3m"Let me see what the bartender offers."\033[0m')
        bartender()

    elif Choice == "2":
        un = '\033[3mUnknown\033[0m'
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
    namelist = ['Sophia', 'Timmy', 'Alex', 'Steve', 'Boldimore']
    bartalk_name = random.choice(namelist)
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
    btgreetings = ['How are you doing today?', 'What can I get you?',"We don't have virgin here for the record.","I feel sorry for people who don't drink. When they wake up in the morning, that's as good as they're going to feel all day."]
    btbuydrink = ['That there is a good drink.', 'You vomit outside, not on me, got it?','Your order.']
    btleave = ['Pleasure doing business.', 'Hope to see you again.','Until you order again.']
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
                print(
                    'You lift you chin and gulp the liquor to the last drop.')
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
                drunk_chance = items['drinks']['dragons_blood'][
                    'drunk_effective'] - (player_stats['constitution'] / 10)
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
                    back_alley()
                else:
                    player_stats['constitution'] += .02
                    print(f"{bt}: Well, I would not have guessed you'd be able to stand after that,")

        elif menu_entry.lower() == 'l':
            print(f'\033[3m{name}\033[0m: Thank you, but I think I am OK.')
            time.sleep(1)
            print(f'{bt}: {choice_of_leave}')
            tavern()
        
        else:
            pass

def travling_merchant():
    print('A merchant, with his backpack filled to the brim with items, comes toward you.')
    time.sleep(1)
    t = input('"Well hello there! Care to look in my shop?" (Y/N)\n')
    if t.lower() == 'y':
        print('The merchant smiles,')
        time.sleep(.25)
        print('"Wonderful! See what you like."')
        time.sleep(1)
        merchant_shop = shop("Merchant's Shop")
        merchant_shop.shop_menu()
    else:
        print('The merchant wonders away in solom.')

def kidnappers():
    thug_fight = battle('Thugs', 10, 2, 20, "", .04, 'strength')
    print('As you walk along the weaving path in the forest,')
    time.sleep(1)
    print('A group of thugs jumps from the bushes.')
    time.sleep(1)
    print("THUG: Get em boys!")
    thug_fight.fight()

def back_alley():
    global coin
    thug = '\033[3mThug\033[0m'
    thug_leader = '\033[3mThug Leader\033[0m'
    wait()
    print('You awaken in a dark alley way.')
    time.sleep(1)
    print('Your head screams and you mouth thirsts.')
    time.sleep(1)
    print('You notice it is night,')
    time.sleep(1)
    print('As you were looking around, you happened to notice a shadow walking toward you...')
    time.sleep(1)
    print(f"{thug_leader}: Hey, you. The sorry looking filth.")
    time.sleep(1)
    print('You notice two other figures behind the masked fellow.')
    time.sleep(1)
    print(f"\033[0m{name}\033[0m: Just get away from me.")
    time.sleep(1)
    print(f'{thug_leader}: Well! Look at the little rascal!')
    time.sleep(1)
    print(f'{thug}: Fiesty little rascal, he is.')
    time.sleep(.5)
    print('\033[3m"Said on the the figures in the back."\033[0m')
    time.sleep(1)
    print(f"{thug_leader}: Ok, let's cut to the chase, give us everything you got.")
    time.sleep(1)
    print(f"{thug}: And we mean everything!")
    time.sleep(1)
    response = input('Should you fight, give them some stuff, or give them all of your stuff? (1, 2, or 3?)\n')

    if response == '1':
        thug_fight = battle('Thugs', 20, 3, 20, "", .02, 'strength')
        print(f'\033[3m{name}\033[0m: As, I said, back the HELL AWAY!')
        time.sleep(1)
        thug_fight.fight()
    elif response == '2':
        print(f"\033[3m{name}\033[0m: Fine, fine, yes. I'll give my stuff.")
        time.sleep(1)
        while True:
            stuff_given = input(f'''
        Inventory: {inventory}

        What do you give?\n
        ''')
            if stuff_given in inventory and stuff_given in items:
                inventory.remove(stuff_given)
                print(f'\033[3m"You give the {stuff_given} to the men, they look you up and down."\033[0m')
                time.sleep(1)
                print(f"{thug_leader}: Well then, that wasn't too hard now, was it?")
                time.sleep(1)
                print('\033[3m"The thugs disappear into the darkness."\033[0m')
                time.sleep(1)
                print(f'{thug_leader}: Not that hard at all...')
                random_event_picker()
            else:
                print('ERROR: Invalid.')
    elif response == '3':
        inventory.remove(inventory)
        print(f"\033[3m{name}\033[0m: OK, OK! Here.")
        time.sleep(1)
        print('\033[3m"You hand the thugs all your things, they mouths foam with envy. A good haul for them."\033[0m')
        time.sleep(1)
        print(f"{thug_leader}: I need you'd come to your senses friend!")
        time.sleep(.5)
        print(f"{thug_leader}: Yeah, these knuckle-heads didn't believe me, but I knew it." )
        time.sleep(1)
        print(f"{thug_leader}: Well, friend, until we meet again!")
        time.sleep(1)
        print('\033[3m"The thugs disappear into the darkness."\033[0m')
        time.sleep(1)
        print(f'{thug_leader}: Until we meet again...')
        random_event_picker()

def town():

    store1 = shop("Sasha's Weapons", [items['weapons']['iron_shortsword'], items['weapons']['crossbow']])
    store2 = shop("Tintoe's Couldron", [items['items']['health_potion']])

    print('\033[3m"You come across a village, should you enter is the question at hand..."\033[0m')
    time.sleep(1)
    x = input('Do you wish to enter? (Y/N)\n')
    if x.lower() == 'y':
        if 'health_potion' not in inventory:
            print(f'\033[3m{name}\033[0m: I do need some health potions...')
        else:
            print(f'\033[3m{name}\033[0m: I do need some things I am sure...')
    else:
        print(f'\033[3m{name}\033[0m: Ah, I do not need anything...')
        random_event_picker()

    print('\033[3mYou enter the village.\033[0m')
    time.sleep(1)
    while True:
        to_do = input(f'''
        Welcome to town!

        Inventory: {inventory}

        Type LEAVE to continue your journey.

        1. Go to {store1.name}?
        2. Go to {store2.name}?
        3. Go to tavern?\n
        ''')
        if to_do == '1':
            store1.shop_menu()
        elif to_do == '2':
            store2.shop_menu()
        elif to_do == '3':
            tavern()
        elif to_do.lower() == 'leave':
            random_event_picker()
        else:
            print('ERROR: Not an option')
            time.sleep(1)

start()
