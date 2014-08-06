__author__ = 'Michael Wagner'
__version__ = '1.0'


#########################################################################
###                            CLASSES                                ###
#########################################################################


class GlobalConstants:
    def __init__(self):
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.NUM_AGENTS = 200
        self.LANDSCAPE_MODE = 2  # 3 = twohill, 2 = procedural, 1 = randomized
        self.RUN_SIMULATION = False
        self.CELL_SIZE = 15
        self.GRID_WIDTH = int(500 / 10) * self.CELL_SIZE
        self.GRID_HEIGHT = int(500 / 10) * self.CELL_SIZE
        #self.ABM_BOUNDS = (0, 10, 40, 50)
        #self.ABM_BOUNDS = (0, 50, 0, 50)
        self.ABM_BOUNDS = (15, 35, 15, 35)
        self.TICKS = 0
        self.MS_PER_TICK = 60
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.MIN_METABOLISM = 1
        self.MAX_METABOLISM = 4
        self.VISION = 6
        self.M_FERTILITY_START = 15
        self.F_FERTILITY_START = 15
        self.M_FERTILITY_END = (50, 60)
        self.F_FERTILITY_END = (40, 50)
        self.MAX_AGENT_LIFE = 100
        self.STARTING_SUGAR = (20, 40)
        ################################
        #         CA CONSTANTS         #
        ################################
        self.MAX_SUGAR = 4
        self.GROWTH_PER_TICK = 1
        self.GROWTH_PERIOD = 1
        self.TOROIDAL = False