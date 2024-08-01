import pygame
import os

def import_folder(path):
    surface_list = []

    for _, __, img_files in os.walk(path):
        for image in img_files:
            if "IDENTIFIER" not in image:  # Exclure les fichiers contenant "IDENTIFIER"
                full_path = os.path.join(path, image)
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                except pygame.error as e:
                    print(f"Failed to load image at {full_path}: {e}")

    if not surface_list:
        raise FileNotFoundError(f"No images found in the folder: {path}")

    return surface_list

from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
    surface_list = []

    for _, __, img_files in os.walk(path):
        for image in img_files:
            if "IDENTIFIER" not in image:  # Exclure les fichiers contenant "IDENTIFIER"
                full_path = os.path.join(path, image)
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                except pygame.error as e:
                    print(f"Failed to load image at {full_path}: {e}")

    if not surface_list:
        raise FileNotFoundError(f"No images found in the folder: {path}")

    return surface_list
