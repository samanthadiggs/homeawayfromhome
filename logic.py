import random
from time import sleep

class Game:
    # This will manage the game state, such as the world selection, player details, inventory, and main game loop.
    def __init__(self):
        self.game_worlds = ["Nunjin", "Sotori"]
        self.current_game_world = None
        self.player = None

    def start_game(self):
        print("Welcome to Home Away From Home! A Text-Based RPG game teaching students about agricultural practices from around the world!")
        print("There are two worlds you can choose from, each with its own gameplay: Nunjin & Sotori")

        user_world = input("Please select your world. Please use capital letters: ").capitalize()
        self.current_game_world = self.choose_world(user_world)

        user_name = input("Please type in your name: ").capitalize()
        self.player = Player(user_name, self.current_game_world)

        print(f"\nNice! Let's get started in {self.current_game_world}")

    def choose_world(self, user_world):
        if user_world in self.game_worlds:
            return World(user_world)
        else:
            print("Hmmm. This world cannot be found. Selecting the Default World: Nunjin")
            return World("Nunjin")
      
    def main_menu(self):
        while True:
            print(f"\n--- Main Menu ---")
            print(f"Coins: {self.player.coins} | XP: {self.player.xp} | Day: {self.player.days} | Level: {self.player.level}")
            print("1. Go Fishing 🎣")
            print("2. Go Farming 🌱")
            print("3. Visit Market 🏪")
            print("4. Sell Items 🛒")
            print("5. Quit 🚪")

            choice = input("Select an option: ")
            if choice == "1":
                self.player.fishing.cast_line(self.player)
            elif choice == "2":
                seed = input("What would you like to plant? please type 'Exit' to exit the farm. To see your inventory, please type 'Show': ").capitalize()
                crop_amount = int(input("How many would you like to plant? "))

                self.player.farming.plant_crop(seed, self.player, crop_amount)
            elif choice == "3":
                print("\nWelcome to the market! Your one-stop shop to buy anything!")
                print("Here you can buy any tools you need as well as special upgrades.")
                print("Loading the market for you now!")
                sleep(0.75)
                self.player.market.show_market()
                item = input("What would you like to buy? (Type 'exit' to leave market or 'show' to see market) ").capitalize()
                amount = int(input("How many would you like to buy? "))
                self.player.market.buy(item, amount, self.player)
            elif choice == "4":
                self.player.market.sell(item, self.player)
            elif choice == "5":
                print("Thanks for playing! See you next time!")
                break
            else:
                print("Invalid option. Try again.")

class Player:
    # This will handle player attributes like inventory, coins, XP, level, etc.
    def __init__(self, name, world):
        self.name = name
        self.world = world
        self.coins = 50
        self.xp = 0
        self.days = 0
        self.level = 0
        self.inventory = {"Garlic seeds": 1}
        self.my_market = {}
        self.unlocked_recipes = ["Takoyaki"]
        self.fishing = Fishing(world)
        self.farming = Farming(world)
        self.market = Market(world)
        self.restaurant = Restaurant()

    def show_stats(self):
        print(f"Player: {self.name} | World: {self.world} | Coins: {self.coins} | XP: {self.xp} | Days: {self.days} | Level: {self.level}")

    def update_coins(self, amount):
        self.coins += amount
        print(f"Updated coins: {self.coins}")
    
    def level_up(self):
        levels = [0, 10, 20, 30, 45, 50, 65, 85, 90, 95, 100, 130, 150, 175, 180, 195, 200, 225, 240, 250, 260]
        for level_XP in levels:
            if self.xp >= level_XP:
                self.level = levels.index(level_XP)
                continue
            else:
                continue
        if self.level == 10:
            print("Wow you have done so well! Here is 100 coins for 100 XP!")
            self.coins +=100
        elif self.level == 16:
            print("Wow level 16? You have done great! Here is 160 coins!")
            self.coins += 160

    def get_inv(self):
        print(f"{self.name}'s inventory")
        print("Item: \tQuantity")
        for key,value in self.inventory.items():
            print(f"Item: {key}\tQuantity: {value} \n")

    def get_market(self):
        print("Item: Price")
        for key, value in self.my_market.items():
            print(f"Item: {key}\tPrice: {value} Coins \n")
    
class World:
    def __init__(self, name):
        self.name = name

        if name == "Nunjin":
            self.market = {
                "Fishing rod":10, #Each Key is the item and the Value is the price!
                "Golden fishing rod": 25,
                "Carrot seeds": 3,
                "Tangerine seeds": 5,
                "Rice seeds" : 3,
                "Pear seeds" : 2,
                "Persimmon seeds" : 7,
                "Strawberry seeds": 12,
                "Garlic seeds": 15,
                "Onion seeds": 10,
                "Super growth ginseng": 45,
                "Special fish bait": 75,
            }
            self.sea_creatures = {
                "Turban shells": 20, # Each Key is the sea creature and the value is how much it is worth!
                "Sea cucumbers": 40, 
                "Mackerel": 10, 
                "Abalone": 5, 
                "Hairtail fish": 20, 
                "Sea Urchin": 13, 
                "Cuttlefish":17, 
                "Octopus": 11, 
                "Cutlassfish": 35, 
                "Shrimp": 1
            }
        elif name == "Sotori":
            self.market = {
                "Fishing rod": 9,
                "Sugar Beet seeds":10,
                "Daikon seeds": 7,
                "Cabbage seeds": 6,
                "Taro seeds": 5,
                "Carrot seeds": 10,
                "Cherry seeds": 13,
                "Pumpkin seeds": 17,
                "Onion seeds": 8,
                "Promotional flyer" : 75,
                "Super growth ginseng": 45,
            }
            self.sea_creatures = {
                "Octopus": 13,
                "Shrimp": 2,
                "Eel": 5,
            }
        else:
            self.market = {}  # Default empty market
            self.sea_creatures = {}

