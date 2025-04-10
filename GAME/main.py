import time
import random
import json
from Game_Data.colors import colors

def error_found(to_do: str = 'Report the issue in GitHub!', error_name: str = None):
    if not error_name:
        print(f'{colors.YELLOW}###~~~--- ERROR ---~~~###{colors.ENDC}')
    else:
        print(f'{colors.YELLOW}###~~~--- ERROR: {error_name.upper()} ---~~~###{colors.ENDC}')
    print(f"{colors.YELLOW}###~~~--- {to_do.upper()} ---~~~###{colors.ENDC}")

def generate_healing(x: int, y: int):
    healing = random.randint(x, y)
    return healing

def calculate_chance(chance: float, modifier = None):
    random_value = random.random()
    if modifier:
        win_chance = chance - (player_stats[modifier] / 10)
    else:
        win_chance = chance
    if random_value < win_chance:
        return True
    else:
        return False

try:
    with open('GAME/Game_Data/items.json', 'r') as f:
        dictitems = json.load(f)
except FileNotFoundError or json.JSONDecodeError as e:
    error_found('There was an error loading the items database.', e)

player_stats = {'strength': 0.0, 'constitution': 0.0}
name = 'DEV'
player_health = 20
dev_mode_enabled = False
inventory = ["greatesthealthpotion", "greatesthealthpotion", "crossbow"]
player_weapon = 'ironlongsword'
player_armor = 'ironarmor'
coin = 100

def determine_armor(armor: str):
    if type(armor) is int:
        return armor
    return dictitems['armors'][armor]['Armor']

def sfix(str_to_be_fixed):
    if type(str_to_be_fixed) == str:
        str_to_be_fixed = str_to_be_fixed.lower()       
    elif type(str_to_be_fixed) == int:
        pass
    else:
        return 'ERROR'
    str_to_be_fixed = str_to_be_fixed.replace(' ', '')
    return str_to_be_fixed

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
    global player_health
    if player_health > 20:
        player_health = 20

def displayinventory():
    item_counts = {}
    for item in inventory:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    result = ""
    for item, count in item_counts.items():
        for category, items in dictitems.items():
            if item in items:
                dname = items[item]['dname']
                break
        if count > 1:
            result += f"            {dname} x{count}\n"
        else:
            result += f"            {dname}\n"
    return result.strip()

