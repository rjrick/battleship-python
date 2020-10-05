import pygame

class Button():
  def __init__(self, text: str, font_size: int = 28, color: tuple = (64, 64, 64), 
               hover_color: tuple = None, width: int = 150, height: int = 75, 
               pos: tuple = (0, 0), on_click = None):
    self.text = text
    self.t_size = font_size
    self.color = color
    self.hover_color = hover_color or tuple((255 - x for x in color))
    self.width = width
    self.height = height
    self.pos = pos
    self.on_click = on_click if on_click else lambda: print(f'Button reading {self.text}')

  @property
  def rect(self):
    return pygame.Rect(*self.pos, self.width, self.height)

  def draw(self, surface):
    font = pygame.font.SysFont(pygame.font.get_default_font(), self.t_size)
    txt = font.render(self.text, True, (0, 0, 0))

    x_center = (self.width - txt.get_size()[0]) / 2 + self.pos[0]
    y_center = (self.height - txt.get_size()[1]) / 2 + self.pos[1]

    draw_color = self.color if not self.rect.collidepoint(pygame.mouse.get_pos()) else self.hover_color

    pygame.draw.rect(surface, draw_color, self.rect)
#    surface.blit(self.rect, self.pos)
    surface.blit(txt, (x_center, y_center))
