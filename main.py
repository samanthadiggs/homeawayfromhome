import random
from time import sleep
print("Welcome to Home Away From Home! A Text-Based RPG game teaching students about agricultural practices from around the world!")
print("There are four worlds you can choose from, each with its own gameplay \nNunjin modeled after South Korea's Jeju Island \nLandry \nSotori modeled after Japan \nNyongo\n Please note the only worlds that are completed are Nunjin and Sotori. The other's will be completed at a later time")

game_worlds = ["Nunjin", "Landry", "Sotori", "Nyongo"]
current_game_world = ""
def choose_world(user_world):
    global game_worlds
    global current_game_world
    for world in game_worlds:
        if user_world == world:
            current_game_world = user_world
    return current_game_world

user_world = input("Please select your world (Nunjin, Landry, Sotori, Nyongo). Please put capital letters: ").capitalize()
choose_world(user_world)
print(f"Nice! Let's get started in {current_game_world}")
user_name = input("Please type in your name: ").capitalize()

inventory = {
    "Garlic Seeds" : 1 # the key is the item and the value is the quantity!
}

my_market = {}

seed_to_plant = {
    "Garlic Seeds" : "Garlic",
    "Onion Seeds": "Onion",
    "Stawberry Seeds": "Strawberry",
    "Pear Seeds": "Pears",
    "Carrot Seeds": "Carrots",
    "Tangerine Seeds": "Tangerines",
    "Rice Seeds" : "1 LB of Rice",
    "Persimmon Seeds" : "Persimmons",
    #maps the seeds to the plant
}
coins = 50
XP = 0
days = 0
level = 0
game_run = True

nunjin_sea = {
    "turban shells": 20, # Each Key is the sea creature and the value is how much it is worth!
    "sea cucumbers": 40, 
    "mackerel": 10, 
    "abalone": 5, 
    "hairtail fish": 20, 
    "Sea Urchin": 13, 
    "Cuttlefish":17, 
    "Octopus": 11, 
    "Cutlassfish": 35, 
    "Shrimp": 1
    }

nunjin_market = {
    "fishing rod":10, #Each Key is the item and the Value is the price!
    "Golden fishing rod - increases your chances of catching fish": 25,
    "Carrot Seeds": 3,
    "Tangerine Seeds": 5,
    "Rice Seeds" : 3,
    "Pear Seeds" : 2,
    "Persimmon Seeds" : 7,
    "Strawberry Seeds": 12,
    "Garlic Seeds": 15,
    "Onion Seeds": 10,
    "Super Growth Ginseng - helps speed up the growing process": 45,
    "Special Fish Bait": 75,
}

sotori_market = {
    "fishing rod": 9,
    "Sugar Beet Seeds":10,
    "Daikon Seeds": 7,
    "Cabbage Seeds": 6,
    "Taro Seeds": 5,
    "Carrot Seeds": 10,
    "Cherry Seeds": 13,
    "Pumpkin Seeds": 17,
    "Onion Seeds": 8,
}
def fishing():
    global coins, XP, days, level, nunjin_sea, inventory
    print(f"Coins {coins}                 | XP {XP}                 | Day {days}                 | Level {level}                 | ")
    print()
    print("Let's get fishing!")
    print("Searching for fishing rod...")
    sleep(0.75)
    if len(inventory) == 0:
        print("Uh oh, your inventory is empty!")
    elif len(inventory) > 0:
        for item in inventory:
            if "fishing rod" not in inventory:
                print("Uh oh! Looks like you need to go buy a fishing rod!")
            elif "fishing rod" in inventory:
                if random.randint(0, 101) < 25:
                    caught_fish = random.choice(nunjin_sea)
                    print("Waiting....")
                    sleep(1)
                    print("Still waiting....")
                    print(0.75)
                    print(f"Hooray, you caught {caught_fish}! {caught_fish} is worth {nunjin_sea[caught_fish]}")
                elif random.randint(0,101) > 25:
                    print("Sorry bad catch day. Better luck next time!")

def farming():
    global days, level, inventory, seed_to_plant, my_market
    print("Let's start farming!")
    print()
    print(f"Here is your inventory:\n {inventory}")
    planted_seed = input("What would you like to plant? ")
    plant_count = int(input(f"How many of your {planted_seed} would you like to plant? "))
    print(f"Searching in the storage for the {plant_count} seeds....")
    sleep(1)
    plant_time = random.randint(0, 10)
    print(f"Found it! The expected plant time is {plant_time} days! You know how it is in Nunjin..very unpredictable! Please wait patiently!")
    sleep(plant_time)
    days += plant_time
    if random.randint(0,51) > 25:
        print(f"Hooray! The {planted_seed} have grown perfectly!")
        plant = seed_to_plant[planted_seed]
        inventory[plant] = plant_count
        inventory.pop(planted_seed)
        print(f"{plant_count} {plant} was added to your inventory. Time to sell and make some money!!")
    elif random.randint(0,51) < 25:
        print("Oh no...the plant did not survive.")
        inventory.pop(planted_seed)
        print("Better luck next time!")
    return days