class shop:
    def __init__(self, name: str, trader_name: str = 'Trader', item_pool: list = None):
        self.name: str = name
        self.trader_name = trader_name

        if item_pool:
            self.item_pool = item_pool
        else:
            self.item_pool = self.generate_random_item_pool()

        self.item1, self.item2, self.item3 = self.select_unique_items()

    def generate_random_item_pool(self):
        allowed_items = []

        for category, items in dictitems.items():
            for item, properties in items.items():
                if properties.get("InShop") is True:
                    allowed_items.append(properties)

        if len(allowed_items) < 3:
            raise ValueError("Not enough items to populate the shop.")

        return allowed_items

    def select_unique_items(self):
        selected_items = random.sample(self.item_pool, 3)
        return selected_items[0], selected_items[1], selected_items[2]

    def shop_menu(self):
        global coin, inventory
        traded = False
        trader_prompts = ['What can I do you for?', 'What will it be today?', 'Anything catching your eye?', "Don't bargin, I am not going to give in.", "I don't do sales."]
        tr = f'\033[3m{self.trader_name}\033[0m'

        while True:
            trader_prompt = random.choice(trader_prompts)
            print(f'''
        {self.name}

        1. {self.item1['dname']} ({self.item1['price']} coins)
        2. {self.item2['dname']} ({self.item2['price']} coins)
        3. {self.item3['dname']} ({self.item3['price']} coins)

        Coin: {coin}

        Inventory: 
            {displayinventory()}

        Hit ENTER to leave.

        1, 2, 3. To buy corresponding items
        4. Sell items\n
        ''')

            t = input("")

            if t == '1':
                print(f'{tr}: {trader_prompt}')
                time.sleep(.5)
                if coin >= self.item1['price']:
                    coin -= self.item1['price']
                    inventory.append(self.item1['name'])
                    print(f'You bought a {self.item1["dname"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')
                else:
                    print('You do not have enough money to buy that item.')

            elif t == '2':
                print(f'{tr}: {trader_prompt}')
                time.sleep(.5)
                if coin >= self.item2['price']:
                    coin -= self.item2['price']
                    inventory.append(self.item2['name'])
                    print(f'You bought a {self.item2["dname"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')
                else:
                    print('You do not have enough money to buy that item.')

            elif t == '3':
                print(f'{tr}: {trader_prompt}')
                time.sleep(.5)
                if coin >= self.item3['price']:
                    coin -= self.item3['price']
                    inventory.append(self.item3['name'])
                    print(f'You bought a {self.item3["dname"]}!')
                    time.sleep(1)
                    print(f'You now have {coin} coins left.')
                else:
                    print('You do not have enough money to buy that item.')

            elif t == '4':
                invalid_items = []
                for category, items in dictitems.items():
                    for item, properties in items.items():
                        if properties.get("sellable") is False:
                            invalid_items.append(item)

                inventory_dict = {str(idx): item for idx, item in enumerate(inventory, start=1)}
                
                dinventory = []

                for idx, item in inventory_dict.items():
                    for category, items in dictitems.items():
                        if item in items:
                            dinventory.append(f"{idx}. {item} (+{dictitems[category][item]['price'] // 2} coins)")
                            break
                
                dinventory_str = "\n            ".join(dinventory)
                
                sell = input(f'''
        
        Selling

        Inventory:
            {dinventory_str}

        Enter the number of the item you'd like to sell\n
        ''')

                sell_item = inventory_dict.get(sell)
                if sell_item and sell_item not in invalid_items:
                    traded = True
                    item_found = False
                    for items in dictitems.values():
                        if sell_item in items:
                            item = items[sell_item]
                            original_price = item['price']
                            selling_price = original_price // 2

                            coin += selling_price
                            inventory.remove(sell_item)
                            print(f"You sold {item['dname']} for {selling_price} coins.")
                            item_found = True
                            break

                    if not item_found:
                        error_found("Try again", "Item not found in shop database")
                else:
                    if not sell_item:
                        error_found("Try again", "Invalid item number")
                    elif sell_item in invalid_items:
                        error_found("Sell another item", "That item cannot be sold")

            elif not t:
                if traded:
                    print('The trader waves goodbye as you leave.')
                else:
                    print('You decide not to trade and leave the shop.')
                break

            else:
                error_found("Try again", "Invalid option")

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
            self.item1 = self.item2 = {'dname': 'Out of Stock', 'price': 0}

        if len(self.special) > 0:
            self.house_special = random.choice(self.special)
        else:
            self.house_special = {'dname': 'Out of Stock', 'price': 0, 'description': 'None available.'}

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
        time.sleep(1)
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
            return

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
            return
            
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

    def back_alley(self):
        global coin, inventory
        thug = '\033[3mThug\033[0m'
        thug_leader = '\033[3mThug Leader\033[0m'
        wait()
        print('You awaken in a dark alley way.')
        time.sleep(2)
        print('Your head screams and your mouth thirsts.')
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
            thug_fight = battle('Thugs', 20, 3, 'strength', attackers_armor="leatherarmor")
            print(f'\033[3m{name}\033[0m: As, I said, back the HELL AWAY!')
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
                    inventory.remove(sfix(stuff_given))
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

    def rat_mini_game(self):
        global coin
        bt = '\033[3mBartender\033[0m'
        coin_gain_cache = 0
        rat_kill_count = 0
        room = "stairs"
        
        print('You look around the cellar, where to go now..')
        time.sleep(1)
        while coin_gain_cache < 30:
            option_1 = '1. Main Cellar'
            option_2 = '2. Storage Room'
            option_3 = '3. Back Room'
            
            if room == 'main cellar':
                option_1 = '1. Main Cellar (You are here)'
            elif room == 'storage room':
                option_2 = '2. Storage Room (You are here)'
            elif room == 'back room':
                option_3 = '3. Back Room (You are here)'

            
            
            go_to = input(f'''
                
                Rat kill count: {rat_kill_count}
                
                Actions:
                
                Hit ENTER to go to a random room
                
                {option_1}
                {option_2}
                {option_3}
                4. Back to the bartender
                ''')
            
            if go_to == '1' and option_1 == '1. Main Cellar':
                room = 'main cellar'
            elif go_to == '2' and option_2 == '2. Storage Room':
                room = 'storage room'
            elif go_to == '3' and option_3 == '3. Back Room':
                room = 'back room'
            elif go_to == '4':
                print('You walk back to the bartender.')
                time.sleep(1)
                print(f'{bt}: You killed {coin_gain_cache} those darn rats! Here, you bloody earned it!')
                time.sleep(1)
                coin += coin_gain_cache
                print(f'You gained {coin_gain_cache} coins!')
            else:
                print('Invalid option, try again.')
            
            print(f'You walk around the {room}, looking for rats.')
            time.sleep(2)
            if calculate_chance(.5):
                print('You hear a loud screeching sound.')
                time.sleep(1)
                battle('Rats', 2, 1, 'strength', attackers_armor='naturalarmor').fight()
                coin_gain_cache += 1
                rat_kill_count += 1
            else:
                print('You look around, but there are no rats in sight.')
                time.sleep(2)

        print('You wiped to sweat from your brow. They were all dead.')
        time.sleep(1)
        print(f'{bt}: You killed {coin_gain_cache} those darn rats! Here, you bloody earned it!')
        time.sleep(1)
        coin += coin_gain_cache
        print(f'You gained {coin_gain_cache} coins!')
            
    def bartender(self):
        global coin
        btgreetings = ['How are you doing today?', 'What can I get you?',"We don't have virgin here for the record.","I feel sorry for people who don't drink. When they wake up in the morning, that's as good as they're going to feel all day."]
        btbuydrink = ['That there is a good drink.', 'You vomit outside, not on me, got it?','Your order.']
        btleave = ['Pleasure doing business.', 'Hope to see you again.','Until you order again.']
        choice_of_greeting = random.choice(btgreetings)
        bt = '\033[3mBartender\033[0m'
        rats = calculate_chance(.25)
        if rats:
            rat_problem = "\nType RAT to help the bartender with a rat problem.\n"
        else:
            rat_problem = ''
        

        print(f'{bt}: {choice_of_greeting}')
        wait()
        while True:
            choice_of_leave = random.choice(btleave)
            choice_of_buydrink = random.choice(btbuydrink)

            menu_entry = input(f'''
        {self.name}'s menu
        {rat_problem}
        Hit ENTER to leave

        1. {self.item1['dname']} ({self.item1['price']} coins)
        2. {self.item2['dname']} ({self.item2['price']} coins)

        For HOUSE SPECIAL, type HS: {self.house_special['dname']} ({self.house_special['price']} coins)

        {self.house_special['description']}\n
        ''')

            if menu_entry == '1':
                if coin < self.item1['price']:
                    print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
                else:
                    drunk_chance = self.item1['drunk_effective'] - (player_stats['constitution'] / 10)
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
                        print(f"{bt}: How the hell do you pass out from bloody wine?")
                        self.back_alley()
                    elif self.item1 == 'wine':
                        print('You sip your wine gently, soaking in the flavor and aroma.')
                        time.sleep(1)
                    elif wasted:
                        print('After downing your mug, you can barely stand.')
                        time.sleep(1)
                        print('You drunkly walk outside, before you pass out.')
                        self.back_alley()
                    else:
                        print('You lift you chin and gulp the liquor to the last drop.')
                        time.sleep(1)


            elif menu_entry == '2':
                if coin < self.item2['price']:
                    print(f"{bt}: Hey there, this ain't a charity, you got to have enough money for this liquor here.")
                else:
                    drunk_chance = self.item2['drunk_effective'] - (player_stats['constitution'] / 10)
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
                        self.back_alley()
                    elif self.item2 == 'wine':
                        print('You sip your wine gently, soaking in the flavor and aroma.')
                        time.sleep(1)
                    elif wasted:
                        print('After downing your mug, you can barely stand.')
                        time.sleep(1)
                        print('You drunkly walk outside, before you pass out.')
                        self.back_alley()
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
                            self.back_alley()
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
            
            
            elif menu_entry.lower() == 'rat':
                if rats:
                    rats = False
                    print(f'{bt}: You want to help me with the rat problem?')
                    time.sleep(1)
                    print(f'{bt}: I have a few rats in the cellar, and I need someone to take care of them.')
                    time.sleep(1)
                    self.rat_mini_game()

            elif not menu_entry:
                print(f'\033[3m{name}\033[0m: Thank you, but I think I am OK.')
                time.sleep(1)
                print(f'{bt}: {choice_of_leave}')
                self.return_tavern()
            
            else:
                pass

