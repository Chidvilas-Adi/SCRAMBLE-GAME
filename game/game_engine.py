import random
import pygame
from game.text_box import TextBox

ROUND_SECONDS = 20
HINT_PENALTY = 1
TIMEUP_PAUSE_MS = 2000
TILE = 50
GAP = 8


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = ["PYTHON", "PYGAME", "PLANET", "ROCKET", "GALAXY", "STREAM", "PUZZLE", "ALGORITHM"]
        self.secret_word = ""
        self.scrambled_word = ""

        self.score = 0
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        # input row: [textbox][SUBMIT][HINT]
        row_y = 300
        start_x = (width - 410) // 2
        self.input_box = TextBox(start_x, row_y, 200, 46)
        self.submit_btn = pygame.Rect(start_x + 210, row_y, 95, 46)
        self.hint_btn = pygame.Rect(start_x + 315, row_y, 95, 46)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_tile = pygame.font.SysFont(None, 42)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)

        self.next_round()

    # ---------- round / scramble ----------
    def scramble_string(self, word):
        letters = list(word)
        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)
            if shuffled != word or len(word) <= 1:
                return shuffled

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(self.secret_word)
        self.input_box.clear()
        self.rack = []                      # indices into scrambled_word, in rack order
        self.hints_used = 0
        self.round_start = pygame.time.get_ticks()
        self.timeup_until = None            # set when time runs out

    # ---------- tiles ----------
    def _tile_x0(self):
        n = len(self.scrambled_word)
        return (self.width - (n * TILE + (n - 1) * GAP)) // 2

    def pool_rect(self, i):
        return pygame.Rect(self._tile_x0() + i * (TILE + GAP), 135, TILE, TILE)

    def rack_rect(self, slot):
        return pygame.Rect(self._tile_x0() + slot * (TILE + GAP), 205, TILE, TILE)

    def _sync_text_from_rack(self):
        self.input_box.text = "".join(self.scrambled_word[i] for i in self.rack)

    def reset_tiles(self):
        self.rack = []

    def _handle_tile_click(self, pos):
        for i in range(len(self.scrambled_word)):
            if i not in self.rack and self.pool_rect(i).collidepoint(pos):
                self.rack.append(i)
                self._sync_text_from_rack()
                return True
        for slot, i in enumerate(self.rack):
            if self.rack_rect(slot).collidepoint(pos):
                self.rack.pop(slot)
                self._sync_text_from_rack()
                return True
        return False

    # ---------- hints ----------
    def use_hint(self):
        if self.hints_used >= len(self.secret_word) - 1:
            self.feedback_msg = "No more hints available!"
            self.feedback_color = (240, 170, 50)
            return
        self.hints_used += 1
        self.score -= HINT_PENALTY
        self.feedback_msg = f"Hint used (-{HINT_PENALTY} point)"
        self.feedback_color = (240, 170, 50)

    def hint_display(self):
        return " ".join(
            c if i < self.hints_used else "_" for i, c in enumerate(self.secret_word)
        )

    # ---------- timer ----------
    def time_left(self):
        elapsed = (pygame.time.get_ticks() - self.round_start) / 1000.0
        return max(0.0, ROUND_SECONDS - elapsed)

    def _in_timeup(self):
        return self.timeup_until is not None

    # ---------- guess ----------
    def submit_guess(self):
        guess = self.input_box.text.strip().upper()
        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # FIX: validate against the original word, not the scrambled one
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)
            self.next_round()
        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()
            self.reset_tiles()

    def handle_event(self, event):
        if self._in_timeup():
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_BACKSPACE and self.rack:
                self.rack.pop()
                self._sync_text_from_rack()
            else:
                before = self.input_box.text
                self.input_box.handle_event(event)
                if self.input_box.text != before:
                    self.reset_tiles()      # typed manually -> tiles back to pool
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()
            elif self.hint_btn.collidepoint(event.pos):
                self.use_hint()
            else:
                self._handle_tile_click(event.pos)
                self.input_box.handle_event(event)
        # keep typing active after any click
        self.input_box.active = True

    def update(self):
        now = pygame.time.get_ticks()
        if self._in_timeup():
            if now >= self.timeup_until:
                self.next_round()
            return
        if self.time_left() <= 0:
            self.feedback_msg = f"TIME'S UP! The word was {self.secret_word}"
            self.feedback_color = (240, 80, 80)
            self.timeup_until = now + TIMEUP_PAUSE_MS

    # ---------- drawing ----------
    def _draw_tile(self, screen, rect, letter, fill, border):
        pygame.draw.rect(screen, fill, rect, border_radius=8)
        pygame.draw.rect(screen, border, rect, width=2, border_radius=8)
        s = self.font_tile.render(letter, True, (20, 25, 35))
        screen.blit(s, (rect.centerx - s.get_width() // 2, rect.centery - s.get_height() // 2))

    def _draw_button(self, screen, rect, label, color):
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), rect, width=2, border_radius=6)
        t = self.font_btn.render(label, True, (255, 255, 255))
        screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))

    def render(self, screen):
        screen.fill((26, 30, 38))

        title_surf = self.font_title.render("Word Scramble Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_msg.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 65))

        # timer bar
        bar_w, bar_h = 400, 14
        bar_x, bar_y = (self.width - bar_w) // 2, 98
        left = 0.0 if self._in_timeup() else self.time_left()
        frac = left / ROUND_SECONDS
        color = (80, 230, 110) if frac > 0.5 else (240, 170, 50) if frac > 0.25 else (240, 80, 80)
        pygame.draw.rect(screen, (55, 60, 72), (bar_x, bar_y, bar_w, bar_h), border_radius=7)
        if frac > 0:
            pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_w * frac), bar_h), border_radius=7)
        secs = self.font_msg.render(f"{int(left) + (1 if left % 1 else 0)}s", True, (210, 215, 225))
        screen.blit(secs, (bar_x + bar_w + 12, bar_y - 3))

        # scrambled tiles (pool) and answer rack
        n = len(self.scrambled_word)
        for i, ch in enumerate(self.scrambled_word):
            r = self.pool_rect(i)
            if i in self.rack:
                pygame.draw.rect(screen, (45, 50, 62), r, width=2, border_radius=8)
            else:
                self._draw_tile(screen, r, ch, (100, 200, 255), (220, 240, 255))
        for slot in range(n):
            r = self.rack_rect(slot)
            if slot < len(self.rack):
                self._draw_tile(screen, r, self.scrambled_word[self.rack[slot]], (255, 220, 80), (255, 240, 170))
            else:
                pygame.draw.rect(screen, (80, 90, 105), r, width=2, border_radius=8)

        # revealed hint letters
        hint_surf = self.font_word.render(self.hint_display(), True, (255, 220, 80))
        screen.blit(hint_surf, (self.width // 2 - hint_surf.get_width() // 2, 259))

        self.input_box.render(screen)
        self._draw_button(screen, self.submit_btn, "SUBMIT", (50, 150, 85))
        self._draw_button(screen, self.hint_btn, "HINT", (60, 110, 200))

        feedback_surf = self.font_msg.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 365))
