import pygame
from os import walk

def import_folder(path):
    surface_list = [] #stores all the surfaces

    for __, __, img_files in walk(path): #walk returns a list with all of the contents of the folder
        for img in img_files:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