class battle:
    def __init__(self, attackers_name: str, attackers_health: int, attackers_damage: int, type_exp: str, reward_gold: int = None, reward_item: str = None, attackers_armor = 0):
        self.attackers_name: str = attackers_name
        self.attackers_health: int = attackers_health
        self.attackers_damage: int = attackers_damage
        self.attackers_armor: int = attackers_armor
        self.exp: float = self.attackers_health * .02
        self.type_exp: str = type_exp
        if not reward_item:
            self.reward_item = False
        else:
            self.reward_item: str = reward_item
        if not reward_gold:
            self.reward_gold = attackers_health * .4
            if self.reward_gold < 1:
                self.reward_gold = 0
            self.reward_gold = round(self.reward_gold)
        elif reward_gold == 'ng':
            self.reward_gold = 0
        else:
            self.reward_gold: int = reward_gold

    def fight(self):
        global player_health, inventory, player_weapon, coin, player_stats

        if dev_mode_enabled:
            sim_question = input('Would you prefer to simulate a battle instead? (Y/N)\n')
            if sim_question.lower() == 'y':
                self.simulate_fight()
                return

        while player_health > 0:
            if self.attackers_health <= 0:
                self.handle_victory()
                break

            time.sleep(1)
            action = self.get_player_action()

            if action == '1':
                self.use_health_potion()
            elif action == '2':
                self.switch_weapon()
            elif not action:
                self.perform_attack()
            else:
                print("Invalid action. Please try again.")
        if player_health <= 0:
            death()

    def handle_victory(self):
        global player_stats, inventory, coin
        player_stats[self.type_exp] += self.exp
        print("You won the fight!")
        if self.reward_item:
            inventory.append(self.reward_item)
            print(f'You are awarded with a {self.reward_item}!')
        if self.reward_gold:
            coin += self.reward_gold
            print(f"You are awarded with {colors.YELLOW}{self.reward_gold}{colors.ENDC} coins!")

    def get_player_action(self):
        return input(f"""
        {colors.RED}Your health: {player_health}{colors.ENDC}

        {colors.BLUE}Equiped Weapon: {dictitems["weapons"][player_weapon]['dname']}
        Equiped Armor: {dictitems['armors'][player_armor]['dname']}{colors.ENDC}

        Actions:

        Hit ENTER to continue the battle

        1. Take health potion (You have {colors.GREEN}{inventory.count('healthpotion') + inventory.count('greaterhealthpotion') + inventory.count('greatesthealthpotion')}{colors.ENDC})
        2. Switch equipped weapon\n
""")

    def use_health_potion(self):
        if 'healthpotion' in inventory or 'greaterhealthpotion' in inventory or 'greatesthealthpotion' in inventory:
            which_health = input(f'\nHit ENTER to leave\n\n1. Health potion ({inventory.count('healthpotion')})\n2. Greater health potion ({inventory.count('greaterhealthpotion')})\n3. Greatest health potion ({inventory.count('greatesthealthpotion')})\n')
            if which_health == '1' and 'healthpotion' in inventory:
                self.consume_potion('healthpotion')
            elif which_health == '2' and 'greaterhealthpotion' in inventory:
                self.consume_potion('greaterhealthpotion')
            elif which_health == '3' and 'greatesthealthpotion' in inventory:
                self.consume_potion('greatesthealthpotion')
            else:
                print("You don't have that potion!")
        else:
            print("You don't have any health potions!")
        time.sleep(1)

    def consume_potion(self, potion_type):
        global player_health, inventory
        player_health += generate_healing(dictitems['items'][potion_type]['min'], dictitems['items'][potion_type]['max'])
        inventory.remove(potion_type)
        healthcap()
        print(f'Consuming one {dictitems['items'][potion_type]['dname']}...')

    def switch_weapon(self):
        global player_weapon, inventory
        switched_weapon = input('What weapon would you like to switch to?\n')
        if switched_weapon in inventory and switched_weapon in dictitems['weapons']:
            inventory.append(dictitems['weapons'][player_weapon]['name'])
            player_weapon = dictitems['weapons'][switched_weapon]['name']
        else:
            print("You don't have that weapon.")

    def perform_attack(self):
        global player_health
        print(f"The {self.attackers_name} charges towards you,")
        time.sleep(.5)
        if self.calculate_hit_chance(determine_armor(self.attackers_armor)):
            self.attackers_health -= dictitems['weapons'][player_weapon]['Damage']
            print(f"The {self.attackers_name} missed! Giving you the opportunity to attack!")
            time.sleep(.5)
            if dev_mode_enabled:
                print(f"The {self.attackers_name} has {self.attackers_health} left!")
        else:
            if player_armor:
                player_health_damage_tracker = player_health
                player_health_damage_tracker -= self.attackers_damage - (0.2 * determine_armor(player_armor))
                player_health_damage_tracker = round(player_health_damage_tracker)
                if player_health_damage_tracker == player_health:
                    print(f"The {self.attackers_name} tried to hit you, but your armor absorbed the damage!")
                    time.sleep(1)
                else:
                    print(f"The {self.attackers_name} hit you!")
                    time.sleep(.5)
                    print(f"You have {player_health} health left!")

    def calculate_hit_chance(self, armor):
        random_value = random.random()
        base_hit_chance = .5
        hit_chance = base_hit_chance - (armor * .02)
        if dev_mode_enabled:
            print(f"Hit chance: {hit_chance}\nArmor: {self.attackers_armor}\nBase hit chance: {base_hit_chance}\nHit chance {hit_chance} < compared value {random_value} {hit_chance < random_value}")
        return random_value < hit_chance

    def simulate_fight(self):
        global player_health, inventory, player_weapon, coin, player_stats
        health_point = input('What should health be before you take a health potion?\n')
        reward_yes = input('Receive rewards? (Y/N)\n')
        if health_point:
            pass
        else:
            health_point = 6
        reward_yes = sfix(reward_yes) == 'y'

        while player_health > 0:

            if self.attackers_health <= 0:
                player_stats[self.type_exp] += self.exp
                print("You won the fight!")
                if self.reward_item and reward_yes:
                    inventory.append(self.reward_item)
                    print(f'You are awarded with a {self.reward_item}!')
                if self.reward_gold and reward_yes:
                    coin += self.reward_gold
                    print(f"You are awarded with {self.reward_gold} coins!")
                break

            if player_health <= round(int(health_point)):
                if 'healthpotion' in inventory or 'greaterhealthpotion' in inventory or 'greatesthealthpotion' in inventory:
                    which_health = input(f'health: {player_health}\n\nHit ENTER to leave\n\n1. Health potion ({inventory.count('healthpotion')})\n2. Greater health potion ({inventory.count('greaterhealthpotion')})\n3. Greatest health potion ({inventory.count('greatesthealthpotion')})\n')
                    if which_health == '1':
                        if 'healthpotion' in inventory:
                            player_health += generate_healing(dictitems['items']['healthpotion']['min'], dictitems['items']['healthpotion']['max'])
                            inventory.remove('healthpotion')
                            healthcap()
                        else:
                            print("You don't have health potions!")
                    elif which_health == '2':
                        if 'greaterhealthpotion' in inventory:
                            player_health += generate_healing(dictitems['items']['greaterhealthpotion']['min'], dictitems['items']['greaterhealthpotion']['max'])
                            inventory.remove('greaterhealthpotion')
                            healthcap()
                        else:
                            print("You don't have greater health potions!")
                    elif which_health == '3':
                        if 'greatesthealthpotion' in inventory:
                            player_health += generate_healing(dictitems['items']['greatesthealthpotion']['min'], dictitems['items']['greatesthealthpotion']['max'])
                            inventory.remove('greatesthealthpotion')
                            healthcap()
                        else:
                            print("You don't have greatest health potions!")

            if self.calculate_hit_chance(determine_armor(self.attackers_armor)):
                self.attackers_health -= dictitems['weapons'][player_weapon]['Damage']
            else:
                player_health -= self.attackers_damage
        else:
            pass
        if player_health <= 0:
            death()

