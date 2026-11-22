import random
import pygame

class Block:
    def __init__(self, x, y, width, height, color, speed=0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.speed = speed
        self.direction = 1

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def update(self, screen_width):
        if self.speed == 0:
            return

        self.x += self.speed * self.direction
        if self.x <= 20:
            self.x = 20
            self.direction = 1
        elif self.x + self.width >= screen_width - 20:
            self.x = screen_width - 20 - self.width
            self.direction = -1

    def render(self, surface):
        draw_rect = self.rect
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=4)
        pygame.draw.rect(surface, (245, 245, 250), draw_rect, width=2, border_radius=4)


class Debris:
    def __init__(self, x, y, width, height, color):
        self.x = float(x)
        self.y = float(y)
        self.width = float(max(2.0, width))
        self.height = float(height)
        self.color = color
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(1.0, 3.0)
        self.gravity = 0.5
        self.angle = 0.0
        self.rot_speed = random.uniform(-6.0, 6.0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.angle += self.rot_speed

    def render(self, surface):
        debris_surf = pygame.Surface((max(2, int(self.width)), max(2, int(self.height))), pygame.SRCALPHA)
        debris_rect = debris_surf.get_rect()
        pygame.draw.rect(debris_surf, self.color, debris_rect, border_radius=2)
        pygame.draw.rect(debris_surf, (220, 220, 230), debris_rect, width=1, border_radius=2)
        rotated = pygame.transform.rotate(debris_surf, self.angle)
        rot_rect = rotated.get_rect(center=(int(self.x + self.width / 2), int(self.y + self.height / 2)))
        surface.blit(rotated, rot_rect.topleft)

    @property
    def is_offscreen(self):
        return self.y > 650
