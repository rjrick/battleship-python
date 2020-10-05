"""Holds the screens for Battleship"""
import abc
import enum

import pygame

from . import events as b_events
from . import widgets


def push_event(event_type, **kwargs):
  """A helper method for writing buttons that push events."""
  return lambda: pygame.event.post(pygame.event.Event(event_type, **kwargs))


class BaseScreen(abc.ABC):
  def __init__(self, screen: pygame.Surface, color=(220, 220, 220)):
    self.color = color
    self.surface = pygame.Surface(screen.get_size()).convert()

  @abc.abstractmethod
  def reset(self, *args, **kwargs):
    pass

  @abc.abstractmethod
  def handle_input(self, event, *args, **kwargs):
    pass

  @abc.abstractmethod
  def get_surface(self, *args, **kwargs):
    pass


class TitleScreen(BaseScreen):
  def __init__(self, screen: pygame.Surface):
    super(TitleScreen, self).__init__(screen)
    self.widgets = [
      widgets.Button('New Game', pos=(170, 190), 
                     on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.SETUP, reset=1)),
      widgets.Button('Load Game', pos=(170, 270)),
      widgets.Button('Quit Game', pos=(170, 350),
                     on_click=push_event(pygame.QUIT))
    ]

  def reset(self):
    print('Title Screen reset')

  def handle_input(self, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        push_event(pygame.QUIT)
    if event.type == pygame.MOUSEBUTTONDOWN:
      for widget in self.widgets:
        if widget.rect.collidepoint(pygame.mouse.get_pos()):
          widget.on_click()

  def get_surface(self):
    self.surface.fill(self.color)

    for w in self.widgets:
      w.draw(self.surface)

    return self.surface


class SetupScreen(BaseScreen):
  def __init__(self, screen: pygame.Surface):
    super(SetupScreen, self).__init__(screen)
    self.widgets = [
      widgets.Button('X', pos=(20, 20), width=20, height=20, on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.TITLE, reset=1)),
      widgets.Button('Start Game', pos=(245, 213),
                     on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.GAME, reset=1))
    ]

  def reset(self):
    print('Setup Screen reset')

  def handle_input(self, event: pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      for widget in self.widgets:
        if widget.rect.collidepoint(pygame.mouse.get_pos()):
          widget.on_click()

  def get_surface(self):
    self.surface.fill(self.color)

    for widget in self.widgets:
      widget.draw(self.surface)

    return self.surface


class PlacementScreen(BaseScreen):
  def __init__(self, screen: pygame.Surface):
    super(PlacementScreen, self).__init__(screen)
    self.widgets = [
        widgets.Button('Peepee')
    ]

  def reset(self):
    print('Placement loaded')

  def handle_input(self, event: pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      for widget in self.widgets:
        if widget.rect.collidepoint(pygame.mouse.get_pos()):
          widget.on_click()

  def get_surface(self):
    self.surface.fill(self.color)
    for widget in self.widgets:
      widget.draw(self.surface)

    return self.surface

class GameScreen(BaseScreen):
  def __init__(self, screen: pygame.Surface):
    super(GameScreen, self).__init__(screen)
    self.widgets = [
        widgets.Button('Pause', pos=(20, 20),
                       on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.PAUSE, reset=1))
    ]

  def reset(self):
    print('Game loaded')

  def handle_input(self, event: pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      for widget in self.widgets:
        if widget.rect.collidepoint(pygame.mouse.get_pos()):
          widget.on_click()

  def get_surface(self):
    self.surface.fill(self.color)
    for widget in self.widgets:
      widget.draw(self.surface)

    return self.surface


class PauseScreen(BaseScreen):
  def __init__(self, screen: pygame.Surface):
    super(PauseScreen, self).__init__(screen)
    self.widgets = [
      widgets.Button('X', pos=(20, 20),
                     on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.GAME, reset=1)),
      widgets.Button('New Game', pos=(245, 170),
                     on_click=push_event(b_events.CHANGE_SCREEN, screen=Screens.SETUP, reset=1)),
      widgets.Button('Save Game', pos=(245, 250),
                     on_click=push_event(b_events.SAVE_GAME)),
      widgets.Button('Load Game', pos=(245, 330),
                     on_click=push_event(b_events.LOAD_GAME)),
      widgets.Button('Exit Game', pos=(245, 410),
                     on_click=push_event(pygame.QUIT))
    ]

  def reset(self):
    print('Game paused')

  def handle_input(self, event:pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      for widget in self.widgets:
        if widget.rect.collidepoint(pygame.mouse.get_pos()):
          widget.on_click()

  def get_surface(self):
    self.surface.fill(self.color)
    for widget in self.widgets:
      widget.draw(self.surface)

    return self.surface


class Screens(enum.Enum):
  TITLE = TitleScreen
  SETUP = SetupScreen
  GAME = GameScreen
  #SUMMARY = 4
  PAUSE = PauseScreen


class ScreenManager:
  def __init__(self, screen):
    self.cur_screen: BaseScreen = None
    self.prev_screen: BaseScreen = None

    self.screens: dict[Screens, BaseScreen] = {}
    for e in Screens:
      self.screens[e] = e.value(screen)

  def display_screen(self, screen_name, reset=1):
    self.prev_screen = self.cur_screen
    self.cur_screen = self.screens[screen_name]
    if reset:
      self.cur_screen.reset()