def random_event_picker():
    global inventory, player_weapon, player_health
    wait()
    while True:
        healthcap()
        X = input(f'''


        Health: {colors.RED}{player_health}{colors.ENDC}

        Equiped weapon: {dictitems["weapons"][player_weapon]['dname']}
        Equiped armor: {dictitems['armors'][player_armor]['dname']}

        Inventory:
            {displayinventory()}
        
        Coin amount: {colors.YELLOW}{coin}{colors.ENDC}

        Actions:

        Hit ENTER to continue walking

        1. Take health potion
        2. Switch equiped weapon\n
''')
        if X == '1':
            if 'healthpotion' in inventory or 'greaterhealthpotion' in inventory or 'greatesthealthpotion' in inventory:
                which_health = input(f'\nHit ENTER to leave\n\n1. Health potion ({inventory.count('healthpotion')})\n2. Greater health potion ({inventory.count('greaterhealthpotion')})\n3. Greatest health potion ({inventory.count('greatesthealthpotion')})\n')
                if which_health == '1':
                    if 'healthpotion' in inventory:
                        player_health += generate_healing(dictitems['items']['healthpotion']['min'], dictitems['items']['healthpotion']['max'])
                        inventory.remove('healthpotion')
                        healthcap()
                        print('Consuming one health potion...')
                    else:
                        print("You don't have health potions!")
                elif which_health == '2':
                    if 'greaterhealthpotion' in inventory:
                        player_health += generate_healing(dictitems['items']['greaterhealthpotion']['min'], dictitems['items']['greaterhealthpotion']['max'])
                        inventory.remove('greaterhealthpotion')
                        healthcap()
                        print('Consuming one greater health potion...')
                    else:
                        print("You don't have greater health potions!")
                elif which_health == '3':
                    if 'greatesthealthpotion' in inventory:
                        player_health += generate_healing(dictitems['items']['greatesthealthpotion']['min'], dictitems['items']['greatesthealthpotion']['max'])
                        inventory.remove('greatesthealthpotion')
                        healthcap()
                        print("Consuming one greatest health potion...")
                    else:
                        print("You don't have greatest health potions!")
            else:
                print("You don't have any health potions!")
            time.sleep(1)
        elif X == '2':
            print("Inventory:")
            weapon_inventory = [item for item in inventory if item in dictitems['weapons']]
            for idx, item in enumerate(weapon_inventory, start=1):
                print(f"    {idx}. {dictitems['weapons'][item]['dname']}")

            try:
                switched_weapon_idx = int(input('Enter the number of the weapon you would like to switch to:\n'))
                if 1 <= switched_weapon_idx <= len(weapon_inventory):
                    switched_weapon = weapon_inventory[switched_weapon_idx - 1]
                    inventory.append(dictitems['weapons'][player_weapon]['name'])
                    player_weapon = dictitems['weapons'][switched_weapon]['name']
                    inventory.remove(switched_weapon)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif not X:
            events = [town, farmer_problem, lost_traveler, travling_merchant, tavern_event, kidnappers, tavern_challenge, skeleton_attack, tavern_rats]
            random.choice(events)()
        else:
            pass
            
