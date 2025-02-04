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
            print("5. Settings 🛒")
            print("6. Quit 🚪")

            choice = input("Select an option: ")
            if choice == "1":
                self.player.fishing.cast_line(self.player)
            elif choice == "2":
                seed = input("What would you like to plant? please type 'Exit' to exit the farm. To see your inventory, please type 'Show': ").capitalize()
                crop_amount = int(input("How many would you like to plant? "))
                maintenance = self.player.farming.farm_maintenance(seed, crop_amount, self.player)
                print(maintenance)
                if maintenance == True:
                    self.player.farming.plant_crop(seed, self.player, crop_amount)
                else:
                    print("Please try again.")
                    while maintenance == False:
                        seed = input("What would you like to plant? please type 'Exit' to exit the farm. To see your inventory, please type 'Show': ").capitalize()
                        crop_amount = int(input("How many would you like to plant? "))
                        maintenance = self.player.farming.farm_maintenance(seed, crop_amount, self.player)
                        if maintenance == True:
                            self.player.farming.plant_crop(seed, crop_amount, self.player)
                        else:
                            print("Please try again.")
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
                self.player.market.sell(self.player)
            elif choice == "5":
                print("Settings Menu")
                print("1. Show Stats")
                print("2. Show Inventory")
                print("3. Show Market")
                print("4. Show My Market")
                print("5. Show Recipes")
                print("6. Exit")
                choice = input("Select an option: ")
                if choice == "1":
                    self.player.show_stats()
                elif choice == "2":
                    self.player.get_inv()
                elif choice == "3":
                    self.player.market.show_market()
                elif choice == "4":
                    self.player.get_market()
                elif choice == "5":
                    print("Recipes")
                    for recipe, ingredients in self.player.restaurant.recipes.items():
                        print(f"{recipe}: {ingredients}")
            elif choice == "6":
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
        self.my_market = {"Pears": {"count": 5, "price": 10}}
        self.menu = {}
        self.unlocked_recipes = ["Takoyaki"]
        self.fishing = Fishing(world)
        self.farming = Farming(world)
        self.market = Market(world)
        self.restaurant = Restaurant()
        self.upgrades = Upgrades()
        self.reputation = 0
        self.loan = 0
        self.loan_due_days = 0

    def show_stats(self):
        print(f"Player: {self.name} | World: {self.world} | Coins: {self.coins} | XP: {self.xp} | Days: {self.days} | Level: {self.level}")

    def update_coins(self, amount):
        self.coins += amount
        print(f"Updated coins: {self.coins}")

    def clean_inv_market(self):
            empty_keys = []
            for keys in self.inventory:
                if self.inventory.get(keys) == 0:
                    empty_keys.append(keys)
                else:
                    continue
            for keys in empty_keys:
                del self.inventory[keys]

            empty_keys = []   
            for keys in self.my_market:
                if self.my_market.get(keys) == 0:
                    empty_keys.append(keys)
                else:
                    continue
            for keys in empty_keys:
                del self.my_market[keys]

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
        print("\n--- Your Market Stall ---")
        for item, details in self.my_market.items():
            print(f"{item}: {details['count']} available | Price: {details['price']} coins")
    
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

            self.recipes = {
                "Takoyaki": [["Octopus", 3], ["Flour", 2]],
                "Risotto": [["Rice", 2]],}
            
            self.menu_prices = {}
        else:
            self.market = {}  # Default empty market
            self.sea_creatures = {}

