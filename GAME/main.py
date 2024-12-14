import time
import random


def generate_healing(x: int, y: int):
    healing = random.randint(x, y)
    return healing


dictitems = {
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
        'dagger': {
            'name': 'dagger',
            'Damage': 1,
            'price': 10
        }
    },
    'items': {
        'health_potion': {
            'name': 'health_potion',
            'healing': generate_healing(1, 5),
            'price': 5
        },
        'greater_health_potion': {
            'name': 'greater_health_potion',
            'healing': generate_healing(1, 10),
            'price': 15
        },
        'greatest_health_potion': {
            'name': 'greatest_health_potion',
            'healing': generate_healing(1, 20),
            'price': 25
        },
    },
    'drinks': {
        'special_drinks': {
            'dragons_blood': {
            'name': "Dragon's Blood",
            'description': "This ale is dark and thick. It's a little bitter with a smokey after taste, an acquired taste for many. The bartender warns you that this drink will certainly leave you wasted.",
            'drunk_effective': .99,
            'exp': .02,
            'price': 6
            },
            'goblin_vomit': {
                'name': 'Goblin Vomit',
                'description': "This dark green that reminds many of goblin vomit. It's surprising thin, for its name, but why many avoid it is because of its horrid bitter taste.",
                'drunk_effective': .99,
                'exp': .03,
                'price': 5
            }
        },
        'rum': {
            'name': 'Rum',
            'drunk_effective': .7,
            'price': 2
        },
        'wine': {
            'name': 'Wine',
            'drunk_effective': .25,
            'price': 3
        },
        'beer': {
            'name': 'Beer',
            'drunk_effective': .6,
            'price': 2
        }

    }
}

player_stats = {'strength': 0.0, 'constitution': 0.0}
name = None
health = 20
dev_mode_enabled = False
inventory = ["health_potion", "chain_mail"]
weapon = 'iron_shortsword'
coin = 100
swear = False
h = 'heck'

def error_found(to_do: str = 'Report the issue in GitHub!', error_name: str = None):
    print(f'###~~~--- ERROR: {error_name} ---~~~###')
    print(to_do)

def death():
    print('You died!')
    start()

def wait():
    if dev_mode_enabled:
        pass
    else:
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

class shop:
    def __init__(self, name: str, categories: list = None, item_pool: list = None):
        self.name: str = name

        if item_pool:
            self.item_pool = item_pool
        else:
            self.item_pool = self.generate_random_item_pool(categories)

        self.item1 = random.choice(self.item_pool)
        self.item2 = random.choice(self.item_pool)
        self.item3 = random.choice(self.item_pool)

    def generate_random_item_pool(self, categories):
        all_items = []
        if categories:
            for category in categories:
                if category in dictitems:
                    all_items.extend(dictitems[category].values())
        else:
            for sub_items in dictitems.values():
                all_items.extend(sub_items.values())
        
        if len(all_items) < 3:
            raise ValueError('ERROR')
        return random.sample(all_items, k=3)

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

                    for item_category in dictitems.items():
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
                        error_found("Try again", 'Item not found')
                else:
                    print("You don't have that item.")

            elif not t:
                if traded:
                    print('The merchant waves goodbye as you leave.')
                    random_event_picker()
                else:
                    print('You leave as the merchant sighs.')
                    random_event_picker()
            else:
                pass