def start():
    global player_stats, name, player_health, dev_mode_enabled, inventory, player_weapon, player_armor, coin
    name = input("What will your character's name be?\n")
    if sfix(name) == 'dev':
        dev_mode_enabled = True
    else:
        name = name
        inventory = ["healthpotion"]
        player_weapon = 'ironshortsword'
        player_armor = 'noarmor'
        coin = 0
    print(f"That's not a bad name, {name}!")
    time.sleep(.5)
    print('Well, that is all, let us begin!')
    random_event_picker()

def tavern_event():
    tavern().enter_tavern()

def travling_merchant():
    print('A merchant, with his backpack filled to the brim with items, comes toward you.')
    time.sleep(1)
    t = input(f'{colors.ITALIC}Merchant{colors.ENDC}: Well, hello there! Care to look in my shop? (Y/N)\n')
    if t.lower() == 'y':
        merchant_shop = shop("Merchant's Shop", 'Merchant')
        print('The merchant smiles,')
        time.sleep(.5)
        print('"Wonderful! See what you like."')
        time.sleep(1)
        merchant_shop.shop_menu()
    else:
        print('The merchant wonders away in solom.')

def kidnappers():
    kidnappers_fight = battle('Thugs', 10, 2, 'strength', attackers_armor="leatherarmor")
    print('As you walk along the weaving path in the forest,')
    time.sleep(1)
    print('A group of thugs jumps from the bushes.')
    time.sleep(1)
    print("\033[3mThugs\033[0m: Get em boys!")
    kidnappers_fight.fight()

def town():
    print('\033[3m"As you walk through a village, you ponder on what you should do..."\033[0m')
    time.sleep(2)
    
    store1 = shop("Shop's Stock", 'Shopkeeper')
    store2 = shop("Shop's Stock", 'Shopkeeper')
    time.sleep(1)
    while True:
        to_do = input(f'''
        Welcome to town!

        Inventory:
            {displayinventory()}

        Hit ENTER to continue your journey.

        1. Go to first shop?
        2. Go to the second shop?
        3. Go to local tavern?\n
        ''')
        if to_do == '1':
            store1.shop_menu()
        elif to_do == '2':
            store2.shop_menu()
        elif to_do == '3':
            tavern().enter_tavern()
        elif not to_do:
            random_event_picker()
        else:
            error_found("Try again", "Invalid")
            time.sleep(1)