class Market:
    '''
    As reputation grows, better customers arrive:

📦 Bulk Buyers: Purchase items in large amounts 💰
👑 VIP Customers: Pay 25%-50% above max price ✨
📜 Contract Buyers: Request specific items for HUGE profits 📈
    '''
    def __init__(self, world):
        self.world = world
        self.base_prices = {
                "Carrots": 3,
                "Tangerines": 5,
                "Rice seeds" : 3,
                "Pears" : 2,
                "Persimmons" : 7,
                "Strawberries": 12,
                "Garlic cloves": 15,
                "Onion bulbs": 10,
        }

        self.acceptable_range_multiplier = (0.8, 1.2)  # Starts with ±20% range

    

    def check_sale_chance(self, item, listed_price):
        """Determines if an item sells based on pricing, with a small chance of negotiation."""
        base_price = self.base_prices.get(item, None)
        if base_price is None:
            return False, None  # Item not recognized

        acceptable_range = (self.acceptable_range_multiplier[0] * base_price,
                            self.acceptable_range_multiplier[1] * base_price)

        if acceptable_range[0] <= listed_price <= acceptable_range[1]:
            sale_chance = 0.75  # 75% chance of selling
        elif listed_price < acceptable_range[0]:
            sale_chance = 1.0  # Sells instantly, but at a loss
        else:
            sale_chance = max(0.1, 1.5 - (listed_price / base_price))  # Decreases if overpriced

        sale_attempt = random.random()

        if sale_attempt < sale_chance:
            return True, listed_price  # Item sold at listed price
        elif sale_attempt < sale_chance + 0.05:  # 5% chance of negotiation
            return True, self.negotiate_price(listed_price)
        return False, None  # Item did not sell

    def negotiate_price(self, listed_price):
        """Handles a negotiation attempt for overpriced items."""
        min_offer = int(0.85 * listed_price)
        max_offer = int(0.95 * listed_price)
        return random.randint(min_offer, max_offer)


    def buy(self, item, item_quantity, player):
        total_price = self.world.market[item] * item_quantity
        if item in self.world.market and player.coins >= total_price:
            player.inventory[item] = player.inventory.get(item, 0) + 1
            player.coins -= total_price
            print(f"🛒 You bought {item_quantity} {item} for {total_price} coins.")
            print(f"Your balance is now {player.coins}")
        else:
            print("🚫 Not enough coins or item unavailable.")

    def sell(self, player):
        print(f"\nWelcome to  Busiest Farmer's Market! 🏪")
        print("Manage your stall, set prices, and attract customers!")
        
        while True:
            print("\n--- Your Market Stall ---")
            for item, details in player.my_market.items():
                print(f"{item}: {details['count']} available | Price: {details['price']} coins")
            
            print("\nYour Inventory:")
            for item, count in player.inventory.items():
                print(f"{item}: {count} in stock")
            
            print("\nOptions:")
            print("1. Add an item to the stall")
            print("2. Adjust item price")
            print("3. Start selling")
            print("4. Exit Market")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                item = input("Enter item to add: ").capitalize()
                if item in player.inventory and player.inventory[item] > 0:
                    count = int(input(f"How many {item} to add? (You have {player.inventory[item]}): "))
                    if count > player.inventory[item]:
                        print("Not enough in inventory!")
                        continue
                    price = int(input("Set your selling price per item: "))
                    player.inventory[item] -= count
                    if item in player.my_market:
                        player.my_market[item]['count'] += count
                        player.my_market[item]['price'] = price
                    else:
                        player.my_market[item] = {'count': count, 'price': price}
                    print(f"Added {count} {item} at {price} coins each!")
                else:
                    print("Item not available in inventory!")
            
            elif choice == "2":
                item = input("Enter item to adjust price: ").capitalize()
                if item in player.my_market:
                    new_price = int(input("Enter new price: "))
                    player.my_market[item]['price'] = new_price
                    print(f"Updated {item} price to {new_price} coins!")
                else:
                    print("Item not in your stall!")
            
            elif choice == "3":
                print("\n🛒 Customers are arriving... Let's see who buys!")
                for item, details in list(player.my_market.items()):
                    sell_count = random.randint(1, details['count'])
                    price = details['price']

                    # Check if the item sells based on pricing logic
                    sold, final_price = self.check_sale_chance(item, price)

                    if sold:
                        total_price = sell_count * final_price
                        player.coins += total_price
                        player.my_market[item]['count'] -= sell_count
                        print(f"🎉 Sold {sell_count} {item} for {total_price} coins!")
                        if final_price != price:
                            print(f"💰 Negotiated price: {final_price} coins per unit.")

                        if player.my_market[item]['count'] == 0:
                            del player.my_market[item]
                    else:
                        print(f"❌ No buyers for {item} today.")

                player.days += 1
                print(f"You now have {player.coins} coins.")
                break
            
            elif choice == "4":
                print("Exiting market...")
                break
            else:
                print("Invalid choice, try again!")

    def show_market(self):
        print(f"\n---Market Items ---")
        for item, price in self.world.market.items():
            print(f"{item}: {price} coins")

