from pygame.math import Vector2

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
TILE_SIZE = 64

OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 14),
    'seed': (40, SCREEN_HEIGHT - 5),
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50,40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7, #players, trees, etc
    'house top':8,
    'fruit': 9,
    'rain drops': 10

}

APPLE_POSITION = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20,30), (30,10)],
    'Large': [(30, 24), (60, 65), (50,50), (16,40), (45, 50), (42,70)]
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7,
}

SALE_PRICE = {

}
PURCHASE_PRICES = {

}