def farmer_problem():
    global coin, player_stats, dev_mode_enabled
    fr = '\033[3mFarmer\033[0m'

    print('During your journey, you come across a farmer in a small town you are passing through.')
    time.sleep(1)
    print('He begs for your help,')
    time.sleep(1)
    print(f"{fr}: Please! Every night something eats my crops! I beg, everyone has regected, but can you help me?")
    time.sleep(1)
    helpquest = input('Should you help the man? (Y/N)\n')
    if sfix(helpquest) == 'y':
        print(f"{name}: Well, I don't see why not.")
        time.sleep(1)
        print('The man graciously thanks you.')
        time.sleep(1)
        print(f"{fr}: Every night my berries always seem to be gone! Do you think you can stay overnight and discover what beast eats my berries?")
        time.sleep(2)
        print('You accept and, at night, after waiting for hours, you finally spot the thief.')
        time.sleep(1)
        print('A bear. And a large one at that.')
        time.sleep(1)
        scared_chance = .2
        random_value = random.random()
        if random_value < scared_chance:
            if dev_mode_enabled:
                print(f"scared chance: {scared_chance}\ncompared value: {random_value}")
            print('As you see the bear, you feel a sense of fear.')
            time.sleep(1)
            print('The bear stands on its hind legs, you fall backwards in fear.')
            time.sleep(1)
            print('You dash before the bear does anything else.')
            random_event_picker()
        choice_bear = input('Should you fight the bear, try to tame the bear, or should you leave it be? (1, 2, or 3)\n')
        if sfix(choice_bear) == '1':
            print('You charge the bear, frightening it.')
            time.sleep(1)
            battle('Bear', 25, 3, 'strength', 'ng', attackers_armor=2).fight()
        elif sfix(choice_bear) == '2':
            print(f'{name}: Woah! Easy there.')
            time.sleep(1)
            print('The bear seems to stare at you,')
            time.sleep(1)
            print('You reach out your hand.')
            time.sleep(1)
            tame_chance = .25
            random_value = random.random()
            if dev_mode_enabled:
                    print(f"tame chance: {tame_chance}\ncompared value: {random_value}")
            if random_value > tame_chance:
                print('As you reach out, however, the bear turns aggresive and lashes out at you.')
                time.sleep(2)
                battle('Bear', 25, 3, 'strength', 'ng', attackers_armor=2).fight()
                coin += 5
                print("In the morning, the man is overjoyed to hear you've gotten rid of the pest problem.")
                time.sleep(2)
                print('He gives you his gold and thanks you for your work.')
                random_event_picker()
            else:
                coin += 7
                print('The bar cautiously walks towards you.')
                time.sleep(1)
                print('It nozzles its nose against your hand.')
                time.sleep(1)
                print('In the morning, you show the farmer how to take care of the bear.')
                time.sleep(2)
                print('You even train it to pick the berries for the farmer.')
                time.sleep(2)
                print('As the farmer gives you your award, you leave to continue your travels.')
                random_event_picker()
        else:
            print('You look at the large bear, and decide on leaving it be.')
            time.sleep(1)
            print('You slip away under the cover of the night.')
            random_event_picker()

    else:
        print(f'{name}: Sorry, but I have too much to do, deal with it yourself.')
        random_event_picker()

def lost_traveler():
    global coin
    print('While traveling along a beaten path in forest,\nyou come across a fellow who is flipping his map over and over, as if he was lost.')
    time.sleep(2)
    ask = input("Ask if he is lost? (Y/N)\n")

    if sfix(ask) == 'y':
        st = '\033[3mStranger\033[0m'
        attack_chance = .05
        questions_beginning = ['Hey, you lost?', 'Are you lost?', "Lost, stranger?", 'Need help?']
        question_beginning = random.choice(questions_beginning)

        print(f'{name}: {question_beginning}')
        time.sleep(1)
        print('The man looks to you.')
        time.sleep(1)
        print(f'{st}: Oh! Yes! Do you know the way to the nearest town?' )
        time.sleep(1)
        nearest_town = input(f'{st}: Well, do you? (Y/N)\n')

        if sfix(nearest_town) == 'y':
            print('You point up the hill.')
            time.sleep(1)
            print(f'{name}: Just up there, look beyond the horizon.')
            time.sleep(1)
            print(f"{name}: Why you heading there?")
            attack_chance += .05
            print(f'{name}: Can I ask why?')
            time.sleep(1)
            print(f'{st}: Oh, I just wanted to find a guide.')
            time.sleep(1)
            if coin <= 10:
                help = input('\033[3m"I could really use the coin... (Help or not)\n"\033[0m')
                time.sleep(1)
            elif coin <= 25:
                help = input('\033[3m"I could do with more coin... (Help or not)\n"\033[0m')
                time.sleep(1)
            else:
                help = input('\033[3m"Well, maybe I could help him... (Help or not)\n"\033[0m')
                time.sleep(1)

            if sfix(help) == 'help':
                attack_chance += .1
                print(f'{name}: You know, I am quite the traveler myself.')
                time.sleep(1)
                print(f'{st}: Well; are you good with-')
                print('He pauses to lean in,')
                time.sleep(2)
                print(f'{st}: Secrets?')
                time.sleep(1)
                fight = input('"Sure" or "No"?\n')

                if sfix(fight) == 'sure':
                    print(f'{name}: Sure, I can keep a secret.')
                    time.sleep(1)
                    print(f'{st}: Well, I am looking for a guide to walk me to the \033[3mNeverwinter Wood\033[0m?.')
                    time.sleep(1)
                    print(f'{name}: Well, I know the way well.')
                    time.sleep(1)
                    print(f'{st}: Oh, thank you so much!')
                    time.sleep(1)
                    print(f'{name}: No problem, just follow me.')
                    journey_to_Neverwinter_Wood()
                else:
                    random_value = random.random()
                    print(f"{name}: I don't know, I'm sure you'll find a better guide in that town.")
                    time.sleep(1)

                    if random_value < attack_chance:
                        print('The stranger looks at you coldly.')
                        time.sleep(1)
                        print(f'{st}: I do apologize, but, I must do this.')
                        battle('Strange Traveler', 20, 5, 'strength', 25, 'ironlongsword', 'ironarmor').fight()
                    print(f'{st}: Well, thanks anyway!')
                    random_event_picker()
            
            else:
                print(f"{name}: Best of luck on your journeys, then.")
                time.sleep(1)
                print('The man smiles as he leaves.')
                random_event_picker()

        else:
            print('\033[3m"Whatever..."\033[0m')
            time.sleep(.5)
            print('You pass by, ignoring the stranger.')
            random_event_picker()

