
import enum
import sys

import battleship.events as b_events
import pygame

from battleship.screens import ScreenManager, Screens


class Direction(enum.Enum):
  UP = (0, -1)
  RIGHT = (0, 1)
  DOWN = (0, 1)
  LEFT = (-1, 0)


class Ship(enum.Enum):
  CARRIER = 5
  BATTLESHIP = 4
  DESTROYER = 3
  SUBMARINE = 3
  PATROL_BOAT = 2


class HitStatus(enum.Enum):
  MISSED = -1
  UNKNOWN = 0
  HIT = 1


class Player:
  def __init__(self, robot: bool, grid_size: int = 8):
    self.hit_board = [[None for _ in range(grid_size)] for __ in range(grid_size)]
    self.ship_board = [[None for _ in range(grid_size)] for __ in range(grid_size)]
    
    self.is_robot = robot

    # Number of hits on your ships
    self.hit_spots = 0

  def can_place_ship(self, pos: tuple, boat: Ship, direction: Direction):
    end_x = pos[0] + boat.value*direction.value[0]
    end_y = pos[1] = boat.value*direction.value[1]

    if end_x < 0 or end_x >= len(self.hit_board) or \
       end_y < 0 or end_y >= len(self.hit_board):
       return False
    return True

  def place_ship(self, pos: tuple, boat: Ship, direction: Direction):
    if not can_place_ship(pos, boat, direction):
      return

    for i in range(boat.value):
      cur_x = pos[0]+direction.value[0]*i
      cur_y = pos[1]+direction.value[1]*i
      self.ship_board[cur_y][cur_x] = boat
    self.hit_spots += boat.value 


class Game:
  def __init__(self, players: list, grid_size: int = 8):
    """"""
    self.players = []
    for robot in players:
      self.players.append(Player(robot, grid_size))
  

def game_loop():
  pygame.init()
  screen: pygame.Surface = pygame.display.set_mode((640, 480))
  pygame.display.set_caption('Battleship')

  # Setup section
  manager = ScreenManager(screen)
  manager.display_screen(Screens.TITLE)

  # Game section
  while 1:
    # Event handling
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit(0)
      if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        manager.cur_screen.handle_input(event)
      if event.type == b_events.CHANGE_SCREEN:
        manager.display_screen(event.screen, reset=event.reset)


    # Game logic updates

    # Game drawing
    # Wipe screen
    screen.fill((0, 0, 0))

    # Draw the surface of the current screen.
    screen.blit(manager.cur_screen.get_surface(), (0, 0))

    pygame.display.flip()