class Market:
    def __init__(self, world):
        self.world = world

    def buy(self, item, item_quantity, player):
        total_price = self.world.market[item] * item_quantity
        if item in self.world.market and player.coins >= total_price:
            player.inventory[item] = player.inventory.get(item, 0) + 1
            player.coins -= total_price
            print(f"🛒 You bought {item_quantity} {item} for {total_price} coins.")
        else:
            print("🚫 Not enough coins or item unavailable.")

    def sell(self, item, player):
        if item in player.inventory:
            value = self.world.market.get(item, 5)  # Default sell price if not in world market
            player.coins += value
            player.inventory[item] -= 1
            if player.inventory[item] == 0:
                del player.inventory[item]
            print(f"💰 You sold {item} for {value} coins.")
        else:
            print("🚫 You don't have that item.")

    def show_market(self):
        print(f"\n---Market Items ---")
        for item, price in self.world.market.items():
            print(f"{item}: {price} coins")

class Farming:
    def __init__(self, world):
        self.world = world
        self.farm = {}  # Stores player's planted crops
        self.seed_to_plant = {
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
            #maps the seeds to the plant
        }

    def farm_maintenance(crop, crop_count, player):
        for x in player.inventory:
            if crop not in player.inventory:
                print(f"{crop} cannot be found!")
                break
            elif crop in player.inventory:
                plant_count_accurate = False
                while plant_count_accurate == False:
                    print(f"Searching in the storage for the {crop_count} seeds....\n\n")
                    if plant_count > player.inventory[crop]:
                        print(f"Hmm. Looks like you only have {player.inventory[crop]} amound of {crop} in your inventory. Please enter a number that is equal to OR less than that")
                    else:
                        plant_count_accurate = True

    def plant_crop(self, crop, player, crop_amount):
        if crop in self.world.market:
            for item in player.inventory:
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
                if "Super growth ginseng" in player.inventory:
                    print("Oh wait.. Super Growth Ginseng has been found in your inventory. This will increase your chances of growing the seed perfectly to 75%! \n Please note that once the super growth ginseng has been used, it will be removed from your inventory! You must purchase it again to experience the benefits!")
                    if random.randint(0,50) < 38: #about 75% chance
                        print(f"Hooray! The {planted_seed} have grown perfectly!")
                        plant = seed_to_plant[planted_seed]
                        player.inventory[plant] = plant_count
                        player.inventory.pop(planted_seed)
                        print(f"{plant_count} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        player.inventory[planted_seed] -= plant_count
                        print("Better luck next time!\n")
                        player.inventory.pop("Super growth ginseng")
                elif "Super growth ginseng" not in player.inventory:
                    if random.randint(0,50) > 25:
                        print(f"Hooray! The {planted_seed} have grown perfectly!")
                        plant = seed_to_plant[planted_seed]
                        player.inventory[plant] = plant_count
                        player.inventory.pop(planted_seed)
                        print(f"{plant_count} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        player.inventory[planted_seed] -= plant_count
                        print("Better luck next time!\n")
                        break
        else:
            print(f"🚫 {crop} is not available in this world.")

class Fishing:
    def __init__(self, world):
        self.world = world  # Get the current world to determine available fish

    def cast_line(self, player):
        if not self.world.sea_creatures:
            print("There are no sea creatures in this world.")
            return
        
        if len(player.inventory) == 0:
            print("Uh oh, your inventory is empty!")
        elif len(player.inventory) > 0:
            for item in player.inventory:
                if "Fishing rod" not in player.inventory:
                    print("Uh oh! Looks like you need to go buy a fishing rod!")
                    break
                elif "Fishing rod" in player.inventory:
                    if random.randint(0, 100) < 25:
                        caught_fish = random.choice(list(self.world.sea_creatures.keys()))
                        print("Waiting....")
                        sleep(1)
                        print("Still waiting....")
                        sleep(0.75)
                        print(f"Hooray, you caught {caught_fish}! {caught_fish} is worth {self.world.sea_creatures[caught_fish]}")
                        player.inventory[caught_fish] = player.inventory.get(caught_fish, 0) + 1
                    elif random.randint(0,100) > 25:
                        print("Sorry bad catch day. Better luck next time!")
                    break
    
class Restaurant:
    def __init__(self):
        self.menu = {
            "Grilled Fish": 15,
            "Pumpkin Soup": 10,
        }
        self.recipes = {
            "Takoyaki": [["Octopus", 3], ["Flour", 2]],
            "Risotto": [["Rice", 2]],
        }

    def cook(self, dish, player):
        if dish in self.menu:
            print(f"👨‍🍳 You cooked {dish}! You can sell it for {self.menu[dish]} coins.")
        else:
            print("🚫 This dish is not in your restaurant menu.")




# Main Game Execution
game = Game()
game.start_game()

game.main_menu()