class tavern:
    def __init__(self, special: str = None, item_pool: list = None, name: str = None):
        if not name:
            self.name = 'Tavern'
        else:
            self.name = name

        if not item_pool:
            self.item_pool = self.generate_random_item_pool(dictitems['drinks'], exclude='special_drinks')
        else:
            self.item_pool = item_pool
        self.special = None
        if not self.special:
            self.special = self.generate_random_item_pool(dictitems['drinks']['special_drinks'])
        else:
            self.special = special

        if len(self.item_pool) > 0:
            self.item1 = random.choice(self.item_pool)
            self.item2 = random.choice(self.item_pool)
        else:
            self.item1 = self.item2 = {'name': 'Out of Stock', 'price': 0}

        if len(self.special) > 0:
            self.house_special = random.choice(self.special)
        else:
            self.house_special = {'name': 'Out of Stock', 'price': 0, 'description': 'None available.'}

    def generate_random_item_pool(self, category, exclude=None):
        all_items = []
        for key, value in category.items():
            if key == exclude:
                continue
            if isinstance(value, dict) and 'name' in value:
                all_items.append(value)
        return all_items


    def enter_tavern(self):
        print('You entered tavern.')
        time.sleep(2)
        print('As you enter, the whiff of alcohol and sweat fills your nose,')
        time.sleep(1)
        print('\033[3mBartender\033[0m: Welcome!')
        time.sleep(1)
        Choice = input('Walk to the bartender or talk to some folk (1 or 2? L for leave.)\n')

        if Choice == '1':
            print('\033[3m"Let me see what the bartender offers."\033[0m')
            self.bartender()

        elif Choice == "2":
            un = '\033[3mUnknown\033[0m'
            print(f"{name}: Hey! You there!")
            time.sleep(2)
            print(f'{un} looks at you.')
            time.sleep(2)
            print(f'{un}: What do you want?')
            self.bartalk()

        else:
            print('\033[3m"Nope, not today."\033[0m')
            time.sleep(2)
            print('You turn around and walk straight out.')
            random_event_picker()

    def return_tavern(self):
        Choice = input('Walk to the bartender or talk to some folk (1 or 2? L for leave.)\n')

        if Choice == '1':
            self.bartender()

        elif Choice == "2":
            un = '\033[3mUnknown\033[0m'
            print(f"{name}: Hey! You there!")
            time.sleep(2)
            print(f'{un} looks at you.')
            time.sleep(2)
            print(f'{un}: What do you want?')
            self.bartalk()

        else:
            print('\033[3m"I have had enough."\033[0m')
            time.sleep(2)
            print('You turn around and walk straight out.')
            random_event_picker()
            
    def bartalk(self):
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

            elif y1 == "4":
                print(f'{name}: Thanks for the talk.\nYou say as you leave.')
                wait()
                self.return_tavern()

            else:
                print('Invalid')

    def bartender(self):
        global coin
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

            menu_entry = input(f'''
        {self.name}'s menu

        1. {self.item1['name']} ({self.item1['price']} coins)
        2. {self.item2['name']} ({self.item2['price']} coins)

        For HOUSE SPECIAL, type HS: {self.house_special['name']} ({self.house_special['price']} coins)

        {self.house_special['description']}

        ENTER to leave\n''')

            if menu_entry == '1':
                if coin < self.item1['price']:
                    print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
                else:
                    drunk_chance = dictitems['drinks'][self.item1]['drunk_effective'] - (player_stats['constitution'] / 10)
                    random_value = random.random()
                    if random_value < drunk_chance:
                        wasted = True
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")
                    else:
                        wasted = False
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")

                coin -= self.item1['price']
                print(f'{bt}: {choice_of_buydrink}')
                time.sleep(1)
                print('You take hold of your drink,')
                time.sleep(1)
                if wasted and self.item1 == 'wine':
                    print('You gently sip your drink,')
                    time.sleep(1)
                    print('But before long, you feel tipsy.')
                    time.sleep(1)
                    print('The last thing you hear before passing out is the bartender.')
                    time.sleep(1)
                    print(f"{bt}: How the {h} do you pass out from bloody wine?")
                    back_alley()
                elif self.item1 == 'wine':
                    print('You sip your wine gently, soaking in the flavor and aroma.')
                    time.sleep(1)
                elif wasted:
                    print('After downing your mug, you can barely stand.')
                    time.sleep(1)
                    print('You drunkly walk outside, before you pass out.')
                    back_alley()
                else:
                    print('You lift you chin and gulp the liquor to the last drop.')
                    time.sleep(1)


            elif menu_entry == '2':
                if coin < self.item2['price']:
                    print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
                else:
                    drunk_chance = dictitems['drinks'][self.item2]['drunk_effective'] - (player_stats['constitution'] / 10)
                    random_value = random.random()
                    if random_value < drunk_chance:
                        wasted = True
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")
                    else:
                        wasted = False
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")

                coin -= self.item2['price']
                print(f'{bt}: {choice_of_buydrink}')
                time.sleep(1)
                print('You take hold of your drink,')
                time.sleep(1)
                if wasted and self.item2 == 'wine':
                    print('You gently sip your drink,')
                    time.sleep(1)
                    print('But before long, you feel tipsy.')
                    time.sleep(1)
                    print('The last thing you hear before passing out is the bartender.')
                    time.sleep(1)
                    print(f"{bt}: How the hell do you pass out from bloody wine?")
                    back_alley()
                elif self.item2 == 'wine':
                    print('You sip your wine gently, soaking in the flavor and aroma.')
                    time.sleep(1)
                elif wasted:
                    print('After downing your mug, you can barely stand.')
                    time.sleep(1)
                    print('You drunkly walk outside, before you pass out.')
                    back_alley()
                else:
                    print('You lift you chin and gulp the liquor to the last drop.')
                    time.sleep(1)


            elif menu_entry.lower() == 'hs':
                if coin < self.house_special['price']:
                    print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
                else:
                    drunk_chance = self.house_special['drunk_effective'] - (player_stats['constitution'] / 10)
                    random_value = random.random()
                    if random_value < drunk_chance:
                        wasted = True
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")
                    else:
                        wasted = False
                        if dev_mode_enabled:
                            print(f"drunk chance: {drunk_chance}\ncompared value: {random_value}")

                    coin -= self.house_special['price']
                    print(f'{bt}: {choice_of_buydrink}')
                    time.sleep(1)
                    print('You take hold of your drink,')
                    time.sleep(1)
                    print('You shakely bring the glass to your lips, as you take the first sip, and instant sharp flavor bursts in your mouth.')
                    time.sleep(1)
                    print('Over time, the drink becomes more tame, and you notice more of its flavor profile.')
                    time.sleep(1)
                    if wasted:
                        print('But, alas, it still hits your stomach with such force, you can barely finish.')
                        back_alley()
                    else:
                        if dev_mode_enabled:
                            print(f'Previous constitution score: {player_stats["constitution"]}')
                            print(f'Applied exp: {self.house_special['exp']}')
                            player_stats['constitution'] += self.house_special['exp']
                            print(f'After: {player_stats["constitution"]}')
                        else:
                            player_stats['constitution'] += self.house_special['exp']
                        print(f"{bt}: Well, I would not have guessed you'd be able to stand after that,")
                        time.sleep(1)

            elif not menu_entry:
                print(f'\033[3m{name}\033[0m: Thank you, but I think I am OK.')
                time.sleep(1)
                print(f'{bt}: {choice_of_leave}')
                self.return_tavern()
            
            else:
                pass

