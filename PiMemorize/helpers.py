import pygame as pg
import os

class Helpers:
    def __init__(self, screen, fonts, images):
        self.screen = screen
        self.fonts = fonts
        self.images = images

    def create_text(self, text, font_name, size, color='white'):
        return self.fonts[font_name][size].render(text, True, color)

    def create_text_and_rect(self, text, font_name, size, x, y, color='white'):
        """Creates text and a rectangle based on given parameters."""
        rendered_text = self.create_text(text, font_name, size, color)
        rect = rendered_text.get_rect(center=(x, y))
        return rendered_text, rect

    def create_button_and_rect(self, text, font_name, size, x, y, rect_width, rect_height, color='white'):
        """Creates the button text and its rectangle based on specified parameters."""
        button_text = self.fonts[font_name][size].render(text, True, color)
        button_rect = pg.Rect(x, y, rect_width, rect_height)

        # Creating text_rect with fonts corrections
        if font_name == 'calibri':
            y_correction = 5
        elif font_name == 'candara':
            y_correction = 8
        else:
            y_correction = 0

        text_rect = button_text.get_rect(center=(button_rect.centerx, button_rect.centery + y_correction))
        return button_text, button_rect, text_rect

    def create_counter_and_rect(self, text, font_name, size, reference_rect, offset_x=0, offset_y=0):
        """Creates the counter text and its rectangle based on the reference rectangle."""
        counter_text = self.create_text(text, font_name, size)
        counter_rect = counter_text.get_rect(
            center=(reference_rect.centerx + offset_x, reference_rect.bottom + reference_rect.height * 0.72 + offset_y)
        )
        return counter_text, counter_rect

    def create_image_rect(self, image_key, reference_rect, offset_x=0, offset_y=0):
        """Creates an image rectangle based on the image key and the reference rectangle."""
        return self.images[image_key].get_rect(
            center=(reference_rect.centerx + offset_x, reference_rect.bottom + reference_rect.height * 0.6 + offset_y)
        )

    def draw_button(self, button_rect, button_text, button_text_rect, color='white'):
        """Helper function to draw a button."""
        pg.draw.rect(self.screen, color, button_rect, 3)
        self.screen.blit(button_text, button_text_rect)

    def read_pi_digits(self):
        try:
            with open('pi_digits.txt', 'r') as file:
                return file.read().strip().replace('\n', '')
        except FileNotFoundError:
            return "Error: pi_digits.txt not found."

    def save_to_highscores(self, nick, digits, avg_thinking_time, total_time, mistakes_ratio, score, thinking_time_counter):
        """Save a new highscore to the file with two decimal places"""
        highscores_list = self.read_from_highscores()

        # Add a new result and sort the list descending by result.
        highscores_list.append((nick, digits, f"{avg_thinking_time:.2f}/{thinking_time_counter:.2f}",
                                f"{total_time:.2f}", mistakes_ratio, int(score)))
        highscores_list = sorted(highscores_list, key=lambda x: float(x[5]), reverse=True)[:10]

        # Save updated list to the file
        with open('highscores.txt', 'w') as file:
            for nick, digits, avg_thinking_time, total_time, mistakes_ratio, score in highscores_list:
                file.write(f"{nick},{digits},{avg_thinking_time},{total_time},{mistakes_ratio},{score}\n")

    def read_from_highscores(self):
        """Read highscores from the file and return them as a list of tuples (name, score)"""
        if not os.path.exists('highscores.txt'):
            return []  # Return an empty list if the file doesn't exist

        highscores_list = []
        try:
            with open('highscores.txt', 'r') as file:
                for line in file:
                    nick, digits, avg_thinking_time, total_time, mistakes_ratio, score = line.strip().split(',')
                    highscores_list.append((nick, digits, avg_thinking_time, total_time, mistakes_ratio, score))
        except FileNotFoundError:
            pass

        return highscores_list

    def show_confirmation_dialog(self, screen):
        """Wyświetla okno potwierdzenia z opcjami 'Tak' i 'Nie' z wykorzystaniem metod pomocniczych."""

        # Tworzenie powierzchni dialogowej
        dialog_surface = pg.Surface((400, 200))
        dialog_surface.fill((50, 50, 50))  # Tło dialogu
        dialog_rect = dialog_surface.get_rect(center=screen.get_rect().center)

        # Tworzenie tekstu pytania
        text, text_rect = self.create_text_and_rect(
            "Are you sure?", 'calibri', 35, dialog_rect.width // 2, dialog_rect.height // 4
        )

        # Tworzenie przycisków "Yes" i "No" w lokalnym układzie współrzędnych dialog_surface
        yes_text, yes_button_rect, yes_text_rect = self.create_button_and_rect(
            "Yes", 'calibri', 35, dialog_rect.width // 4 - 50, dialog_rect.height // 3 + 50, 100, 50, 'white'
        )
        no_text, no_button_rect, no_text_rect = self.create_button_and_rect(
            "No", 'calibri', 35, (dialog_rect.width * 3) // 4 - 50, dialog_rect.height // 3 + 50, 100, 50, 'white'
        )

        pg.event.clear()  # Czyści kolejkę zdarzeń, aby uniknąć konfliktów

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False  # Wyjście z gry
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Dopasowanie pozycji myszki do globalnego układu współrzędnych
                    mouse_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                    if yes_button_rect.collidepoint(mouse_pos):  # Kliknięto "Yes"
                        return True
                    if no_button_rect.collidepoint(mouse_pos):  # Kliknięto "No"
                        return False

            # Rysowanie tła dialogu
            dialog_surface.fill((50, 50, 50))

            # Rysowanie tekstu pytania
            dialog_surface.blit(text, text_rect)

            # Rysowanie przycisków "Yes" i "No"
            pg.draw.rect(dialog_surface, 'green', yes_button_rect)
            pg.draw.rect(dialog_surface, 'red', no_button_rect)
            dialog_surface.blit(yes_text, yes_text_rect)
            dialog_surface.blit(no_text, no_text_rect)

            # Wyświetlanie dialogu na ekranie
            screen.blit(dialog_surface, dialog_rect.topleft)
            pg.display.flip()  # Aktualizacja ekranu