def buy(world_market):
    global nunjin_market, sotori_market
    global coins
    global inventory
    print(f"Coins {coins}                 | XP {XP}                 | Day {days}                 | Level {level}                 | ")
    print()
    print("Welcome to the market! Your one-stop shop to buy anything!")
    print("Here you can buy farming tools, which you will need to farm and fishing tools which you would need to fish.")
    market_enter = input("Would you like to purchase items in the market? (Y/N)")
    if market_enter == "Y":
        print("Loading the market for you now!")
        sleep(0.75)
        print(world_market)
        while market_enter == "Y":
            purchase = input("What would you like to buy? (Type exit, to leave market")
            if purchase == "exit" or "Exit":
                market_enter = "N"
            else:
                pass
            print("Checking stock....")
            sleep(0.75)
            item_quantity = int(input("How many would you like to buy? "))
            if coins >= world_market[purchase]:
                print("Checking your balance....")
                print()
                sleep(0.75)
                print("Iniating money transfer...")
                print()
                print("Money Transfer Success! ")
                coins = coins - world_market[purchase]
                print(f"Your balance is now {coins}")
                if len(inventory) > 0:
                    for item in inventory:
                        if purchase not in inventory:
                            inventory[purchase] = item_quantity
                            break
                        elif purchase in inventory:
                            inventory[purchase] += item_quantity
                            break
                elif len(inventory) == 0:
                    inventory[purchase] = item_quantity
            elif coins < world_market[purchase]:
                print("Sorry you don't have enough money to make this purchase.")
    return coins

def selling():
    global inventory, my_market, coins
    print("Entering Nunjin's Busiest Farmer's Market. Here you can find the best of the best items! Do you have what it takes to sell? Let's find out!")
    print(f"This is your market: {my_market}")
    print("To add items to your market, you must move it from your inventory first!")
    print(f"Here is your inventory:\n {inventory}")
    new_market_item = input("What would you like to add to your market? ")
    market_item_price = int(input("How much would you like to sell it for? (The market is unpredictable..it may not go for what you want!)"))
    item_count = int(input("How many would you like to sell? (Note you may sell all or none) "))
    print("Setting up market now!")
    inventory[new_market_item] -= item_count
    my_market[new_market_item] = item_count
    sleep(2)
    print("Your market is now ready to sell!")
    print(f"You are selling {item_count} {new_market_item} for {market_item_price} coins!")
    if random.randint(0, 51) > 25:
        print("Oh look! A customer has come to purchase..")
        sell_price = random.randint(1, market_item_price+10)
        sell_count = random.randint(0,item_count+1)
        sleep(1.75)
        print(f"After negotiating, you have sold {sell_count} {new_market_item} for {sell_price}!!!!")
        coins += sell_price
        my_market[new_market_item] -= sell_count
    else:
        pass

def reset_stats(first, second, third):
    coins = second
    XP = first
    health = third
    days = first
    level = first

def user_guide(world):
    pass


if current_game_world == "Nunjin":
    print(f"Welcome to Nunjin! Nunjin is a coastal city that survives upon the sea! and {user_name} has just moved in!")
    print("The commands you have avalible to you in Nunjin are the following: \n Fish \n Farm \n Buy \n Inv/Inventory \n Sell \n Help")
    print()
    sleep(0.5)
    print(f"You are starting off with {coins} coins, {XP} XP at the {days} days mark! As you buy and sell the items you harvest, you gain XP which helps you to level up!")
    while game_run == True:
        sleep(1.75)
        print("Game Loading....")
        print("\n \n")
        print(f"Coins {coins}                 | XP {XP}                 | Day {days}                 | Level {level}                 | ")
        user_command = input("Please enter a command to get started: ").capitalize()
        if user_command == "Fish":
            print()
            fishing()
        elif user_command == "Farm":
            print()
            farming()
        elif user_command == "Exit":
            game_run = False
        elif user_command == "Buy":
            buy(nunjin_market)
        elif user_command == "Inv" or user_command == "Inventory":
            print()
            print(inventory)
            print("Within your market is the following: ")
            print(my_market)
            print()
        elif user_command == "Sell":
            selling()
        elif user_command == "Help":
            user_guide("Nunjin")
elif current_game_world == "Sotori":
    reset_stats(0, 50, 100)
    print(f"Welcome to Sotori! Sotori is a fictional mountainous city modeled after Japan and it's terrance farming!")
    print("The commands you have avalible to you in Sotori are the following: \n Restaurant \n Farm \n Buy \n See Inventory or See Inv \n Sell \n Help")
    print()
    sleep(0.5)
    print(f"You are starting off with {coins} coins, {XP} XP at the {days} days mark! As you buy and sell the items you harvest, you gain XP which helps you to level up!")
    while game_run == True:
        user_command = input("Please enter a command to get started: ").capitalize()
        if user_command == "Restaurant":
            pass
        elif user_command == "Sell":
            pass
        elif user_command == "Farm":
            pass
        elif user_command == "Buy":
            buy(sotori_market)
        elif user_command == "Inventory" or user_command == "Inv":
            pass
        elif user_command == "Help":
            pass
        elif user_command == "Exit":
            game_run = False
else:
    print("These worlds have not been made yet!\nFor the sake of this project, I have sticked to only two worlds, but I hope I can turn this into an actual game probably using pycharm, and finish the rest of the worlds!")