class battle:

    def __init__(self, attackers_name: str, attackers_health: int, attackers_damage: int, type_exp: str, reward_gold: int = None, reward_item: str = None):
        self.attackers_name: str = attackers_name
        self.attackers_health: int = attackers_health
        self.attackers_damage: int = attackers_damage
        self.exp: float = self.attackers_health * .02
        self.type_exp: str = type_exp
        if not reward_item:
            self.reward_item = False
        else:
            self.reward_item: str = reward_item
        if not reward_gold:
            self.reward_gold = attackers_health * .4
            self.reward_gold = round(self.reward_gold)
        else:
            self.reward_gold: int = reward_gold

    def fight(self):
        global health, inventory, weapon, healthp_amount, coin, player_stats

        if dev_mode_enabled:
            sim_question = input('Would you prefer to simulate a battle instead? (Y/N)\n')
            if sim_question.lower() == 'y':
                self.simulate_fight()
                return

        while health > 0:
            healthp_amount = inventory.count('health_potion')

            if self.attackers_health <= 0:
                player_stats[self.type_exp] += self.exp
                print("You won the fight!")
                if self.reward_item:
                    inventory.append(self.reward_item)
                    print(f'You are awarded with a {self.reward_item}!')
                if self.reward_gold:
                    coin += self.reward_gold
                    print(f"You are awarded with {self.reward_gold} coins!")
                return

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
                if 'health_potion' in inventory:
                    health += dictitems['items']['health_potion']['healing']
                    inventory.remove('health_potion')
                    healthcap()
                    print("Consuming one health potion...")
                    time.sleep(1)
                    print(f"You now have {health} health and {inventory.count('health_potion')} health potions left.")
                else:
                    print("You don't have any health potions!")
            elif X.lower() == '2':
                switched_weapon = input(
                    'What weapon would you like to switch to?\n')
                switched_weapon = switched_weapon.strip().lower()
                if switched_weapon in inventory:
                    inventory.append(weapon)
                    weapon = switched_weapon
                else:
                    print("You don't have that weapon.")
            elif not X:
                print(f"The {self.attackers_name} charges towards you,")
                time.sleep(.5)
                hitq = random.randint(1, 10)
                if hitq > 5:
                    self.attackers_health -= dictitems['weapons'][weapon]['Damage']
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

        death()

    def simulate_fight(self):
        global health, inventory, weapon, healthp_amount, coin, player_stats
        healthp_amount = inventory.count('health_potion')
        health_point = input('What should health be before you take a health potion?\n')
        reward_yes = input('Receive rewards? (Y/N)\n')
        reward_yes = reward_yes.lower() == 'y'

        while health > 0:

            if self.attackers_health <= 0:
                player_stats[self.type_exp] += self.exp
                print("You won the fight!")
                if self.reward_item and reward_yes:
                    inventory.append(self.reward_item)
                    print(f'You are awarded with a {self.reward_item}!')
                if self.reward_gold and reward_yes:
                    coin += self.reward_gold
                    print(f"You are awarded with {self.reward_gold} coins!")
                return

            if health <= round(int(health_point)):
                if 'health_potion' in inventory:
                    health += dictitems['items']['health_potion']['healing']
                    inventory.remove('health_potion')
                    healthcap()
                else:
                    pass

            hitq = random.randint(1, 10)
            if hitq > 5:
                self.attackers_health -= dictitems['weapons'][weapon]['Damage']
            else:
                health -= self.attackers_damage
        else:
            pass

        death()

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
            health += dictitems['items']['health_potion']['healing']
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
        elif not X:
            events = [travling_merchant, tavern1, kidnappers, town]
            random.choice(events)()
        else:
            pass
            
