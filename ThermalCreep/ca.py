#!/usr/bin/python

__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. The CA is supposed to simulate heat emission
# of an object passing through the CA grid.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

import colorsys
#import math
#import time

import pygame

#########################################################################
###                       Global Variables                            ###
#########################################################################

# The Grid of the CA
#Cells = {}
# Dimensions of the grid
GRID_WIDTH = 800
GRID_HEIGHT = 800
MAX_TEMPERATURE = 100
HEAT_FLUX = 0.5

#########################################################################
###                            CLASSES                                ###
#########################################################################


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, temperature):
        self.col = (0, 0, 0)
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.temperature = temperature
        self.temp_balance = 0
        self.persist = False
        self.neigh_temp = []

    def get_temperature(self):
        return self.temperature

    def sense_neigh(self, neighbor):
        self.temp_balance += neighbor.get_temperature()
        if neighbor.get_temperature() > 0:
            self.neigh_temp.append(neighbor.get_temperature())

    def regulate(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        i = 0
        for n in self.neigh_temp:
            if n > self.temp_balance:
                i += 1
        if i >= 2 and self.temperature < MAX_TEMPERATURE:
            self.temperature += 1
        elif self.temperature > 0:
            self.temperature -= 1

    @property
    def calculate_color_hsv(self):
        """
        Calculates the RGB values depending on the cell's current temperature.
        This method uses HSV ranges.
        :return:
        """
        h = (1 - (self.temperature / MAX_TEMPERATURE)) * 250
        red, green, blue = colorsys.hsv_to_rgb(h / 360, 1., 1.)
        return red * 255, green * 255, blue * 255

    def calculate_color(self):
        """
        Calculates the RGB values depending on the cell's current temperature.
        :return:
        """
        normalized_v = self.temperature / MAX_TEMPERATURE
        red = 0
        green = 0
        blue = 0
        if 0 <= normalized_v <= 1 / 8:
            red = 0
            green = 0
            blue = 4 * normalized_v + 0.5
        elif 1 / 8 < normalized_v <= 3 / 8:
            red = 0
            green = 4 * normalized_v - 0.5
            blue = 1
        elif 3 / 8 < normalized_v <= 5 / 8:
            red = 4 * normalized_v - 1.5
            green = 1
            blue = -4 * normalized_v + 2.5
        elif 5 / 8 < normalized_v <= 7 / 8:
            red = 1
            green = -4 * normalized_v + 3.5
            blue = 0
        elif 7 / 8 < normalized_v <= 1:
            red = -4 * normalized_v + 4.5
            green = 0
            blue = 0
        else:
            pass

        return red * 255, green * 255, blue * 255

    def draw(self, surf):
        #print("new color: (%i,%i,%i)" % (red, green, blue))
        self.col = self.calculate_color()
        pygame.draw.rect(surf, self.col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)


#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################
# The following methods are used to manipulate the CA grid


def draw_cells(ca_grid, screen):
    for y in range(0, int(GRID_HEIGHT / 10)):
        for x in range(0, int(GRID_WIDTH / 10)):
            ca_grid[x, y].draw(screen)


def init_ca():
    """
    Initializes and returns the cellular automaton.
    The CA is a dictionary and not a list of lists
    :return: The initialized CA.
    """
    ca_grid = {}
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            ca_grid[x, y] = ClassCell(x, y, 0)

    return ca_grid


def cycle_ca(ca_grid):
    ca_grid = update_from_neighs(ca_grid)
    ca_grid = update_states(ca_grid)
    return ca_grid


#########################################################################
###                    UPDATE FROM NEIGHBOR METHODS                   ###
#########################################################################


def update_from_neighs(ca_grid):
    """
    Looping over all cells to gather all the neighbor information they need to update
    """
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            if y - 1 > -1 and x - 1 > -1 and x + 1 < width and y + 1 < height:
                ca_grid[x, y].sense_neigh(ca_grid[(x - 1), (y - 1)])  #Top Left
                ca_grid[x, y].sense_neigh(ca_grid[x, (y - 1)])  #Top
                ca_grid[x, y].sense_neigh(ca_grid[(x + 1), (y - 1)])  #Top Right
                ca_grid[x, y].sense_neigh(ca_grid[(x - 1), (y + 1)])  #Bottom Left
                ca_grid[x, y].sense_neigh(ca_grid[x, (y + 1)])  #Bottom
                ca_grid[x, y].sense_neigh(ca_grid[(x + 1), (y + 1)])  #Bottom Right
                ca_grid[x, y].sense_neigh(ca_grid[(x - 1), y])  #Left
                ca_grid[x, y].sense_neigh(ca_grid[(x + 1), y])  #Right
    return ca_grid


#########################################################################
###                       UPDATE STATES METHODS                       ###
#########################################################################


def update_states(ca_grid):
    """
    After executing update_neighs this is the actual update of the cell itself
    """
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            ca_grid[x, y].regulate()
    return ca_grid