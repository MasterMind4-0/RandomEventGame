import tkinter as tk
import tkinter.ttk as ttk
import time
import random

def generate_healing(x: int, y: int):
    healing = random.randint(x, y)
    return healing

dictitems = {
    'weapons': {
        'ironshortsword': {
            'name': 'ironshortsword',
            'dname': 'Iron Shortsword',
            'Damage': 2,
            'price': 15
        },
        'crossbow': {
            'name': 'crossbow',
            'dname': 'Crossbow',
            'Damage': 3,
            'price': 15
        },
        'dagger': {
            'name': 'dagger',
            'dname': 'Dagger',
            'Damage': 1,
            'price': 8
        }
    },
    'items': {
        'healthpotion': {
            'name': 'healthpotion',
            'dname': 'Health Potion',
            'healing': generate_healing(1, 5),
            'price': 5
        },
        'greaterhealthpotion': {
            'name': 'greaterhealthpotion',
            'dname': 'Greater health potion',
            'healing': generate_healing(1, 10),
            'price': 15
        },
        'greatesthealthpotion': {
            'name': 'greatesthealthpotion',
            'dname': 'Greatest health potion',
            'healing': generate_healing(1, 20),
            'price': 25
        },
    },
    'drinks': {
        'special_drinks': {
            'dragonsblood': {
                'name': 'dragonsblood',
                'dname': "Dragon's Blood",
                'description': "This ale is dark and thick. It's a little bitter with a smokey after taste, an acquired taste for many. The bartender warns you that this drink will certainly leave you wasted.",
                'drunk_effective': .85,
                'exp': .02,
                'price': 6
            },
            'goblinvomit': {
                'name': 'goblinvomit',
                'dname': 'Goblin Vomit',
                'description': "This dark green that reminds many of goblin vomit. It's surprising thin, for its name, but why many avoid it is because of its horrid bitter taste.",
                'drunk_effective': .90,
                'exp': .03,
                'price': 5
            }
        },
        'rum': {
            'name': 'rum',
            'dname': 'Rum',
            'drunk_effective': .7,
            'price': 2
        },
        'wine': {
            'name': 'wine',
            'dname': 'Wine',
            'drunk_effective': .25,
            'price': 3
        },
        'beer': {
            'name': 'beer',
            'dname': 'Beer',
            'drunk_effective': .6,
            'price': 2
        }

    }
}

player_stats = {'strength': 0.0, 'constitution': 0.0}
name = None
health = 20
dev_mode_enabled = False
inventory = ["healthpotion"]
weapon = 'ironshortsword'
coin = 0


def didsomething():
    print('YOU DID SOMETHING!!')

def show_main_window():
    start.destroy()

    window = tk.Tk()
    window.title('Game')
    for i in range(0, 3):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)

    sidebar = tk.Frame(window, relief='ridge', borderwidth=5)
    sidebar.grid(row=0, column=0)

    ttk.Label(text=name.get(), master=sidebar).grid(row=0, column=0, padx=5, pady=5)
    tk.Text(window).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(text='CLICK ON MEEEE!', command=didsomething, master=sidebar).grid(row=1, column=0, padx=5, pady=5)

    window.mainloop()

start = tk.Tk()
start.title('Start')
ttk.Label(text='Are you ready for an adventure?', master=start).grid(padx=20, pady=20)
name = tk.StringVar()
ttk.Entry(master=start, textvariable=name).grid(padx=20, pady=20)
ttk.Button(text='Start', command=show_main_window, master=start).grid(padx=20, pady=20)

start.mainloop()