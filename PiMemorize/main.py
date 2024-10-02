import pygame as pg
import time
from pygame import font


class PiGame:
    def __init__(self):
        pg.init()  # Pygame initialization

        # Fullscreen mode (default)
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # Reading screen sizes
        screen_info = pg.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h

        # Clock
        self.clock = pg.time.Clock()

        # Fonts
        font.init()
        self.candara_96_font = font.SysFont('candara', size=96)
        self.candara_72_font = font.SysFont('candara', size=72)
        self.candara_60_font = font.SysFont('candara', size=60)
        self.candara_50_font = font.SysFont('candara', size=50)
        self.calibri_72_font = font.SysFont('calibri', size=72)
        self.calibri_60_font = font.SysFont('calibri', size=60)
        self.calibri_55_font = font.SysFont('calibri', size=55)
        self.calibri_40_font = font.SysFont('calibri', size=40)
        self.cambria_35_font = font.SysFont('cambria', size=35)

        self.main_values()

    def main_values(self):
        # Learning screen counters
        self.digits_in_columns_counter = 5

        self.page_change_multipliers = [1, 2, 5, 10, 100]
        self.page_change_multiplier_counter = 1

        self.page_number_counter = 1

        self.digits_on_page_counter_bottom = 1
        self.digits_on_page_counter_top = 1
        self.digits_on_page_counter = 0

        # Screens settings counters ( training and challenge )
        self.digit_multipliers = [1, 10, 50, 100, 1000]
        self.digit_multiplier_counter = 1
        self.start_digit_counter = 1

        self.thinking_time_counter = 5
        self.mistakes_allowed_counter = 3

        # Training screen
        self.digits_display_offset = 30
        self.switch_position = 1
        self.keys_layout = 1
        self.digit_counter = 1
        self.hint_counter = 4

        # Goal counters
        self.goal_digit_counter = 25

        self.goal_digit_multipliers = [25, 50, 100, 250, 500]
        self.goal_digit_multiplier_counter = 25

        self.game_over = False

    # Main screen initialization
    def main_screen(self):
        main_running = True
        self.main_screen_objects()

        while main_running:
            self.screen.fill('black')

            # Logo displayed
            self.screen.blit(self.logo_image, self.game_logo)

            # Drawing buttons
            pg.draw.rect(self.screen, 'white', self.learning_button_rect, 3)
            pg.draw.rect(self.screen, 'white', self.training_button_rect, 3)
            pg.draw.rect(self.screen, 'white', self.challenge_button_rect, 3)
            pg.draw.rect(self.screen, 'white', self.quit_button_rect, 3)

            self.screen.blit(self.learning_button_text, self.learning_button_text_rect)
            self.screen.blit(self.training_button_text, self.training_button_text_rect)
            self.screen.blit(self.challenge_button_text, self.challenge_button_text_rect)
            self.screen.blit(self.quit_button_text, self.quit_button_text_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    main_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.quit_button_rect.collidepoint(event.pos):
                        exit()
                    if self.learning_button_rect.collidepoint(event.pos):
                        self.learning_screen()
                    if self.training_button_rect.collidepoint(event.pos):
                        self.training_screen_settings()
                    if self.challenge_button_rect.collidepoint(event.pos):
                        self.challenge_screen_settings()

            pg.display.flip()
            self.clock.tick(60)  # Screen refresh frequency

        pg.quit()  # Close pygame after loop ends

    def read_pi_digits(self):
        try:
            with open('pi_digits.txt', 'r') as file:
                pi_digits = file.read().strip().replace('\n', '')
                return pi_digits
        except FileNotFoundError:
            return "Error: pi_digits.txt not found."

    def draw_learning_pi_digits(self):
        # Loading digits (list)
        pi_digits = self.read_pi_digits()

        # Start (main) value of bottom digits counter
        self.digits_on_page_counter_bottom = 1

        # Pages logic
        if self.page_number_counter == 2:
            pi_digits = pi_digits[self.digits_on_page_counter:]
            self.digits_on_page_counter_bottom = self.digits_on_page_counter
        if self.page_number_counter > 2:
            pi_digits = pi_digits[(self.page_number_counter - 1) * self.digits_on_page_counter:]
            self.digits_on_page_counter_bottom = (self.page_number_counter - 1) * self.digits_on_page_counter

        x = self.x  # start X position of digits rectangle
        y = 35  # start Y position of digits rectangle

        # Drawing loop
        for i, digit in enumerate(pi_digits):

            # Text rendering
            text = self.calibri_40_font.render(str(pi_digits[:self.digits_in_columns_counter]), True, 'white')
            pi_digits = pi_digits[self.digits_in_columns_counter:]

            # Creating a rectangle for text
            rect = text.get_rect(center=(self.digits_rect.left + x, self.screen_height * 0.1 + y))

            # Checking if the rectangle extends beyond right frame edge
            if (rect.right + 15) > self.digits_rect.right:
                x = self.x  # Reset X position
                y += 50  # Start printing from a new line
                rect = text.get_rect(
                    center=(self.digits_rect.left + x, self.screen_height * 0.1 + y))  # Rect position update

            # Checking if the rectangle extends beyond bottom frame edge
            if rect.bottom > self.digits_rect.bottom:
                # Digits in page counter update
                self.digits_on_page_counter = i * self.digits_in_columns_counter
                self.digits_on_page_counter_top = self.page_number_counter * self.digits_on_page_counter
                if self.digits_on_page_counter_top > 1000000:
                    self.digits_on_page_counter_top = 1000000

                # Digits in page counter drawing
                self.learning_screen_objects()
                self.screen.blit(self.digits_on_page_counter_text, self.digits_on_page_counter_rect)
                break

            # Space between columns for next digits
            x += ((((self.digits_rect.width - 2 * self.x) - (rect.width * self.columns)) / self.columns)
                  + rect.width)

            # Text drawing
            self.screen.blit(text, rect)

    def images_initialization(self):

        minus_image = pg.image.load('images/minus.png')
        plus_image = pg.image.load('images/plus.png')
        switch_on_image = pg.image.load('images/switch_on.png')
        switch_off_image = pg.image.load('images/switch_off.png')
        switch_neutral_image = pg.image.load('images/switch_neutral.png')
        heart_image = pg.image.load('images/heart.png')
        logo_image = pg.image.load('images/logo.png')

        # Scaling images
        self.logo_image = pg.transform.scale(logo_image, (self.screen_width * 0.23, self.screen_height * 0.16))

        self.minus_image = pg.transform.scale(minus_image, (self.screen_width * 0.035, self.screen_width * 0.035))
        self.plus_image = pg.transform.scale(plus_image, (self.screen_width * 0.035, self.screen_width * 0.035))

        self.t_s_minus_image = pg.transform.scale(minus_image, (self.screen_width * 0.06, self.screen_width * 0.06))
        self.t_s_plus_image = pg.transform.scale(plus_image, (self.screen_width * 0.06, self.screen_width * 0.06))

        self.switch_on_image = pg.transform.scale(switch_on_image, (self.screen_width * 0.06, self.screen_width * 0.03))
        self.switch_off_image = pg.transform.scale(switch_off_image,
                                                   (self.screen_width * 0.06, self.screen_width * 0.03))
        self.switch_neutral_image = pg.transform.scale(switch_neutral_image,
                                                       (self.screen_width * 0.06, self.screen_width * 0.03))

        self.heart_image = pg.transform.scale(heart_image, (self.screen_width * 0.038, self.screen_width * 0.034))

    def keys_initialization(self):
        # Keys layout options
        if self.keys_layout == 0:
            self.square_1_y_pos = self.switch_keys_layout_rect.y
            self.square_7_y_pos = self.back_button_rect.y
        elif self.keys_layout == 1:
            self.square_1_y_pos = self.back_button_rect.y
            self.square_7_y_pos = self.switch_keys_layout_rect.y

        # Squares
        for i in range(10):
            # Squares texts
            setattr(self, f'square_{i}_text', self.calibri_72_font.render(str(i), True, 'white'))

        # Squares rects
        self.square_0_rect = pg.Rect(self.guessing_rect.centerx - 0.06 * self.screen_height,  # Position X
                                     self.back_button_rect.bottom + self.back_button_rect.height * 0.4,
                                     # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_1_rect = pg.Rect(
            self.square_0_rect.left - self.square_0_rect.width - self.guessing_rect.height * 0.5,  # Position X
            self.square_1_y_pos,  # Position Y
            self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_2_rect = pg.Rect(self.square_0_rect.x,  # Position X
                                     self.square_1_rect.y,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_3_rect = pg.Rect(
            self.square_0_rect.left + self.square_0_rect.width + self.guessing_rect.height * 0.5,  # Position X
            self.square_1_rect.y,  # Position Y
            self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_4_rect = pg.Rect(self.square_1_rect.x,  # Position X
                                     (self.square_1_y_pos + self.square_7_y_pos) * 0.5,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_5_rect = pg.Rect(self.square_2_rect.x,  # Position X
                                     self.square_4_rect.y,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_6_rect = pg.Rect(self.square_3_rect.x,  # Position X
                                     self.square_4_rect.y,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_7_rect = pg.Rect(self.square_1_rect.x,  # Position X
                                     self.square_7_y_pos,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_8_rect = pg.Rect(self.square_2_rect.x,  # Position X
                                     self.square_7_rect.y,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        self.square_9_rect = pg.Rect(self.square_3_rect.x,  # Position X
                                     self.square_7_rect.y,  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)  # Size

        # Text rects for squares
        for i in range(10):
            square_text = getattr(self, f'square_{i}_text')
            square_rect = getattr(self, f'square_{i}_rect')
            setattr(self, f'square_{i}_text_rect', square_text.get_rect(center=square_rect.center))

    def main_screen_objects(self):
        self.images_initialization()

        # Text displayed
        self.learning_button_text = self.cambria_35_font.render("Learning", True, 'white')
        self.training_button_text = self.cambria_35_font.render("Training", True, 'white')
        self.challenge_button_text = self.cambria_35_font.render("Challenge", True, 'white')
        self.quit_button_text = self.cambria_35_font.render("Quit", True, 'white')

        # Rectangles (buttons)
        self.learning_button_rect = pg.Rect(self.screen_width * 0.42, self.screen_height * 0.35,
                                            self.screen_width * 0.16, self.screen_height * 0.08)
        self.training_button_rect = pg.Rect(self.learning_button_rect.left, self.learning_button_rect.bottom + 20,
                                            self.screen_width * 0.16, self.screen_height * 0.08)
        self.challenge_button_rect = pg.Rect(self.learning_button_rect.left, self.training_button_rect.bottom + 20,
                                             self.screen_width * 0.16, self.screen_height * 0.08)
        self.quit_button_rect = pg.Rect(self.learning_button_rect.left, self.challenge_button_rect.bottom + 120,
                                        self.screen_width * 0.16, self.screen_height * 0.08)

        # Text rects
        self.learning_button_text_rect = self.learning_button_text.get_rect(center=self.learning_button_rect.center)
        self.training_button_text_rect = self.training_button_text.get_rect(center=self.training_button_rect.center)
        self.challenge_button_text_rect = self.challenge_button_text.get_rect(center=self.challenge_button_rect.center)
        self.quit_button_text_rect = self.quit_button_text.get_rect(center=self.quit_button_rect.center)

        # Images rectangles
        self.game_logo = self.logo_image.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.20)
        )

    def learning_screen_objects(self):
        self.images_initialization()

        # Texts
        self.digits_in_columns_text = self.calibri_40_font.render("Digits in columns:", True, 'white')
        self.page_number_text = self.calibri_40_font.render("Page number:", True, 'white')
        self.page_change_multiplier_text = self.calibri_40_font.render("Page change multiplier:", True, 'white')
        self.digits_on_page_text = self.calibri_40_font.render("Digits on page:", True, 'white')

        # Rectangles
        self.digits_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,
                                   self.screen_width * 0.6, self.screen_height * 0.8)
        self.digits_in_columns_rect = self.digits_in_columns_text.get_rect(
            center=(self.digits_rect.right + 0.5 * (self.screen_width - self.digits_rect.right),
                    self.digits_rect.top + 25)
        )
        self.page_number_rect = self.page_number_text.get_rect(
            center=(self.digits_in_columns_rect.centerx,
                    self.digits_in_columns_rect.centery + self.digits_in_columns_rect.height * 4)
        )
        self.page_change_multiplier_rect = self.page_change_multiplier_text.get_rect(
            center=(self.digits_in_columns_rect.centerx,
                    self.page_number_rect.centery + self.digits_in_columns_rect.height * 4)
        )
        self.digits_on_page_rect = self.digits_on_page_text.get_rect(
            center=(self.digits_in_columns_rect.centerx,
                    self.page_change_multiplier_rect.centery + 5 * self.digits_in_columns_rect.height)
        )

        # Buttons and counters
        self.l_s_back_button_text = self.cambria_35_font.render("Back", True, 'white')
        self.l_s_back_button_rect = pg.Rect(
            self.digits_rect.right + 0.5 * (self.screen_width - self.digits_rect.right) - self.screen_width * 0.08,
            self.digits_rect.bottom - self.screen_height * 0.08,
            self.screen_width * 0.16, self.screen_height * 0.08)
        self.l_s_back_button_text_rect = self.l_s_back_button_text.get_rect(center=self.l_s_back_button_rect.center)

        self.digits_in_columns_counter_text = self.calibri_40_font.render(
            str(self.digits_in_columns_counter), True, 'white')
        self.page_number_counter_text = self.calibri_40_font.render(
            str(self.page_number_counter), True, 'white')
        self.page_change_multiplier_counter_text = self.calibri_40_font.render(
            "x" + str(self.page_change_multiplier_counter), True, 'white')
        self.digits_on_page_counter_text = self.calibri_40_font.render(
            str(self.digits_on_page_counter_bottom) + " - " + str(self.digits_on_page_counter_top), True, 'white')

        # Counters rects
        self.digits_in_columns_counter_rect = self.digits_in_columns_counter_text.get_rect(
            center=(self.digits_in_columns_rect.centerx,
                    self.digits_in_columns_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.page_number_counter_rect = self.page_number_counter_text.get_rect(
            center=(self.page_number_rect.centerx, self.page_number_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.page_change_multiplier_counter_rect = self.page_change_multiplier_counter_text.get_rect(
            center=(self.page_change_multiplier_rect.centerx,
                    self.page_change_multiplier_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.digits_on_page_counter_rect = self.digits_on_page_counter_text.get_rect(
            center=(self.digits_on_page_rect.centerx,
                    self.digits_on_page_rect.bottom + self.digits_in_columns_rect.height)
        )

        # Images rectangles
        self.digits_in_columns_minus = self.minus_image.get_rect(
            center=(self.digits_in_columns_rect.centerx - 80,
                    self.digits_in_columns_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.digits_in_columns_plus = self.plus_image.get_rect(
            center=(self.digits_in_columns_rect.centerx + 80, self.digits_in_columns_minus.centery)
        )

        self.page_number_minus = self.minus_image.get_rect(
            center=(self.digits_in_columns_minus.centerx, self.page_number_rect.bottom + self.page_number_rect.height)
        )
        self.page_number_plus = self.plus_image.get_rect(
            center=(self.digits_in_columns_plus.centerx, self.page_number_minus.centery)
        )

        self.page_change_multiplier_minus = self.minus_image.get_rect(
            center=(self.page_number_minus.centerx,
                    self.page_change_multiplier_rect.bottom + self.page_change_multiplier_rect.height)
        )
        self.page_change_multiplier_plus = self.plus_image.get_rect(
            center=(self.page_number_plus.centerx, self.page_change_multiplier_minus.centery)
        )

    def training_screen_settings_objects(self):
        self.images_initialization()

        # Texts
        self.training_mode_title_text = self.candara_72_font.render("Training mode", True, 'white')
        self.choose_start_point_text = self.candara_60_font.render("Choose a start point", True, 'white')
        self.start_digit_text = self.calibri_40_font.render("Digit:", True, 'white')
        self.digit_multiplier_text = self.calibri_40_font.render("Multiplier:", True, 'white')

        # Rectangles
        self.training_mode_title_rect = self.training_mode_title_text.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.2))
        self.choose_start_point_rect = self.choose_start_point_text.get_rect(
            center=(self.screen_width * 0.5,
                    self.training_mode_title_rect.bottom + self.training_mode_title_rect.height * 2)
        )
        self.start_digit_rect = self.start_digit_text.get_rect(
            center=(self.training_mode_title_rect.left,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )
        self.digit_multiplier_rect = self.digit_multiplier_text.get_rect(
            center=(self.training_mode_title_rect.right,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )

        # Buttons and counters
        self.start_button_text = self.candara_60_font.render("Start", True, 'white')
        self.start_button_rect = pg.Rect(
            self.training_mode_title_rect.centerx - self.screen_width * 0.08,
            self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 4,
            self.screen_width * 0.16, self.screen_height * 0.08  # Size
        )
        self.start_button_text_rect = self.start_button_text.get_rect(
            center=self.start_button_rect.center
        )

        self.back_button_text = self.candara_60_font.render("Back", True, 'white')
        self.back_button_rect = pg.Rect(
            self.start_button_rect.left,
            self.start_button_rect.bottom + 20,
            self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.back_button_text_rect = self.back_button_text.get_rect(
            center=self.back_button_rect.center
        )

        self.start_digit_counter_text = self.candara_50_font.render(str(self.start_digit_counter), True, 'white')
        self.start_digit_counter_rect = self.start_digit_counter_text.get_rect(
            center=(self.start_digit_rect.centerx,
                    self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

        self.digit_multiplier_counter_text = self.candara_50_font.render(
            "x" + str(self.digit_multiplier_counter), True, 'white')
        self.digit_multiplier_counter_rect = self.digit_multiplier_counter_text.get_rect(
            center=(self.digit_multiplier_rect.centerx,
                    self.digit_multiplier_rect.bottom + self.digit_multiplier_rect.height)
        )

        # Images rectangles
        self.start_digit_plus = self.plus_image.get_rect(
            center=(self.start_digit_rect.centerx + 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.start_digit_minus = self.minus_image.get_rect(
            center=(self.start_digit_rect.centerx - 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_plus = self.plus_image.get_rect(
            center=(
                self.digit_multiplier_rect.centerx + 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_minus = self.minus_image.get_rect(
            center=(
                self.digit_multiplier_rect.centerx - 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

    def training_screen_objects(self):
        self.images_initialization()

        # Texts
        self.switch_keys_layout_text = self.calibri_40_font.render("Switch the keys layout", True, 'white')
        if self.switch_position == 0:
            self.hint_text = self.calibri_40_font.render("Hint after: " + str(self.hint_counter) + " seconds", True,
                                                         (59, 59, 59))
        elif self.switch_position == 1:
            self.hint_text = self.calibri_40_font.render("Hint after: " + str(self.hint_counter) + " seconds", True,
                                                         'white')
        self.your_time_text = self.candara_72_font.render("Your time:", True, 'white')

        # Rectangles
        self.guessing_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,  # Position
                                     self.screen_width * 0.88, self.screen_height * 0.12)  # Size

        self.switch_keys_layout_rect = pg.Rect(self.guessing_rect.left,
                                               self.guessing_rect.bottom + self.guessing_rect.height,
                                               self.screen_width * 0.24, self.screen_height * 0.12)

        self.hint_rect = pg.Rect(self.guessing_rect.left,
                                 self.switch_keys_layout_rect.bottom + self.switch_keys_layout_rect.height * 0.4,
                                 self.screen_width * 0.24, self.screen_height * 0.12)

        self.switch_keys_layout_text_rect = self.switch_keys_layout_text.get_rect(
            center=self.switch_keys_layout_rect.center)
        self.hint_text_rect = self.hint_text.get_rect(center=self.hint_rect.center)

        # Buttons and counters
        self.back_button_text = self.back_button_text
        self.back_button_rect = pg.Rect(self.guessing_rect.right - self.screen_width * 0.24,  # Position X
                                        self.hint_rect.bottom + self.hint_rect.height * 0.4,  # Position Y
                                        self.screen_width * 0.24, self.screen_height * 0.12)  # Size

        self.back_button_text_rect = self.back_button_text.get_rect(center=self.back_button_rect.center)

        self.your_time_rect = self.your_time_text.get_rect(
            center=(self.back_button_rect.centerx, self.switch_keys_layout_rect.centery)
        )

        # Keyboard initialization method
        self.keys_initialization()

        # Images rectangles
        self.hint_minus = self.t_s_minus_image.get_rect(
            center=(self.hint_rect.centerx - (self.hint_rect.width * 0.5) + self.screen_width * 0.03,
                    self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.hint_plus = self.t_s_plus_image.get_rect(
            center=(self.hint_rect.centerx, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_on = self.switch_on_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03,
                    self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_off = self.switch_off_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03,
                    self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_neutral = self.switch_neutral_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03,
                    self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )

    def challenge_screen_settings_objects(self):
        self.images_initialization()

        # Texts
        self.challenge_mode_title_text = self.candara_72_font.render("Challenge mode", True, 'white')
        self.choose_start_point_text = self.candara_60_font.render("Choose a start point", True, 'white')
        self.set_thinking_time_text = self.candara_60_font.render("Set thinking time [s]", True, 'white')
        self.set_ch_goal_text = self.candara_60_font.render("Set challenge goal", True, 'white')
        self.mistakes_allowed_text = self.candara_60_font.render("Mistakes allowed", True, 'white')
        self.start_digit_text = self.calibri_40_font.render("Digit:", True, 'white')
        self.digit_multiplier_text = self.calibri_40_font.render("Multiplier:", True, 'white')

        # Rectangles
        self.challenge_mode_title_rect = self.challenge_mode_title_text.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.15)
        )
        self.choose_start_point_rect = self.choose_start_point_text.get_rect(
            center=(self.screen_width * 0.25,
                    self.challenge_mode_title_rect.bottom + self.challenge_mode_title_rect.height)
        )
        self.set_ch_goal_rect = self.set_ch_goal_text.get_rect(
            center=(self.screen_width * 0.75,
                    self.choose_start_point_rect.centery)
        )
        self.set_thinking_time_rect = self.set_thinking_time_text.get_rect(
            center=(self.choose_start_point_rect.centerx,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 4.5)
        )
        self.mistakes_allowed_rect = self.mistakes_allowed_text.get_rect(
            center=(self.set_ch_goal_rect.centerx,
                    self.set_ch_goal_rect.bottom + self.set_ch_goal_rect.height * 4.5)
        )
        self.start_digit_rect = self.start_digit_text.get_rect(
            center=(self.choose_start_point_rect.left + 40,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )
        self.digit_multiplier_rect = self.digit_multiplier_text.get_rect(
            center=(self.choose_start_point_rect.right - 40,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )
        self.goal_digit_rect = self.start_digit_text.get_rect(
            center=(self.set_ch_goal_rect.centerx - 0.5 * (self.choose_start_point_rect.width - 80),
                    self.set_ch_goal_rect.bottom + self.set_ch_goal_rect.height * 0.5)
        )
        self.goal_digit_multiplier_rect = self.digit_multiplier_text.get_rect(
            center=(self.set_ch_goal_rect.centerx + 0.5 * (self.choose_start_point_rect.width - 80),
                    self.set_ch_goal_rect.bottom + self.set_ch_goal_rect.height * 0.5)
        )

        # Buttons and counters
        # Start button
        self.start_button_text = self.candara_60_font.render("Start", True, 'white')
        self.start_button_rect = pg.Rect(
            self.challenge_mode_title_rect.centerx - self.screen_width * 0.08,
            self.set_thinking_time_rect.bottom + 0.4 * (self.screen_height - self.set_thinking_time_rect.bottom),
            self.screen_width * 0.16, self.screen_height * 0.08  # Size
        )
        self.start_button_text_rect = self.start_button_text.get_rect(
            center=self.start_button_rect.center
        )

        # Back button
        self.back_button_text = self.candara_60_font.render("Back", True, 'white')
        self.back_button_rect = pg.Rect(
            self.start_button_rect.left,
            self.start_button_rect.bottom + 20,
            self.screen_width * 0.16, self.screen_height * 0.08
        )
        self.back_button_text_rect = self.back_button_text.get_rect(
            center=self.back_button_rect.center
        )

        # Start point counter
        self.start_digit_counter_text = self.candara_50_font.render(str(self.start_digit_counter), True, 'white')
        self.start_digit_counter_rect = self.start_digit_counter_text.get_rect(
            center=(self.start_digit_rect.centerx,
                    self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

        # Start point multiplier counter
        self.digit_multiplier_counter_text = self.candara_50_font.render(
            "x" + str(self.digit_multiplier_counter), True, 'white')
        self.digit_multiplier_counter_rect = self.digit_multiplier_counter_text.get_rect(
            center=(self.digit_multiplier_rect.centerx,
                    self.digit_multiplier_rect.bottom + self.digit_multiplier_rect.height)
        )

        # Goal digit counter
        self.goal_digit_counter_text = self.candara_50_font.render(
            str(self.goal_digit_counter), True, 'white')
        self.goal_digit_counter_rect = self.goal_digit_counter_text.get_rect(
            center=(self.goal_digit_rect.centerx,
                    self.goal_digit_rect.bottom + self.goal_digit_rect.height)
        )

        # Goal digit multiplier counter
        self.goal_digit_multiplier_counter_text = self.candara_50_font.render(
            "x" + str(self.goal_digit_multiplier_counter), True, 'white')
        self.goal_digit_multiplier_counter_rect = self.goal_digit_multiplier_counter_text.get_rect(
            center=(self.goal_digit_multiplier_rect.centerx,
                    self.goal_digit_multiplier_rect.bottom + self.goal_digit_multiplier_rect.height)
        )

        # Thinking time counter
        self.thinking_time_counter_text = self.candara_50_font.render(
            str(self.thinking_time_counter), True, 'white')
        self.thinking_time_counter_rect = self.thinking_time_counter_text.get_rect(
            center=(self.set_thinking_time_rect.centerx,
                    self.set_thinking_time_rect.bottom + self.set_thinking_time_rect.height)
        )

        # Mistakes allowed counter
        self.mistakes_allowed_counter_text = self.candara_50_font.render(
            str(self.mistakes_allowed_counter), True, 'white')
        self.mistakes_allowed_counter_rect = self.mistakes_allowed_counter_text.get_rect(
            center=(self.mistakes_allowed_rect.centerx,
                    self.mistakes_allowed_rect.bottom + self.mistakes_allowed_rect.height)
        )

        # Image rectangles
        # Start point + and -
        self.start_digit_plus = self.plus_image.get_rect(
            center=(self.start_digit_rect.centerx + 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.start_digit_minus = self.minus_image.get_rect(
            center=(self.start_digit_rect.centerx - 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

        # Start point multiplier + and -
        self.digit_multiplier_plus = self.plus_image.get_rect(
            center=(self.digit_multiplier_rect.centerx + 95,
                    self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_minus = self.minus_image.get_rect(
            center=(self.digit_multiplier_rect.centerx - 95,
                    self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

        # Goal digit + and -
        self.goal_digit_plus = self.plus_image.get_rect(
            center=(self.goal_digit_rect.centerx + 95, self.goal_digit_rect.bottom + self.goal_digit_rect.height)
        )
        self.goal_digit_minus = self.minus_image.get_rect(
            center=(self.goal_digit_rect.centerx - 95, self.goal_digit_rect.bottom + self.goal_digit_rect.height)
        )

        # Goal digit counter + and -
        self.goal_digit_multiplier_plus = self.plus_image.get_rect(
            center=(self.goal_digit_multiplier_rect.centerx + 95,
                    self.goal_digit_multiplier_rect.bottom + self.goal_digit_multiplier_rect.height)
        )
        self.goal_digit_multiplier_minus = self.minus_image.get_rect(
            center=(self.goal_digit_multiplier_rect.centerx - 95,
                    self.goal_digit_multiplier_rect.bottom + self.goal_digit_multiplier_rect.height)
        )

        # Thinking time + and -
        self.thinking_time_plus = self.plus_image.get_rect(
            center=(self.set_thinking_time_rect.centerx + 95,
                    self.set_thinking_time_rect.bottom + self.set_thinking_time_rect.height)
        )
        self.thinking_time_minus = self.minus_image.get_rect(
            center=(self.set_thinking_time_rect.centerx - 95,
                    self.set_thinking_time_rect.bottom + self.set_thinking_time_rect.height)
        )

        # Mistakes allowed + and -
        self.mistakes_allowed_plus = self.plus_image.get_rect(
            center=(self.mistakes_allowed_rect.centerx + 95,
                    self.mistakes_allowed_rect.bottom + self.mistakes_allowed_rect.height)
        )
        self.mistakes_allowed_minus = self.minus_image.get_rect(
            center=(self.mistakes_allowed_rect.centerx - 95,
                    self.mistakes_allowed_rect.bottom + self.mistakes_allowed_rect.height)
        )

    def challenge_screen_objects(self):
        self.images_initialization()

        # Texts
        self.your_time_text = self.candara_72_font.render("Your time:", True, 'white')
        self.thinking_time_text = self.candara_60_font.render("Thinking time:", True, 'white')

        self.goal_text = self.candara_60_font.render("Goal: " + str(self.goal_digit_counter), True, 'white')

        #   Game_over texts
        self.game_text = self.candara_96_font.render("Game", True, 'white')
        self.over_text = self.candara_96_font.render("Over", True, 'white')

        #   Winning texts
        self.win_main_text = self.candara_96_font.render("Good job!", True, 'white')
        self.win_second_text = self.calibri_55_font.render("You have reached the goal", True, 'yellow')

        # Rectangles
        self.guessing_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,  # Position
                                     self.screen_width * 0.88, self.screen_height * 0.12)  # Size

        self.goal_rect = self.goal_text.get_rect(
            center=(self.guessing_rect.left + self.screen_width * 0.12,
                    self.guessing_rect.bottom + 2.8 * self.guessing_rect.height)
        )

        self.your_time_rect = self.your_time_text.get_rect(
            center=(self.back_button_rect.centerx, self.guessing_rect.bottom + self.guessing_rect.height)
        )
        self.thinking_time_rect = self.thinking_time_text.get_rect(
            center=(self.goal_rect.centerx, self.goal_rect.bottom + 2 * self.goal_rect.height)
        )

        self.game_rect = self.game_text.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.45)
        )
        self.over_rect = self.over_text.get_rect(
            center=(self.game_rect.centerx, self.game_rect.bottom + self.game_rect.height)
        )

        self.win_main_rect = self.win_main_text.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.5)
        )
        self.win_second_rect = self.win_second_text.get_rect(
            center=(self.win_main_rect.centerx, self.win_main_rect.bottom + self.win_main_rect.height)
        )

        # Buttons and counters
        self.switch_keys_layout_text = self.calibri_40_font.render("Switch the keys layout", True, 'white')
        self.switch_keys_layout_rect = pg.Rect(self.guessing_rect.left,
                                               self.guessing_rect.bottom + self.guessing_rect.height,
                                               self.screen_width * 0.24, self.screen_height * 0.12)
        self.switch_keys_layout_text_rect = self.switch_keys_layout_text.get_rect(
            center=self.switch_keys_layout_rect.center)

        self.back_button_text = self.candara_60_font.render("Back", True, 'white')
        self.back_button_rect = pg.Rect(self.guessing_rect.right - self.screen_width * 0.24,  # Position X
                                        self.switch_keys_layout_rect.bottom + self.switch_keys_layout_rect.height * 1.4,
                                        # Position Y
                                        self.screen_width * 0.24, self.screen_height * 0.12)  # Size
        self.back_button_text_rect = self.back_button_text.get_rect(center=self.back_button_rect.center)

        # Keyboard initialization method
        self.keys_initialization()

        # Images rectangles

    def learning_screen_logic(self):
        self.learning_screen_objects()

        if self.digits_in_columns_counter == 1:
            self.x = 50
            self.columns = 20
        elif self.digits_in_columns_counter == 2:
            self.x = 55
            self.columns = 15
        elif self.digits_in_columns_counter == 3:
            self.x = 70
            self.columns = 10
        elif self.digits_in_columns_counter == 4 or self.digits_in_columns_counter == 5:
            self.x = 85
            self.columns = 6
        elif self.digits_in_columns_counter == 6:
            self.x = 110
            self.columns = 5
        elif self.digits_in_columns_counter == 7 or self.digits_in_columns_counter == 8:
            self.x = 105
            self.columns = 4
        elif self.digits_in_columns_counter == 9 or self.digits_in_columns_counter == 10:
            self.x = 135
            self.columns = 3

    def learning_screen(self):
        learning_running = True
        self.main_values()
        self.learning_screen_logic()

        while learning_running:
            self.screen.fill((69, 69, 69))  # Dark gray color

            # Text drawing on the screen
            self.screen.blit(self.digits_in_columns_text, self.digits_in_columns_rect)
            self.screen.blit(self.page_number_text, self.page_number_rect)
            self.screen.blit(self.page_change_multiplier_text, self.page_change_multiplier_rect)
            self.screen.blit(self.digits_on_page_text, self.digits_on_page_rect)

            # Counters text drawing
            self.screen.blit(self.digits_in_columns_counter_text, self.digits_in_columns_counter_rect)
            self.screen.blit(self.page_number_counter_text, self.page_number_counter_rect)
            self.screen.blit(self.page_change_multiplier_counter_text, self.page_change_multiplier_counter_rect)

            # Images drawing on the screen
            self.screen.blit(self.minus_image, self.digits_in_columns_minus)
            self.screen.blit(self.plus_image, self.digits_in_columns_plus)

            self.screen.blit(self.minus_image, self.page_number_minus)
            self.screen.blit(self.plus_image, self.page_number_plus)

            self.screen.blit(self.minus_image, self.page_change_multiplier_minus)
            self.screen.blit(self.plus_image, self.page_change_multiplier_plus)

            # Drawing buttons
            pg.draw.rect(self.screen, 'white', self.digits_rect, 3)
            pg.draw.rect(self.screen, 'white', self.l_s_back_button_rect, 3)

            self.screen.blit(self.l_s_back_button_text, self.l_s_back_button_text_rect)

            # Drawing digits method
            self.draw_learning_pi_digits()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    learning_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.l_s_back_button_rect.collidepoint(event.pos):
                        learning_running = False
                        self.main_screen()

                    # digits_in_columns - and + handling
                    if self.digits_in_columns_minus.collidepoint(event.pos):
                        self.draw_learning_pi_digits()
                        if self.digits_in_columns_counter > 1:
                            self.digits_in_columns_counter -= 1
                            self.learning_screen_logic()
                        self.digits_in_columns_counter_text = self.calibri_40_font.render(
                            str(self.digits_in_columns_counter), True, 'white')

                    if self.digits_in_columns_plus.collidepoint(event.pos):
                        self.draw_learning_pi_digits()
                        if self.digits_in_columns_counter < 10:
                            self.digits_in_columns_counter += 1
                            self.learning_screen_logic()
                        self.digits_in_columns_counter_text = self.calibri_40_font.render(
                            str(self.digits_in_columns_counter), True, 'white')

                    # page_number - and + handling
                    if self.page_number_minus.collidepoint(event.pos):
                        if self.page_number_counter - self.page_change_multiplier_counter >= 1:
                            self.page_number_counter -= self.page_change_multiplier_counter
                        else:
                            self.page_number_counter = 1
                        self.learning_screen_logic()
                        self.page_number_counter_text = self.calibri_40_font.render(
                            str(self.page_number_counter), True, 'white')

                    if self.page_number_plus.collidepoint(event.pos):
                        self.page_number_counter += self.page_change_multiplier_counter
                        self.learning_screen_logic()
                        self.page_number_counter_text = self.calibri_40_font.render(
                            str(self.page_number_counter), True, 'white')

                    # page_change_multiplier - and + handling
                    if self.page_change_multiplier_minus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.page_change_multipliers.index(self.page_change_multiplier_counter)

                        # Choose previous index, if it is not the beginning of the list
                        if current_index > 0:
                            self.page_change_multiplier_counter = self.page_change_multipliers[current_index - 1]
                            self.learning_screen_logic()
                            self.page_change_multiplier_counter_text = self.calibri_40_font.render(
                                "x" + str(self.page_change_multiplier_counter), True, 'white')

                    if self.page_change_multiplier_plus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.page_change_multipliers.index(self.page_change_multiplier_counter)

                        # Choose next index, if it is not the end of the list
                        if current_index < len(self.page_change_multipliers) - 1:
                            self.page_change_multiplier_counter = self.page_change_multipliers[current_index + 1]
                            self.learning_screen_logic()
                            self.page_change_multiplier_counter_text = self.calibri_40_font.render(
                                "x" + str(self.page_change_multiplier_counter), True, 'white')

            pg.display.flip()
            self.clock.tick(60)

    def training_screen_settings(self):
        training_settings_running = True
        self.main_values()
        self.training_screen_settings_objects()

        while training_settings_running:
            self.screen.fill((59, 59, 59))  # Dark gray color

            # Images drawing on the screen
            self.screen.blit(self.minus_image, self.start_digit_minus)
            self.screen.blit(self.plus_image, self.start_digit_plus)

            self.screen.blit(self.minus_image, self.digit_multiplier_minus)
            self.screen.blit(self.plus_image, self.digit_multiplier_plus)

            # Drawing rectangles
            self.screen.blit(self.training_mode_title_text, self.training_mode_title_rect)
            self.screen.blit(self.choose_start_point_text, self.choose_start_point_rect)
            self.screen.blit(self.start_digit_text, self.start_digit_rect)
            self.screen.blit(self.digit_multiplier_text, self.digit_multiplier_rect)

            self.screen.blit(self.start_digit_counter_text, self.start_digit_counter_rect)
            self.screen.blit(self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect)

            # Drawing buttons
            pg.draw.rect(self.screen, 'white', self.start_button_rect, 5)
            pg.draw.rect(self.screen, 'white', self.back_button_rect, 5)

            self.screen.blit(self.start_button_text, self.start_button_text_rect)
            self.screen.blit(self.back_button_text, self.back_button_text_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    training_settings_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        training_settings_running = False
                        self.main_screen()
                    if self.start_button_rect.collidepoint(event.pos):
                        training_settings_running = False
                        self.training_screen()

                    # start_digit - and + handling
                    if self.start_digit_minus.collidepoint(event.pos):
                        if self.start_digit_counter - self.digit_multiplier_counter >= 1:
                            self.start_digit_counter -= self.digit_multiplier_counter
                        else:
                            self.start_digit_counter = 1
                        self.training_screen_settings_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    if self.start_digit_plus.collidepoint(event.pos):
                        self.start_digit_counter += self.digit_multiplier_counter
                        self.training_screen_settings_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    # digit_multiplier - and + handling
                    if self.digit_multiplier_minus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)

                        # Choose previous index, if it is not the beginning of the list
                        if current_index > 0:
                            self.digit_multiplier_counter = self.digit_multipliers[current_index - 1]
                            self.training_screen_settings_objects()
                            self.digit_multiplier_counter_text = self.candara_50_font.render(
                                "x" + str(self.digit_multiplier_counter), True, 'white')

                    if self.digit_multiplier_plus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)

                        # Choose next index, if it is not the end of the list
                        if current_index < len(self.digit_multipliers) - 1:
                            self.digit_multiplier_counter = self.digit_multipliers[current_index + 1]
                            self.training_screen_settings_objects()
                            self.digit_multiplier_counter_text = self.candara_50_font.render(
                                "x" + str(self.digit_multiplier_counter), True, 'white')

            pg.display.flip()
            self.clock.tick(60)

    def training_screen(self):
        training_running = True
        self.training_screen_objects()

        start_time = time.time()  # Start time initialization
        reset_time = time.time()  # Time of last interaction with digit squares

        self.user_input = []
        self.incorrect_square_number = None
        self.next_correct_digit = None  # Initially no digit highlighted

        self.max_display_digits = int(self.guessing_rect.width / 37.53)  # Number of digits visible in guessing_rect

        while training_running:
            self.training_screen_objects()
            self.screen.fill((39, 39, 39))  # Dark gray color

            # Time calculation
            self.time_to_hint = time.time() - reset_time
            self.training_elapsed_time = time.time() - start_time
            formatted_time = time.strftime('%M:%S', time.gmtime(self.training_elapsed_time))  # Time formatted to MM:SS

            # Time rendering
            time_text = self.calibri_72_font.render(f"{formatted_time}", True, 'white')
            time_rect = time_text.get_rect(
                center=(self.your_time_rect.centerx, self.your_time_rect.bottom + self.your_time_rect.height * 0.7))
            self.screen.blit(time_text, time_rect)

            # Images drawing on the screen
            self.screen.blit(self.t_s_minus_image, self.hint_minus)
            self.screen.blit(self.t_s_plus_image, self.hint_plus)

            if self.switch_position == 0:
                time.sleep(0.1)
                self.screen.blit(self.switch_off_image, self.switch_off)
            elif self.switch_position == 1:
                time.sleep(0.1)
                self.screen.blit(self.switch_on_image, self.switch_on)

            # Drawing text
            # Digits drawing logic
            digits_str = "".join(self.user_input[-self.max_display_digits:])
            guessed_digits_text = self.calibri_72_font.render(f"{digits_str}", True, 'white')
            base_text = self.calibri_72_font.render("3. ", True, 'green')
            self.digit_number_text = self.calibri_55_font.render(
                "Digit: " + f"{self.digit_counter + self.start_digit_counter - 1}", True, 'white')

            self.guessed_digits_text_rect = guessed_digits_text.get_rect(
                center=(self.guessing_rect.right - self.digits_display_offset, self.guessing_rect.centery))
            self.base_text_rect = base_text.get_rect(
                center=(self.guessed_digits_text_rect.left - 25, self.guessing_rect.centery))
            self.digit_number_rect = self.digit_number_text.get_rect(
                center=(self.guessing_rect.centerx, self.guessing_rect.bottom + 0.4 * self.guessing_rect.height)
            )
            self.screen.blit(self.your_time_text, self.your_time_rect)

            if len(self.user_input) < self.max_display_digits - 1:
                if self.start_digit_counter == 1:
                    self.screen.blit(base_text, self.base_text_rect)
            self.screen.blit(guessed_digits_text, self.guessed_digits_text_rect)

            # Drawing rectangles
            pg.draw.rect(self.screen, 'white', self.guessing_rect, width=3)
            pg.draw.rect(self.screen, 'white', self.switch_keys_layout_rect, width=3)

            if self.switch_position == 0:
                pg.draw.rect(self.screen, (59, 59, 59), self.hint_rect, width=3)
            elif self.switch_position == 1:
                pg.draw.rect(self.screen, 'white', self.hint_rect, width=3)

            self.screen.blit(self.switch_keys_layout_text, self.switch_keys_layout_text_rect)
            self.screen.blit(self.hint_text, self.hint_text_rect)
            self.screen.blit(self.digit_number_text, self.digit_number_rect)

            # Drawing buttons
            pg.draw.rect(self.screen, 'white', self.back_button_rect, 3)

            self.screen.blit(self.back_button_text, self.back_button_text_rect)

            # Squares with digits
            for i in range(10):
                if i == self.next_correct_digit:
                    pg.draw.rect(self.screen, 'green', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))
                else:
                    pg.draw.rect(self.screen, 'white', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

            # Checking if wrong square clicked
            if self.incorrect_square_number:
                i = self.incorrect_square_number
                pg.draw.rect(self.screen, 'red', getattr(self, f'square_{i}_rect'), 5)
                self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

            # Check if time to hint
            if self.time_to_hint > self.hint_counter:
                if self.switch_position == 1:
                    pi_digits = self.read_pi_digits()[self.start_digit_counter - 1:]
                    self.next_correct_digit = int(pi_digits[len(self.user_input)])  # Set the next correct digit
                    reset_time = time.time()  # Reset the hint timer

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    training_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        training_running = False
                        self.main_values()
                        self.training_screen_settings()
                    if self.switch_on.collidepoint(event.pos):
                        if self.switch_position == 0:
                            self.screen.blit(self.switch_neutral_image, self.switch_neutral)
                            self.switch_position = 1
                        elif self.switch_position == 1:
                            self.screen.blit(self.switch_neutral_image, self.switch_neutral)
                            self.switch_position = 0
                    if self.hint_plus.collidepoint(event.pos) and self.switch_position == 1:
                        self.hint_counter = min(10, self.hint_counter + 1)
                    if self.hint_minus.collidepoint(event.pos) and self.switch_position == 1:
                        self.hint_counter = max(0, self.hint_counter - 1)
                    if self.switch_keys_layout_rect.collidepoint(event.pos):
                        self.keys_layout = 1 - self.keys_layout
                        self.training_screen_objects()

                    # Squares with digits
                    for i in range(10):
                        if getattr(self, f'square_{i}_rect').collidepoint(event.pos):
                            self.draw_digits(str(i))
                            reset_time = time.time()
                            self.next_correct_digit = None

            pg.display.flip()
            self.clock.tick(60)

    def draw_digits(self, user_input):
        self.incorrect_square_number = None
        pi_digits = self.read_pi_digits()[self.start_digit_counter - 1:]
        pi_tokens = list(pi_digits.replace(".", ""))

        tested_digits = self.user_input + [user_input]
        tested_token = pi_tokens[:len(tested_digits)]

        correct = self.compare_tokens(tested_digits, tested_token)
        if correct:
            self.user_input.append(user_input)
            self.digit_counter += 1
            if 1 < len(self.user_input) < self.max_display_digits + 1:
                self.digits_display_offset += 18.5
            return True
        else:
            self.mistakes_allowed_counter -= 1
            self.incorrect_square_number = user_input

    def compare_tokens(self, user_input, pi_tokens):
        user_input = list(user_input)

        if len(user_input) != len(pi_tokens):
            return False

        # Compare full strings
        for i in range(len(user_input)):
            if user_input[i] != pi_tokens[i]:
                return False

        return True

    def challenge_screen_settings(self):
        challenge_settings_running = True

        self.main_values()
        self.challenge_screen_settings_objects()

        while challenge_settings_running:
            self.screen.fill((59, 59, 59))  # Dark gray color

            # Images drawing on the screen
            self.screen.blit(self.minus_image, self.start_digit_minus)
            self.screen.blit(self.plus_image, self.start_digit_plus)

            self.screen.blit(self.minus_image, self.digit_multiplier_minus)
            self.screen.blit(self.plus_image, self.digit_multiplier_plus)

            self.screen.blit(self.minus_image, self.goal_digit_minus)
            self.screen.blit(self.plus_image, self.goal_digit_plus)

            self.screen.blit(self.minus_image, self.goal_digit_multiplier_minus)
            self.screen.blit(self.plus_image, self.goal_digit_multiplier_plus)

            self.screen.blit(self.minus_image, self.thinking_time_minus)
            self.screen.blit(self.plus_image, self.thinking_time_plus)

            self.screen.blit(self.minus_image, self.mistakes_allowed_minus)
            self.screen.blit(self.plus_image, self.mistakes_allowed_plus)

            # Drawing rectangles
            self.screen.blit(self.challenge_mode_title_text, self.challenge_mode_title_rect)

            # Start point
            self.screen.blit(self.choose_start_point_text, self.choose_start_point_rect)
            self.screen.blit(self.start_digit_text, self.start_digit_rect)
            self.screen.blit(self.digit_multiplier_text, self.digit_multiplier_rect)

            self.screen.blit(self.start_digit_counter_text, self.start_digit_counter_rect)
            self.screen.blit(self.digit_multiplier_counter_text, self.digit_multiplier_counter_rect)

            # Goal
            self.screen.blit(self.set_ch_goal_text, self.set_ch_goal_rect)
            self.screen.blit(self.start_digit_text, self.goal_digit_rect)
            self.screen.blit(self.digit_multiplier_text, self.goal_digit_multiplier_rect)

            self.screen.blit(self.goal_digit_counter_text, self.goal_digit_counter_rect)
            self.screen.blit(self.goal_digit_multiplier_counter_text, self.goal_digit_multiplier_counter_rect)

            # Thinking time
            self.screen.blit(self.set_thinking_time_text, self.set_thinking_time_rect)

            self.screen.blit(self.thinking_time_counter_text, self.thinking_time_counter_rect)

            # Mistakes allowed
            self.screen.blit(self.mistakes_allowed_text, self.mistakes_allowed_rect)

            self.screen.blit(self.mistakes_allowed_counter_text, self.mistakes_allowed_counter_rect)

            # Drawing buttons
            pg.draw.rect(self.screen, 'white', self.start_button_rect, 5)
            pg.draw.rect(self.screen, 'white', self.back_button_rect, 5)

            self.screen.blit(self.start_button_text, self.start_button_text_rect)
            self.screen.blit(self.back_button_text, self.back_button_text_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    challenge_settings_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        challenge_settings_running = False
                        self.main_screen()
                    if self.start_button_rect.collidepoint(event.pos):
                        challenge_settings_running = False
                        self.challenge_screen()

                    # Start digit - and + handling
                    if self.start_digit_minus.collidepoint(event.pos):
                        self.start_digit_counter = max(1, self.start_digit_counter - self.digit_multiplier_counter)
                        self.challenge_screen_settings_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    if self.start_digit_plus.collidepoint(event.pos):
                        self.start_digit_counter += self.digit_multiplier_counter
                        self.challenge_screen_settings_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    # digit_multiplier - and + handling
                    if self.digit_multiplier_minus.collidepoint(event.pos):
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)
                        self.digit_multiplier_counter = self.digit_multipliers[max(0, current_index - 1)]
                        self.challenge_screen_settings_objects()
                        self.digit_multiplier_counter_text = self.candara_50_font.render(
                            "x" + str(self.digit_multiplier_counter), True, 'white')

                    if self.digit_multiplier_plus.collidepoint(event.pos):
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)
                        self.digit_multiplier_counter = self.digit_multipliers[
                            min(len(self.digit_multipliers) - 1, current_index + 1)]
                        self.challenge_screen_settings_objects()
                        self.digit_multiplier_counter_text = self.candara_50_font.render(
                            "x" + str(self.digit_multiplier_counter), True, 'white')

                    # Goal digit - and + handling
                    if self.goal_digit_minus.collidepoint(event.pos):
                        self.goal_digit_counter = max(25, self.goal_digit_counter - self.goal_digit_multiplier_counter)
                        self.challenge_screen_settings_objects()
                        self.goal_digit_counter_text = self.candara_50_font.render(
                            str(self.goal_digit_counter), True, 'white')

                    if self.goal_digit_plus.collidepoint(event.pos):
                        self.goal_digit_counter += self.goal_digit_multiplier_counter
                        self.challenge_screen_settings_objects()
                        self.goal_digit_counter_text = self.candara_50_font.render(
                            str(self.goal_digit_counter), True, 'white')

                    # Goal multiplier - and + handling
                    if self.goal_digit_multiplier_minus.collidepoint(event.pos):
                        current_index = self.goal_digit_multipliers.index(self.goal_digit_multiplier_counter)
                        self.goal_digit_multiplier_counter = self.goal_digit_multipliers[max(0, current_index - 1)]
                        self.challenge_screen_settings_objects()
                        self.goal_digit_multiplier_counter_text = self.candara_50_font.render(
                            "x" + str(self.goal_digit_multiplier_counter), True, 'white')

                    if self.goal_digit_multiplier_plus.collidepoint(event.pos):
                        current_index = self.goal_digit_multipliers.index(self.goal_digit_multiplier_counter)
                        self.goal_digit_multiplier_counter = self.goal_digit_multipliers[
                            min(len(self.goal_digit_multipliers) - 1, current_index + 1)]
                        self.challenge_screen_settings_objects()
                        self.goal_digit_multiplier_counter_text = self.candara_50_font.render(
                            "x" + str(self.goal_digit_multiplier_counter), True, 'white')

                    # Thinking time - and + handling
                    if self.thinking_time_minus.collidepoint(event.pos):
                        self.thinking_time_counter = max(5, self.thinking_time_counter - 5)
                        self.challenge_screen_settings_objects()
                        self.thinking_time_counter_text = self.candara_50_font.render(
                            str(self.thinking_time_counter), True, 'white')

                    if self.thinking_time_plus.collidepoint(event.pos):
                        self.thinking_time_counter = min(60, self.thinking_time_counter + 5)
                        self.challenge_screen_settings_objects()
                        self.thinking_time_counter_text = self.candara_50_font.render(
                            str(self.thinking_time_counter), True, 'white')

                    # Mistakes allowed - and + handling
                    if self.mistakes_allowed_minus.collidepoint(event.pos):
                        self.mistakes_allowed_counter = max(1, self.mistakes_allowed_counter - 1)
                        self.challenge_screen_settings_objects()
                        self.mistakes_allowed_counter_text = self.candara_50_font.render(
                            str(self.mistakes_allowed_counter), True, 'white')

                    if self.mistakes_allowed_plus.collidepoint(event.pos):
                        self.mistakes_allowed_counter = min(5, self.mistakes_allowed_counter + 1)
                        self.challenge_screen_settings_objects()
                        self.mistakes_allowed_counter_text = self.candara_50_font.render(
                            str(self.mistakes_allowed_counter), True, 'white')

            pg.display.flip()
            self.clock.tick(60)

    def hearts_drawing(self):
        if self.mistakes_allowed_counter:
            for i in range(self.mistakes_allowed_counter):
                mistakes_allowed_heart = self.heart_image.get_rect(
                    center=(self.guessing_rect.right - self.screen_width * 0.019 - (i * self.screen_width * 0.039),
                            self.guessing_rect.bottom + 0.4 * self.guessing_rect.height)
                )

                self.screen.blit(self.heart_image, mistakes_allowed_heart)
        else:
            self.game_over = True

    def challenge_screen(self):
        challenge_running = True
        self.challenge_screen_objects()

        start_time = time.time()  # Start time initialization
        thinking_start_time = time.time()  # Thinking time start

        self.user_input = []
        self.incorrect_square_number = None
        self.goal_reached = False

        self.max_display_digits = int(self.guessing_rect.width / 37.53)  # Number of digits visible in guessing_rect

        while challenge_running:
            self.training_screen_objects()
            self.screen.fill((39, 39, 39))  # Dark gray color

            # Time calculation for overall time
            if self.game_over == False and self.goal_reached == False:
                self.training_elapsed_time = time.time() - start_time
            formatted_time = time.strftime('%M:%S', time.gmtime(self.training_elapsed_time))  # Time formatted to MM:SS

            # Time rendering
            if self.game_over:
                time_text = self.calibri_72_font.render(f"{formatted_time}", True, 'red')
            elif self.goal_reached:
                time_text = self.calibri_72_font.render(f"{formatted_time}", True, 'green')
            else:
                time_text = self.calibri_72_font.render(f"{formatted_time}", True, 'white')
            time_rect = time_text.get_rect(
                center=(self.your_time_rect.centerx, self.your_time_rect.bottom + self.your_time_rect.height * 0.7))
            self.screen.blit(time_text, time_rect)

            # Thinking time calculation (remaining time in seconds)
            if self.game_over == False and self.goal_reached == False:
                self.thinking_elapsed_time = time.time() - thinking_start_time
            remaining_thinking_time = max(self.thinking_time_counter - self.thinking_elapsed_time, 0)
            formatted_thinking_time = "{:.2f}".format(remaining_thinking_time)
            if remaining_thinking_time == 0:
                self.game_over = True

                # Thinking time rendering (format seconds:hundredths of a second)
                thinking_time_text = self.calibri_60_font.render(f"{formatted_thinking_time}", True, 'red')
            else:
                thinking_time_text = self.calibri_60_font.render(f"{formatted_thinking_time}", True, 'white')
            thinking_time_rect = thinking_time_text.get_rect(
                center=(self.thinking_time_rect.centerx,
                        self.thinking_time_rect.bottom + self.thinking_time_rect.height * 0.6))
            self.screen.blit(thinking_time_text, thinking_time_rect)

            # Images drawing on the screen
            self.hearts_drawing()

            # Drawing text
            self.screen.blit(self.goal_text, self.goal_rect)
            self.screen.blit(self.thinking_time_text, self.thinking_time_rect)

            # Digits drawing logic
            digits_str = "".join(self.user_input[-self.max_display_digits:])
            guessed_digits_text = self.calibri_72_font.render(f"{digits_str}", True, 'white')

            base_text = self.calibri_72_font.render("3. ", True, 'green')

            self.digit_number_text = self.calibri_55_font.render(
                "Digit: " + f"{self.digit_counter + self.start_digit_counter - 1}", True, 'white')

            self.guessed_digits_text_rect = guessed_digits_text.get_rect(
                center=(self.guessing_rect.right - self.digits_display_offset, self.guessing_rect.centery))
            self.base_text_rect = base_text.get_rect(
                center=(self.guessed_digits_text_rect.left - 25, self.guessing_rect.centery))
            self.digit_number_rect = self.digit_number_text.get_rect(
                center=(self.guessing_rect.centerx, self.guessing_rect.bottom + 0.4 * self.guessing_rect.height)
            )
            self.screen.blit(self.your_time_text, self.your_time_rect)

            if len(self.user_input) < self.max_display_digits - 1:
                if self.start_digit_counter == 1:
                    self.screen.blit(base_text, self.base_text_rect)
            self.screen.blit(guessed_digits_text, self.guessed_digits_text_rect)

            # Drawing rectangles
            pg.draw.rect(self.screen, 'white', self.guessing_rect, width=3)
            pg.draw.rect(self.screen, 'white', self.switch_keys_layout_rect, width=3)

            self.screen.blit(self.digit_number_text, self.digit_number_rect)

            # Drawing buttons
            if self.game_over or self.goal_reached:
                pg.draw.rect(self.screen, 'green', self.back_button_rect, 5)
            else:
                pg.draw.rect(self.screen, 'white', self.back_button_rect, 3)

            self.screen.blit(self.switch_keys_layout_text, self.switch_keys_layout_text_rect)
            self.screen.blit(self.back_button_text, self.back_button_text_rect)

            # Squares with digits
            if self.game_over:
                # Keyboard disappearing and Game Over printing
                self.screen.blit(self.game_text, self.game_rect)
                self.screen.blit(self.over_text, self.over_rect)

                # Printing 5 next correct digits
                pi_digits = self.read_pi_digits()[self.start_digit_counter - 1:]
                self.correct_digits_text = self.calibri_60_font.render(
                    "Should be: " + pi_digits[len(self.user_input):len(self.user_input) + 5] + "...",
                    True, 'yellow')

                self.correct_digits_rect = self.correct_digits_text.get_rect(
                    center=(self.over_rect.centerx, self.over_rect.bottom + self.over_rect.height * 0.5)
                )

                self.screen.blit(self.correct_digits_text, self.correct_digits_rect)

            # Winning condition
            elif self.digit_counter - 1 == self.goal_digit_counter:
                self.goal_reached = True
                self.goal_text = self.candara_60_font.render("Goal: " + str(self.goal_digit_counter), True, 'green')

                # Keyboard disappearing and Congrats printing
                self.screen.blit(self.win_main_text, self.win_main_rect)
                self.screen.blit(self.win_second_text, self.win_second_rect)

            else:
                # Printing keyboard only if it is not game_over
                for i in range(10):
                    pg.draw.rect(self.screen, 'white', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

                # Checking if wrong square clicked
                if self.incorrect_square_number:
                    i = self.incorrect_square_number
                    pg.draw.rect(self.screen, 'red', getattr(self, f'square_{i}_rect'), 5)
                    self.screen.blit(getattr(self, f'square_{i}_text'), getattr(self, f'square_{i}_text_rect'))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    challenge_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        challenge_running = False
                        self.main_values()
                        self.challenge_screen_settings()
                    if self.game_over == False or self.goal_reached == False:
                        if self.switch_keys_layout_rect.collidepoint(event.pos):
                            self.keys_layout = 1 - self.keys_layout
                            self.challenge_screen_objects()

                        # Squares with digits
                        for i in range(10):
                            if getattr(self, f'square_{i}_rect').collidepoint(event.pos):
                                if self.draw_digits(str(i)):
                                    thinking_start_time = time.time()  # Reset thinking time

            pg.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = PiGame()
    game.main_screen()
