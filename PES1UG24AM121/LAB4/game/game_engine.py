import random
import pygame
from game.block import Block, Debris


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)
        self.font_bonus = pygame.font.SysFont(None, 32)

        # Starfield for high altitude atmosphere
        self.stars = [
            (random.randint(0, self.width), random.randint(0, self.height), random.randint(1, 2))
            for _ in range(45)
        ]

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def get_atmospheric_background(self):
        """
        Task 4: Calculate atmospheric background color shift based on stack height.
        Interpolates smoothly across atmospheric layers as the tower rises.
        """
        alt = len(self.stack) - 1

        # Color checkpoints (height_threshold, (R, G, B))
        keyframes = [
            (0,  (28, 30, 48)),    # Sea level / Twilight city
            (5,  (45, 35, 68)),    # Planetary Boundary Layer
            (10, (25, 55, 95)),    # Troposphere (Deep Cyan-Blue)
            (18, (18, 35, 80)),    # Stratosphere (Navy/Cobalt)
            (28, (12, 18, 45)),    # Mesosphere (Deep Indigo)
            (40, (5, 6, 15)),      # Thermosphere / Exosphere (Cosmic Void)
        ]

        for i in range(len(keyframes) - 1):
            h0, c0 = keyframes[i]
            h1, c1 = keyframes[i + 1]
            if h0 <= alt <= h1:
                t = (alt - h0) / float(h1 - h0)
                r = int(c0[0] + t * (c1[0] - c0[0]))
                g = int(c0[1] + t * (c1[1] - c0[1]))
                b = int(c0[2] + t * (c1[2] - c0[2]))
                return (r, g, b)

        return keyframes[-1][1]

    def reset(self):
        self.score = 0
        self.game_over = False
        self.perfect_streak = 0
        self.perfect_message_timer = 0
        self.perfect_message = ""
        self.debris_list: list[Debris] = []

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60
        base_block = Block(base_x, base_y, self.base_width, self.block_height, self.get_color(0), speed=0)
        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]
        next_y = top_block.y - self.block_height - 4
        speed = min(10.0, 4.5 + (len(self.stack) * 0.35))
        color = self.get_color(len(self.stack))

        start_x = 25 if random.choice([True, False]) else self.width - 25 - top_block.width
        self.active_block = Block(start_x, next_y, top_block.width, self.block_height, color, speed=speed)

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)
        right = min(act.x + act.width, top_block.x + top_block.width)
        overlap = right - left

        # Task 1: Fix inverted overlap placement bug
        is_successful_drop = overlap > 0

        if is_successful_drop:
            # Task 2: Implement "Perfect Placement" bonus & width restoration
            offset = abs(act.x - top_block.x)
            if offset <= 3.5:
                # Snap block perfectly flush without shaving
                placement_x = top_block.x
                self.perfect_streak += 1

                # Restore lost width if on a streak
                bonus_width = 8.0 if self.perfect_streak >= 2 else 0.0
                placed_width = min(float(self.base_width), top_block.width + bonus_width)

                self.score += 2  # Bonus score for perfect placement
                if self.perfect_streak >= 2:
                    self.perfect_message = f"PERFECT x{self.perfect_streak}! +WIDTH!"
                else:
                    self.perfect_message = "PERFECT! +2"
                self.perfect_message_timer = 40
            else:
                # Imperfect placement: trim overhang
                placement_x = left
                placed_width = max(8.0, overlap)
                self.perfect_streak = 0
                self.score += 1

                # Task 3: Falling off-cut debris animation
                if act.x < top_block.x:
                    # Off-cut on the left side
                    debris_x = act.x
                    debris_w = top_block.x - act.x
                    if debris_w > 1.0:
                        self.debris_list.append(Debris(debris_x, act.y, debris_w, self.block_height, act.color))
                elif act.x + act.width > top_block.x + top_block.width:
                    # Off-cut on the right side
                    debris_x = top_block.x + top_block.width
                    debris_w = (act.x + act.width) - (top_block.x + top_block.width)
                    if debris_w > 1.0:
                        self.debris_list.append(Debris(debris_x, act.y, debris_w, self.block_height, act.color))

            new_block = Block(placement_x, act.y, placed_width, self.block_height, act.color, speed=0)
            self.stack.append(new_block)

            # Camera scrolling adjustment
            if new_block.y < 200:
                shift_amount = self.block_height + 4
                for b in self.stack:
                    b.y += shift_amount
                for d in self.debris_list:
                    d.y += shift_amount

            self.spawn_active_block()
        else:
            # Tower collapses when placement completely misses
            self.game_over = True
            # Spawn falling debris for the missed active block
            self.debris_list.append(Debris(act.x, act.y, act.width, self.block_height, act.color))

    def handle_event(self, event):
        if self.game_over:
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_r or event.key == pygame.K_SPACE)) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.reset()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)

        # Update falling debris
        for d in self.debris_list:
            d.update()
        self.debris_list = [d for d in self.debris_list if not d.is_offscreen]

        # Update feedback message timer
        if self.perfect_message_timer > 0:
            self.perfect_message_timer -= 1

    def render(self, screen):
        # Task 4: Atmospheric Background Shifting
        bg_color = self.get_atmospheric_background()
        screen.fill(bg_color)

        # Draw stars when reaching higher atmospheric strata
        if len(self.stack) >= 12:
            star_alpha = min(255, (len(self.stack) - 10) * 15)
            for sx, sy, srad in self.stars:
                star_color = (star_alpha, star_alpha, star_alpha)
                pygame.draw.circle(screen, star_color, (sx, sy), srad)

        title_surf = self.font_title.render("Skyscraper Stack", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        score_surf = self.font_hud.render(f"Height: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))

        # Render falling debris
        for d in self.debris_list:
            d.render(screen)

        # Render tower stack
        for b in self.stack:
            b.render(screen)

        # Render active moving block
        if not self.game_over:
            self.active_block.render(screen)

        # Render perfect prompt bonus
        if self.perfect_message_timer > 0:
            color = (255, 235, 60) if "x" in self.perfect_message else (100, 255, 140)
            bonus_surf = self.font_bonus.render(self.perfect_message, True, color)
            screen.blit(bonus_surf, (self.width // 2 - bonus_surf.get_width() // 2, 90))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("TOWER COLLAPSED!", True, (240, 75, 75))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_hud.render(f"Final Height: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_hud.render("Press [Space] or [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