class Farming:
    '''
    🚜 Farming Enhancements
        Livestock →

        Cows for milk, chickens for eggs, etc.
        Animals need feeding and care (maybe auto-feeders later?).
        Different breeds could produce different quality products.
        Automated Farming →

        Buy sprinklers for auto-watering crops.
        Add mechanical harvesters for faster collection.
        A farmhand system where NPCs or robots help maintain fields.
    '''
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

    def farm_maintenance(self, crop, crop_count, player):
        if crop not in player.inventory.keys():
            print(f"{crop} cannot be found!")
            return False
        elif crop in player.inventory:
            print(f"Searching in the storage for the {crop_count} seeds....\n\n")
            if crop_count > player.inventory[crop]:
                print(f"Hmm. Looks like you only have {player.inventory[crop]} amound of {crop} in your inventory. Please enter a number that is equal to OR less than that")
                return False
            else:
                return True

    def plant_crop(self, crop, player, crop_amount):
        if crop in self.world.market:
                sleep(1)
                plant_time = random.randint(1, 8)
                print(f"Found it! The expected plant time is {plant_time} days! You know how it is here..very unpredictable! Please wait patiently!")
                sleep(plant_time)
                player.days += plant_time
                if "Super growth ginseng" in player.inventory:
                    print("Oh wait.. Super Growth Ginseng has been found in your inventory. This will increase your chances of growing the seed perfectly to 75%! \n Please note that once the super growth ginseng has been used, it will be removed from your inventory! You must purchase it again to experience the benefits!")
                    if random.randint(0,50) < 38: #about 75% chance
                        print(f"Hooray! The {crop} have grown perfectly!")
                        plant = self.seed_to_plant[crop]
                        player.inventory[crop] = crop_amount
                        player.inventory.pop(crop)
                        print(f"{crop_amount} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        player.inventory[crop] -= crop_amount
                        print("Better luck next time!\n")
                        player.inventory.pop("Super growth ginseng")
                elif "Super growth ginseng" not in player.inventory:
                    if random.randint(0,50) > 25:
                        print(f"Hooray! The {crop} have grown perfectly!")
                        plant = self.seed_to_plant[crop]
                        player.inventory[plant] = crop_amount
                        player.inventory.pop(crop)
                        print(f"{crop_amount} {plant} was added to your inventory. Time to sell and make some money!! \n")
                    else:
                        print("Oh no...the plant did not survive.")
                        player.inventory[crop] -= crop_amount
                        print("Better luck next time!\n")
                        
        else:
            print(f"🚫 {crop} is not available in this world.")

class Fishing:
    ''' 
    🎣 Fishing Expansion
        Fishing Rod Upgrades →

        Basic rods catch common fish, better rods allow for deeper fishing.
        Maybe a durability system where rods need repairs?
        Bait & Lures →

        Some fish only bite on certain bait types.
        Could be craftable or purchasable at a fishing shop.
        Fishing Tournaments →

        Timed events where players compete to catch the biggest or rarest fish.
        Rewards could include exclusive rods, bait, or money.
    '''
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
    ''' 🍽️ Restaurant Growth
            Menu Customization →

            Players choose what dishes to serve based on available ingredients.
            Some dishes might be more profitable based on trends.
            Customers could have preferences, and serving the right dishes could boost reputation.
            Restaurant Chains →

            Start with a small diner and expand to bigger or multiple locations.
            Each location could have unique demands (e.g., a seaside restaurant focuses on fish dishes).
            Food Reviews & Reputation →

            Customers leave ratings based on food quality and service speed.
            Good ratings attract VIP customers who pay extra.
            A restaurant rank system could unlock better ingredients or perks.'''
    
    def __init__(self):
        self.menu_prices = {
            "Takoyaki": 15,
            "Risotto": 10,
        }

    def cook(self, dish, player):
        if dish in self.menu:
            print(f"👨‍🍳 You cooked {dish}! You can sell it for {self.menu[dish]} coins.")
        else:
            print("🚫 This dish is not in your restaurant menu.")

class Upgrades:
    # manages upgrades special perks, etc
    def __init__(self):
        self.upgrade_levels = {
            "price_range_boost": {"reputation": 10},  # Expands price range
            "better_customers": {"reputation": 20},  # Unlocks high-tier customers
            "bigger_stall": {"level": 5},  # Increases stall size
            "loan_discount": {"reputation": 40},  # Reduces loan interest
        }
        self.unlocked_upgrades = set()

    def check_upgrades(self, player):
        for upgrade, conditions in self.upgrade_levels.items():
            if upgrade not in self.unlocked_upgrades:
                if all(getattr(player, key, 0) >= value for key, value in conditions.items()):
                    self.unlocked_upgrades.add(upgrade)
                    print(f"🎉 Upgrade unlocked: {upgrade.replace('_', ' ').title()}!")

    def apply_upgrades(self, market, player):
        if "price_range_boost" in self.unlocked_upgrades:
            market.acceptable_range_multiplier = (0.7, 1.3)
        if "better_customers" in self.unlocked_upgrades:
            market.high_tier_customers = True
        if "bigger_stall" in self.unlocked_upgrades:
            market.stall_size += 5
        if "loan_discount" in self.unlocked_upgrades:
            player.loan_interest_rate = 0.05  # Lower loan interest
        if "bulk_selling" in self.unlocked_upgrades:
            market.bulk_selling_enabled = True


# Main Game Execution
game = Game()
game.start_game()

game.main_menu()