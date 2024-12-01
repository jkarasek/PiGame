
"""
Helper functions and utility methods for PiGame.

This module provides a set of helper functions and utility classes to support
various functionalities within the PiGame application.
"""

import pygame as pg
import os


class Helpers:
    """
        A class used to provide utility functions and helpers for the PiGame application.
        This class includes methods for rendering text, creating UI elements, managing files,
        and handling common tasks shared across different game screens.

        Attributes
        ----------
        screen : pygame.Surface
            The primary display surface to render elements.
        fonts : dict
            A dictionary of preloaded fonts categorized by their name and size.
        images : dict
            A dictionary of preloaded images used in the game.

        Methods
        -------
        create_text(text, font_name, font_size, color='white')
            Renders text with the specified font, size, and color.
        create_text_and_rect(text, font_name, font_size, center_x, center_y, color='white')
            Renders text and calculates its rectangular position for centering.
        create_button_and_rect(text, font_name, font_size, x, y, width, height, color='black')
            Creates a button with text and returns the text, button rectangle, and text rectangle.
        create_counter_and_rect(text, font_name, font_size, reference_rect)
            Creates a counter and aligns it with a reference rectangle.
        create_image_rect(image_key, reference_rect, offset_x=0, offset_y=0)
            Creates a rectangle for an image relative to a reference rectangle with offsets.
        draw_button(rect, text, text_rect, color='black')
            Draws a button and its text on the screen.
        show_confirmation_dialog(screen)
            Displays a confirmation dialog and waits for the user's response.
        read_pi_digits()
            Reads the digits of Pi from a file and returns them as a single string.
        save_to_highscores(nickname, digits, thinking_time, total_time, mistakes_ratio, score, time_for_hint)
            Saves a player's performance in the highscores file.
        read_from_highscores()
            Reads the highscores from the file and returns them as a list of entries.

    """

    def __init__(self, screen, fonts, images):
        self.screen = screen
        self.fonts = fonts
        self.images = images
        self.base_path = os.path.dirname(__file__)

    def create_text(self, text, font_name, size, color='white'):
        return self.fonts[font_name][size].render(text, True, color)

    def create_text_and_rect(self, text, font_name, size, x, y, color='white'):
        rendered_text = self.create_text(text, font_name, size, color)
        rect = rendered_text.get_rect(center=(x, y))
        return rendered_text, rect

    def create_button_and_rect(self, text, font_name, size, x, y, rect_width, rect_height, color='white'):
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
        counter_text = self.create_text(text, font_name, size)
        counter_rect = counter_text.get_rect(
            center=(reference_rect.centerx + offset_x, reference_rect.bottom + reference_rect.height * 0.72 + offset_y)
        )
        return counter_text, counter_rect

    def create_image_rect(self, image_key, reference_rect, offset_x=0, offset_y=0):
        return self.images[image_key].get_rect(
            center=(reference_rect.centerx + offset_x, reference_rect.bottom + reference_rect.height * 0.6 + offset_y)
        )

    def draw_button(self, button_rect, button_text, button_text_rect, color='white'):
        pg.draw.rect(self.screen, color, button_rect, 3)
        self.screen.blit(button_text, button_text_rect)

    def read_pi_digits(self):
        file_path = os.path.join(self.base_path, 'pi_digits.txt')
        try:
            with open(file_path, 'r') as file:
                return file.read().strip().replace('\n', '')
        except FileNotFoundError:
            return "Error: pi_digits.txt not found."

    def save_to_highscores(self, nick, digits, avg_thinking_time, total_time, mistakes_ratio, score,
                           thinking_time_counter):
        file_path = os.path.join(self.base_path, 'highscores.txt')
        highscores_list = self.read_from_highscores()

        # Add a new result and sort the list descending by result.
        highscores_list.append((nick, digits, f"{avg_thinking_time:.2f}/{thinking_time_counter:.2f}",
                                f"{total_time:.2f}", mistakes_ratio, int(score)))
        highscores_list = sorted(highscores_list, key=lambda x: float(x[5]), reverse=True)[:10]

        # Save updated list to the file
        with open(file_path, 'w') as file:
            for nick, digits, avg_thinking_time, total_time, mistakes_ratio, score in highscores_list:
                file.write(f"{nick},{digits},{avg_thinking_time},{total_time},{mistakes_ratio},{score}\n")

    def read_from_highscores(self):
        file_path = os.path.join(self.base_path, 'highscores.txt')
        if not os.path.exists(file_path):
            return []  # Return an empty list if the file doesn't exist

        highscores_list = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    nick, digits, avg_thinking_time, total_time, mistakes_ratio, score = line.strip().split(',')
                    highscores_list.append((nick, digits, avg_thinking_time, total_time, mistakes_ratio, score))
        except FileNotFoundError:
            pass

        return highscores_list

    def show_confirmation_dialog(self, screen):
        # Creation a pop-up window surface
        dialog_surface = pg.Surface((400, 200))
        dialog_surface.fill((50, 50, 50))  # Dialog background
        dialog_rect = dialog_surface.get_rect(center=screen.get_rect().center)

        # Creation a question text
        text, text_rect = self.create_text_and_rect(
            "Are you sure?", 'calibri', 35, dialog_rect.width // 2, dialog_rect.height // 4
        )

        # Creation of ‘Yes’ and ‘No’ buttons in the local coordinate system dialog_surface
        yes_text, yes_button_rect, yes_text_rect = self.create_button_and_rect(
            "Yes", 'calibri', 35, dialog_rect.width // 4 - 50, dialog_rect.height // 3 + 50, 100, 50, 'white'
        )
        no_text, no_button_rect, no_text_rect = self.create_button_and_rect(
            "No", 'calibri', 35, (dialog_rect.width * 3) // 4 - 50, dialog_rect.height // 3 + 50, 100, 50, 'white'
        )

        pg.event.clear()  # Clears the event queue to avoid conflicts

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False  # Quit
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Adjust mouse position to global coordinate system
                    mouse_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                    if yes_button_rect.collidepoint(mouse_pos):  # "Yes" answer
                        return True
                    if no_button_rect.collidepoint(mouse_pos):  # "No" answer
                        return False

            # Drawing the background of the dialog
            dialog_surface.fill((50, 50, 50))

            # Drawing the text of the question
            dialog_surface.blit(text, text_rect)

            # Drawing the ‘Yes’ and ‘No’ buttons
            pg.draw.rect(dialog_surface, 'green', yes_button_rect)
            pg.draw.rect(dialog_surface, 'red', no_button_rect)
            dialog_surface.blit(yes_text, yes_text_rect)
            dialog_surface.blit(no_text, no_text_rect)

            # Displaying the pop-up on the screen
            screen.blit(dialog_surface, dialog_rect.topleft)
            pg.display.flip()  # Screen update