def start():
    global player_stats, name, health, dev_mode_enabled, inventory, weapon, coin, h, swear
    player_stats = {'strength': 0.0, 'constitution': 0.0}
    name = None
    health = 20
    dev_mode_enabled = False
    inventory = ["health_potion", "chain_mail"]
    weapon = 'iron_shortsword'
    coin = 0
    print('Hello!')
    time.sleep(.5)
    print('Are you ready for an adventure??')
    time.sleep(.5)
    print('Yeah, I thought you were.')
    print("Ok, first, let's create your character:")
    name = input("What will your character's name be?\n")
    if name.lower() == 'dev':
        dev_mode_enabled = True
    elif name.lower() == 'dez':
        dev_mode_enabled = True
        swear = True
    print(f"That's not a bad name, {name}!")
    time.sleep(.5)
    print('Well, that is all, let us begin!')
    if swear:
        h = 'hell'
    random_event_picker()

def tavern1():
    tavern_ = tavern()
    tavern_.enter_tavern()

def travling_merchant():
    print('A merchant, with his backpack filled to the brim with items, comes toward you.')
    time.sleep(1)
    t = input('"Well hello there! Care to look in my shop?" (Y/N)\n')
    if t.lower() == 'y':
        merchant_shop = shop("Merchant's Shop", ['weapon', 'items'])
        print('The merchant smiles,')
        time.sleep(.5)
        print('"Wonderful! See what you like."')
        time.sleep(1)
        merchant_shop.shop_menu()
    else:
        print('The merchant wonders away in solom.')

def kidnappers():
    kidnappers_fight = battle('Thugs', 10, 2, 'strength')
    print('As you walk along the weaving path in the forest,')
    time.sleep(1)
    print('A group of thugs jumps from the bushes.')
    time.sleep(1)
    print("\033[3mThugs\033[0m: Get em boys!")
    kidnappers_fight.fight()