def journey_to_Neverwinter_Wood():
    st = '\033[3mStranger\033[0m'

    print('You and the stranger walk along the path to the Neverwinter Wood.')
    time.sleep(2)
    print('The stranger and you are quiet.')
    time.sleep(1)
    print('And as you walk, you hear the sound of a twig snapping.')
    time.sleep(2)
    print('You turn around to see a hobgoblin in the distance.')
    time.sleep(2)
    print(f'{st}: What in the blazes is a hobgoblin doing in this terrain?')
    time.sleep(1)
    print("As the stranger speaks, the hobgoblin's ears perk.")
    time.sleep(2)
    print('It turns its head to you and the stranger.')
    battle('Hobgoblin', 15, 3, 'strength', 10, attackers_armor='naturalarmor').fight()
    print(f'{st}: This is percisely why I needed a guide.')
    time.sleep(2)
    print(f'{name}: Yeah, I can see that.')
    time.sleep(1)
    print('You continue mostly uninterrupted to the Neverwinter Wood.')
    time.sleep(2)
    print('And once you arrive,')
    time.sleep(1)
    choice = input(f'{st}: Do you think you could take me a little more into the woods? (Y/N)')
    if sfix(choice) == 'y':
        print(f'{name}: Sure, I can take you a little further.')
        time.sleep(1)
        print(f'{st}: Thank you so much!')
        time.sleep(1)
        print('You and the stranger walk further into the woods.')
        time.sleep(2)
        print('The stranger looks around,')
        time.sleep(1)
        print(f'{st}: NOW!!')
        time.sleep(2)
        print('You, surprised, start seeing hooded figures jump from the trees.')
        time.sleep(2)
        print("You see a sly smile on the stranger's face.")
        time.sleep(2)
        print('And as they grow nearer, you see the hooded figures pale faces and sharp teeth.')
        time.sleep(2)
        print('\033[3mVampires...\033[0m')
        battle('Vampires', 30, 5, 'strength', 35, attackers_armor='hood').fight()
        print(f'You finish off the vampires, they all lay dead.')
        time.sleep(1)
        print("You spit on the stranger's body as you walk out of the woods; continuing your journey.")
        time.sleep(3)
        random_event_picker()
    else:
        print(f'{name}: I think this is good enough.')
        time.sleep(1)
        print('The stranger curses as he walks off into the woods.')
        time.sleep(1)
        print("Oddly, you feel as if you've just avoided something awful.")
        time.sleep(3)
        random_event_picker()

