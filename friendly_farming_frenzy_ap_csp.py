import random
from time import sleep
print("Welcome to Home Away From Home! A Text-Based RPG game involving farming!\nThroughout the game, you will farm, sell items, and purchase items.")
print("You have will have an inventory which will contain your seeds, planted items, and special items. You also have a market in which you put items that you wish to sell.")
print("These are the worlds you can choose from: \n\nNunjin \n\nSotori \n")


game_worlds = ["Nunjin", "Sotori"]
current_game_world = ""
def choose_world(user_world):
    global game_worlds
    global current_game_world
    for world in game_worlds:
        if user_world == world:
            current_game_world = user_world
        elif user_world not in game_worlds:
            print("Hmmm. This world cannot be found. Be careful to spell all things correctly! Selecting the Default World:")
            current_game_world =  "Nunjin"
            break
    return current_game_world

user_world = input("Please select your world. Please use capital letters: ").capitalize()
choose_world(user_world)
print(f"\nNice! Let's get started in {current_game_world}")
user_name = input("Please type in your name: ").capitalize()

inventory = {
    "Garlic seeds" : 1 # the key is the item and the value is the quantity!
}

my_market = {}

seed_to_plant = {
    "Garlic seeds" : "Garlic cloves",
    "Onion seeds": "Onion bulbs",
    "Strawberry seeds": "Strawberries",
    "Pear seeds": "Pears",
    "Carrot seeds": "Carrots",
    "Tangerine seeds": "Tangerines",
    "Rice seeds" : "1 LB of Rice",
    "Persimmon seeds" : "Persimmons",
    "Sugar beet seeds": "Sugar Beets",
    "Daikon seeds": "Daikons",
    "Cabbage seeds": "Cabbage",
    "Taro seeds": "Taro roots",
    "Cherry seeds": "Cherries",
    "Pumpkin seeds": "Pumpkins",
}
coins = 50
XP = 0
days = 0
level = 0
game_run = True

nunjin_market = {
    "Carrot seeds": 3, #Each Key is the item and the Value is the price!
    "Tangerine seeds": 5,
    "Rice seeds" : 3,
    "Pear seeds" : 2,
    "Persimmon seeds" : 7,
    "Strawberry seeds": 12,
    "Garlic seeds": 15,
    "Onion seeds": 10,
    "Super growth ginseng": 45,
}

sotori_market = {
    "Pumpkin seeds" : 4,
    "Cherry seeds": 6,
    "Taro seeds": 3,
    "Sugar beet seeds": 5,
    "Pumpkin seeds": 2,
    "Cabbage seeds": 7,
    "Super growth ginseng": 45,
}