def back_alley():
    global coin
    thug = '\033[3mThug\033[0m'
    thug_leader = '\033[3mThug Leader\033[0m'
    wait()
    print('You awaken in a dark alley way.')
    time.sleep(2)
    print('Your head screams and you mouth thirsts.')
    time.sleep(2)
    print('You notice it is night,')
    time.sleep(2)
    print('As you were looking around, you happened to notice a shadow walking toward you...')
    time.sleep(2)
    print(f"{thug_leader}: Hey, you. The sorry looking filth.")
    time.sleep(2)
    print('You notice two other figures behind the masked fellow.')
    time.sleep(2)
    print(f"\033[0m{name}\033[0m: Just get away from me.")
    time.sleep(2)
    print(f'{thug_leader}: Well! Look at the little rascal!')
    time.sleep(2)
    print(f'{thug}: Feisty little rascal, he is.')
    time.sleep(2)
    print('\033[3m"Said the figures in the back."\033[0m')
    time.sleep(2)
    print(f"{thug_leader}: Ok, let's cut to the chase, give us everything you got.")
    time.sleep(2)
    print(f"{thug}: And we mean everything!")
    time.sleep(2)
    response = input('Should you fight, give them some stuff, or give them all of your stuff? (1, 2, or 3?)\n')

    if response == '1':
        thug_fight = battle('Thugs', 20, 3, 'strength')
        print(f'\033[3m{name}\033[0m: As, I said, back the {h.upper()} AWAY!')
        time.sleep(2)
        thug_fight.fight()
    elif response == '2':
        print(f"\033[3m{name}\033[0m: Fine, fine, yes. I'll give my stuff.")
        time.sleep(1)
        while True:
            stuff_given = input(f'''
        Inventory: {inventory}

        What do you give?\n
        ''')
            if stuff_given.lower() in inventory and stuff_given in dictitems:
                inventory.remove(stuff_given.lower())
                print(f'\033[3m"You give the {stuff_given} to the men, they look you up and down."\033[0m')
                time.sleep(1)
                print(f"{thug_leader}: Well then, that wasn't too hard now, was it?")
                time.sleep(1)
                print('\033[3m"The thugs disappear into the darkness."\033[0m')
                time.sleep(1)
                print(f'{thug_leader}: Not that hard at all...')
                random_event_picker()
            else:
                error_found("Try again", "Invalid option")
    elif response == '3':
        inventory = []
        print(f"\033[3m{name}\033[0m: OK, OK! Here.")
        time.sleep(1)
        print('\033[3m"You hand the thugs all your things, their mouths foam with envy. A good haul for them."\033[0m')
        time.sleep(1)
        print(f"{thug_leader}: I knew you'd come to your senses friend!")
        time.sleep(.5)
        print(f"{thug_leader}: Yeah, these knuckle-heads didn't believe me, but I knew it." )
        time.sleep(1)
        print(f"{thug_leader}: Well, friend, until we meet again!")
        time.sleep(1)
        print('\033[3m"The thugs disappear into the darkness."\033[0m')
        time.sleep(1)
        print(f'{thug_leader}: Until we meet again...')
        random_event_picker()
    else:
        error_found('Try again', 'Invalid option')

def town():
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
    store1 = shop("Sasha's", ['weapon', 'items'])
    store2 = shop("Tintoe's General", ['weapons', 'items'])
    time.sleep(1)
    while True:
        to_do = input(f'''
        Welcome to town!

        Inventory: {inventory}

        Hit ENTER to continue your journey.

        1. Go to {store1.name}?
        2. Go to {store2.name}?
        3. Go to local tavern?\n
        ''')
        if to_do == '1':
            store1.shop_menu()
        elif to_do == '2':
            store2.shop_menu()
        elif to_do == '3':
            taverm_ = tavern()
            taverm_.enter_tavern()
        elif not to_do:
            random_event_picker()
        else:
            error_found("Try again", "Invalid")
            time.sleep(1)

start()