def tavern_challenge():
    global player_health, coin
    bt = '\033[3mBartender\033[0m'

    print('Completely beat, you walk into a tavern.')
    time.sleep(1)
    print('As you walk in and sit down by the bartender.')
    time.sleep(.5)
    print('You notice a crowd around a table across the tavern; getting drunk as if their was no tommorrow.')
    time.sleep(1)
    print(f"{bt}: I see you're interested.")
    time.sleep(1)
    choice = input(f'"Not really," or "What is going on?" (1 or 2)\n')
    if sfix(choice) == '2':
        print(f"{bt}: Well, those fools are drinking their heart out to win in a competition.")
        time.sleep(1)
        print(f"{bt}: Ya interested?\n")
        time.sleep(1)
        choice = input('(Y/N)\n')
        if sfix(choice) == 'y':
            print(f"{name}: Why not? What's to lose?")
            time.sleep(1)
            print(f'{bt}: Actually, you do lose something; admission is 5 coins.')
            time.sleep(1)
            print(f'{bt}: But hey, you could win the pot.')
            time.sleep(.5)
            choice = input(f'{colors.ITALIC}Should I..? (Y/N){colors.ENDC}')
            if sfix(choice) == 'y':
                if coin < 5:
                    print(f'{bt}: Sorry, you do not have enough coins.')
                    time.sleep(1)
                    print(f'{bt}: You might have enough for a drink if you want though.')
                    tavern().bartender()
                    random_event_picker()
                else:
                    amount_people = random.randint(3, 15)
                    random_value = random.random()
                    win_chance = .45 - (player_stats['constitution'] / 10)
                    coin -= 5

                    print('You give the bartender the 5 coins.')
                    time.sleep(2)
                    print('You make you way down to the table.')
                    time.sleep(2)
                    print(f'There seems to be {amount_people} people at the table.')
                    time.sleep(2)
                    print('You sit and prepare yourself as the large beer is placed in front of you.')
                    time.sleep(3)
                    print(f'{bt}: Alright, the rules are simple, drink the beer as fast as you can.')
                    time.sleep(4)
                    print(f'{bt}: The first to finish, wins.')
                    time.sleep(2)
                    print(f"{bt}: Now, let's begin!")
                    time.sleep(2)
                    if random_value < win_chance:
                        coin += 5 * amount_people
                        print('As you drink your large mug of ale,')
                        time.sleep(.5)
                        print("You don't even pay attention to the others, you're set on your goal of winning.")
                        time.sleep(1)
                        print('And just before you black out, you take the last swig and slam the mug on the table.')
                        time.sleep(1)
                        print('You barely manage to hear the bartender saying you won.')
                        time.sleep(1)
                        print('You completely pass out, everything far beyond a haze.')
                        time.sleep(1)
                        print('You walk up on the streets in front of the tavern with a nasty headache. You shrug it off and get up to continue your journey.')
                        random_event_picker()
                    else:
                        print('As you down the mug, it sloshes down your chin.')
                        time.sleep(1)
                        print('And right there your fall, completely knocked out.')
                        time.sleep(1)
                        print(f'{name}: Ugh...')
                        tavern().back_alley()
        else:
            print(f'{name}: Nah, just let me see what you sell.')
            tavern().bartender()
            random_event_picker()
    else:
        print(f'{name}: Nah, just let me see what you sell.')
        tavern().bartender()
        random_event_picker()

def skeleton_attack():
    global player_health, coin
    print('You come across a dead body, its skeleton showing through the rotton flesh.')
    time.sleep(1)
    choice = input('Should you loot the body, walk away, or bury the body? (1, 2, or 3)\n')
    if sfix(choice) == '1':
        if calculate_chance(.7):
            coin += random.randint(3, 12)
            print('The body animates as you come near,')
            time.sleep(1)
            print('It screeches and lunges at you.')
            time.sleep(1)
            battle('Skeleton', 10, 2, 'strength', attackers_armor='naturalarmor', reward_item="bonedagger").fight()
            print('You wipe the sweat off your brow.')
            time.sleep(1)
            print('You also loot the body and find a couple coins.')
            random_event_picker()
        else:
            coin += random.randint(6, 16)
            print('You loot the body of its past lifes belongings.')
            random_event_picker()
    elif sfix(choice) == '2':
        print('You decided to leave, best to leave the dead to the body collectors.')
        random_event_picker()
    elif sfix(choice) == '3':
        if calculate_chance(.5):
            print('The body animates as you come near,')
            time.sleep(1)
            print('It screeches and lunges at you.')
            time.sleep(1)
            battle('Skeleton', 10, 2, 'strength', attackers_armor='naturalarmor', reward_item="bonedagger").fight()
            print('Once you kill the undead. You bury the body.')
            time.sleep(2)
            print('You wipe the sweat off your brow as you leave.')
            random_event_picker()
        else:
            print('You bury the body, say your prayers, and leave.')
            random_event_picker()

def tavern_rats():
    global coin
    bt = '\033[3mBartender\033[0m'
    
    print('As you were waiting for the bartender at a lonely bar a stormy night,')
    time.sleep(1)
    print('The bartender walks up to you-- with a solemn look on his face.')
    time.sleep(1)
    print(f'{bt}: I know you came here for a drink, but you look like you can handle a problem of mine.')
    time.sleep(1)
    print(f'{bt}: As you can see, this tavern does not have the most amount of clients.')
    time.sleep(1)
    print(f'{bt}: The problem is, I have a rat problem in the cellar, and I need someone to take care of it.')
    time.sleep(2)
    accept = input(f'{bt}: I can pay you a a coin for each damned rat you kill. (Y/N)\n')
    if sfix(accept) == 'y':
        print(f'{name}: Why not.')
        time.sleep(1)
        print(f'{bt}: Right down this way, please.')
        time.sleep(1)
        print('You walk down the stairs to the cellar.')
        time.sleep(2)
        print('And as you walk down the stairs, you hear a loud screeching sound.')
        time.sleep(2)
        battle('Rats', 2, 1, 'strength', attackers_armor='naturalarmor').fight()
        print('You finish off the rat, and look around the cellar.')
        time.sleep(1)
        print(f"{name}: A coin a rat...")
        time.sleep(1)
        tavern().rat_mini_game()
        random_event_picker()
    else:
        print(f'{name}: Sorry, but I am here just for a drink.')
        time.sleep(1)
        print('The bartender signs.')
        time.sleep(1)
        print(f'{bt}: Well, I guess I can understand that.')
        time.sleep(2)
        tavern().bartender()
        random_event_picker()

start()