def farming():
    global days, level, inventory, seed_to_plant, my_market
    print("Welcome to the farm!")
    print()
    print(f"Here is your inventory:\n {inventory}")
    farm_enter = input("Would you like to enter your farm? (Y/N) ").capitalize()
    if farm_enter == "Y":
        while farm_enter == "Y":
            planted_seed = input("What would you like to plant? please type 'Exit' to exit the farm. To see your inventory, please type 'Show': ").capitalize()
            if planted_seed == "Exit":
                farm_enter = "N"
            elif planted_seed == "Show":
                get_inv(inventory)
            else:
                for item in inventory:
                    if item != planted_seed: 
                        continue
                    elif item == planted_seed:
                        break
                    else:
                        print(f"Hmmm. Looks like {planted_seed} cannot be found in your inventory. Exiting the farm now")
                plant_count_accurate = False
                while plant_count_accurate == False:
                    plant_count = int(input(f"How many of your {planted_seed} would you like to plant? "))
                    print(f"Searching in the storage for the {plant_count} seeds....\n\n")
                    if plant_count > inventory[planted_seed]:
                        print(f"Hmm. Looks like you only have {inventory[planted_seed]} amount of {planted_seed} in your inventory. Please enter a number that is equal to OR less than that")
                    else:
                        plant_count_accurate = True
                sleep(1)
                plant_time = random.randint(1, 10)
                print(f"Found it! The expected plant time is {plant_time} days! You know how it is here..very unpredictable! Please wait patiently!")
                sleep(plant_time)
                days += plant_time
                if "Super growth ginseng" in inventory:
                    print("Oh wait.. Super Growth Ginseng has been found in your inventory. This will increase your chances of growing the seed perfectly to 75%! \n Please note that once the super growth ginseng has been used, it will be removed from your inventory! You must purchase it again to experience the benefits!")
                    if random.randint(0,50) < 38: #about 75% chance
                        print(f"Hooray! The {planted_seed} have grown perfectly!")
                        plant = seed_to_plant[planted_seed]
                        inventory[plant] = plant_count
                        inventory.pop(planted_seed)
                        print(f"{plant_count} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        inventory[planted_seed] -= plant_count
                        print("Better luck next time!\n")
                    inventory.pop("Super growth ginseng")
                elif "Super growth ginseng" not in inventory:
                    if random.randint(0,50) > 25:
                        print(f"Hooray! The {planted_seed} have grown perfectly!")
                        plant = seed_to_plant[planted_seed]
                        inventory[plant] = plant_count
                        inventory.pop(planted_seed)
                        print(f"{plant_count} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        inventory[planted_seed] -= plant_count
                        print("Better luck next time!\n")
                    break
                else:
                    print("There seems to be an error of sorts. Exiting the farm. Please try again another day.")
                    days += 1
                    farm_enter = "N"
            
    elif farm_enter == "N":
        pass
    else:
        print("This is not a valid answer. Exiting the farm now \n")
    return days

def buy(world_market):
    global nunjin_market, sotori_market
    global coins
    global inventory
    global market_enter
    print(f"Coins {coins}                 | XP {XP}                 | Day {days}                 | Level {level}                 | ")
    print("\nWelcome to the market! Your one-stop shop to buy anything!")
    print("Here you can buy any tools you need as well as special upgrades.")
    market_enter = input("Would you like to purchase items in the market? (Y/N): ")
    print("Loading the market for you now!")
    sleep(0.75)
    get_market(world_market)
    while market_enter == "Y":
        purchase = input("What would you like to buy? (Type 'exit' to leave market or 'show' to see market) ").capitalize()
        if purchase == "exit" or purchase == "Exit":
            market_enter = "N"
        elif purchase == "show" or purchase == "Show":
            print("Loading market")
            get_market(world_market)
        else:
            item_quantity = int(input("How many would you like to buy? "))
            print("Checking stock....")
            sleep(0.75)
            def checking_stock(item, amount, market):
                global nunjin_market, sotori_market, market_enter
                for x in market:
                    if item in market:
                        amount *= market[item]
                        break
                    elif item not in market:
                        print(f"{item} cannot be found in the market. Leaving Market now out of embarrassment...")
                        market_enter = "N"
                        break
                return amount
            total_amount = checking_stock(purchase, item_quantity, world_market)
            def receipt(price, purchase, quantity):
                print(f"Here is your receipt {user_name}!")
                print(f"You are purchasing {quantity} {purchase} for {price} coins!")
            if coins >= total_amount and market_enter == "Y":
                print("Checking your balance....")
                print()
                sleep(0.75)
                print("Initiating money transfer... \n")
                print("Money Transfer Success! \n")
                coins = coins - total_amount
                receipt(total_amount, purchase, item_quantity)
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
            elif coins < total_amount:
                print("Sorry you don't have enough money to make this purchase.")
    return coins

def sell(world):
    global inventory, my_market, coins, market_item, item_count, days
    print(f"Entering {world}'s Busiest Farmer's Market. Here you can find the best of the best items! Do you have what it takes to sell? Let's find out!")
    print(f"This is your market stall: {my_market}\n")
    print("To add items to your market, you must move it from your inventory first!\n")
    print(f"Here is your inventory:\n {inventory}")
    new_market_item = input("What would you like to add to your market? \n If nothing, type 'Non' \n To exit the market, please type 'exit' \n To only add items to the market, and not sell type 'add'. \n Enter here: ").capitalize()
    def stock_checking(original_count, item_type):
        global inventory, my_market, market_item, new_market_item
        if original_count > inventory[item_type] or original_count != inventory[item_type]:
            new_item_count = int(input(f"Sorry, but you do not have {original_count} amount of {item_type} to sell. As a reminder, you only have {inventory[item_type]}. Please enter another quantity: "))
            inventory[item_type] -= new_item_count
            my_market[item_type] = new_item_count
            return new_item_count
        else:
            inventory[item_type] -= original_count
            my_market[item_type] = original_count
            return original_count

    if new_market_item == "Non":
        market_item = input("Please enter an item from your market that you would like to try selling!").capitalize()
        item_count = int(input("How many would you like to sell? (Note: You may only sell up to the amount in your inventory!) "))
        print("Setting up market now!")
        adjusted_item_count = stock_checking(item_count, market_item)
        sleep(2)
        print("Your market is now ready to sell!")
        print(f"You are selling {adjusted_item_count} {market_item} for {market_item_price} coins!")
        sell_confirm = input("Confirm your listing (Y/N)! ")
        if sell_confirm == "Y" or sell_confirm == "y":
            if random.randint(0, 50) > 25:
                print("Oh look! A customer has come to purchase..")
                sell_price = random.randint(1, market_item_price+10)
                sell_count = random.randint(0,item_count+1)
                sleep(1.75)
                print(f"After negotiating, you have sold {sell_count} {new_market_item} for {sell_price}!!!!")
                coins += sell_price
                my_market[new_market_item] -= sell_count
            else:
                print("Hmm..looks like nobody's around to purchase your item. The flashy ")
    elif new_market_item == "Exit":
        pass
    elif new_market_item == "Add":
        new_market_item = input("Enter item name that you would like to add to your market stall. Note: You will exit the farmer's market once you have entered the item: ")
        item_count = int(input("Enter the item count (It cannot be greater than what you have in your inventory) "))
        stock_checking(item_count, new_market_item)
        my_market[new_market_item] = item_count
    else:
        market_item_price = int(input("How much coins would you like to sell it for? (You can set it to virtually any price!) "))
        item_count = int(input("How many would you like to sell? (Note: You may only sell up to the amount in your inventory!) "))
        print("Setting up market now!")
        stock_checking(item_count, new_market_item)
        sleep(2)
        print("Your market is now ready to sell!")
        print(f"You are selling {item_count} {new_market_item} for {market_item_price} coins!")
        sell_confirm = input("Confirm your listing (Y/N)! ")
        if sell_confirm == "Y" or sell_confirm == "y":
            if random.randint(0, 50) > 25:
                print("Oh look! A customer has come to purchase..")
                sell_price = random.randint(1, market_item_price+10)
                sell_count = random.randint(0,item_count+1)
                sleep(1.75)
                print(f"After negotiating, you have sold {sell_count} {new_market_item} for {sell_price}!! Nice job. See you tomorrow!")
                coins += sell_price
                my_market[new_market_item] -= sell_count
                days += 1
            else:
                print(f"Oh no. It looks like the customer is not pleased with the items you have to sell today. Try again tomorrow")
                days += 1
        else:
            print("You did not confirm your listing.. The products have unfortunately expired. Exiting sale. Trying again tomorrow")
            days += 1
    return days


def clean_inventory_market():
    global inventory, my_market
    empty_keys = []
    for keys in inventory:
        if inventory.get(keys) == 0:
            empty_keys.append(keys)
        else:
            continue
    for keys in empty_keys:
        del inventory[keys]

    empty_keys = []   
    for keys in my_market:
        if my_market.get(keys) == 0:
            empty_keys.append(keys)
        else:
            continue
    for keys in empty_keys:
        del my_market[keys]

def get_inv(dict):
    global user_name, inventory
    print(f"{user_name}'s inventory")
    print("Item: \tQuantity")
    for key,value in dict.items():
        print(f"Item: {key}\tQuantity: {value} \n")

def get_market(dict):
    global nunjin_market, sotori_market
    print("Item: Price")
    for key, value in dict.items():
        print(f"Item: {key}\tPrice: {value} Coins \n")

def level_up(current_XP):
    global level, coins
    levels = [0, 10, 20, 30, 45, 50] #levels 0-5. 
    level_reward = False
    for level_XP in levels:
        if current_XP >= level_XP:
            level = levels.index(level_XP)
            continue
        else:
            continue
    if level == 3 and level_reward == False:
        print("Wow you have done so well! Here is 30 coins for 30 XP!")
        coins +=30
        level_reward = True

def main_game(world, market):
     global coins, XP, days, level, inventory, my_market, game_run
     while game_run == True:
        sleep(1.25)
        print("\n \n")
        print(f"Coins {coins}                 | XP {XP}                 | Day {days}                 | Level {level}                 | ")
        user_command = input("Please enter a command to get started: ").capitalize()
        random_XP = random.randrange(0,11,5)
        XP += random_XP
        level_up(XP)
        clean_inventory_market()
        if user_command == "Farm":
            print()
            farming()
        elif user_command == "Exit":
            game_run = False
        elif user_command == "Buy":
            buy(market)
        elif user_command == "Inv" or user_command == "Inventory":
            print()
            get_inv(inventory)
            print("Within your market is the following: ")
            print(my_market)
            print()
        elif user_command == "Sell":
            sell(world)
        elif user_command == "Help":
            print(f"The commands you have available to you in {world} are the following: \n Farm \n Buy \n Inv/Inventory \n Sell \n Help")
        elif coins <= 0:
            print("Uh oh....Funds just too low...")
            print("We cannot survive on this income.. We must go home..You lose")
            game_run = False
        elif level == 5:
            print("Wow. Congratulations. You have made it all the way to level 5. Thank you for playing the game. You have now completed the game. The game is now done!")
            game_run = False
        else:
            print(f"Hmmm. That command is not found. There might be a typo. Please enter the command again.")

if current_game_world == "Nunjin":
    print(f"Welcome to Nunjin! Nunjin is a fictional coastal city that survives upon the sea! {user_name} has just moved in!")
    print("The commands you have available to you in Nunjin are the following: \n Farm \n Buy \n Inv/Inventory \n Sell \n Help")
    print()
    sleep(0.5)
    print(f"You are starting off with {coins} coins, {XP} XP at the {days} days mark! As you buy and sell the items you harvest, you gain XP which helps you to level up!")
    game_run = True
    main_game("Nunjin", nunjin_market)
if current_game_world == "Sotori": 
    print(f"Welcome to Sotori! Sotori is a fictional farm town that survives upon the terrance farming and large fields! {user_name} has just moved in!")
    print("The commands you have available to you in Sotori are the following: \n Farm \n Buy \n Inv/Inventory \n Sell \n Help")
    print()
    sleep(0.5)
    print(f"You are starting off with {coins} coins, {XP} XP at the {days} days mark! As you buy and sell the items you harvest, you gain XP which helps you to level up!")
    game_run = True
    main_game("Sotori", sotori_market)
else:
    print("Hm. There has been a sudden error in the world selection process. Please start over.")
