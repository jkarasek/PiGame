import pygame as pg
import time
from pygame import font

class PiGame:
    def __init__(self):
        pg.init()  # Inicjalizacja Pygame

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
        self.candara_72_font = font.SysFont('candara', size=72)
        self.candara_60_font = font.SysFont('candara', size=60)
        self.candara_50_font = font.SysFont('candara', size=50)
        self.calibri_72_font =  font.SysFont('calibri', size=72)
        self.calibri_55_font =  font.SysFont('calibri', size=55)
        self.calibri_40_font = font.SysFont('calibri', size=40)
        self.cambria_35_font = font.SysFont('cambria', size=35)

        self.main_values()



    def main_values(self):
        # Learning screen counter
        self.digits_in_columns_counter = 5  # Main value

        self.page_change_multipliers = [1, 2, 5, 10, 100]
        self.page_change_multiplier_counter = 1  # Main value

        self.page_number_counter = 1

        self.digits_on_page_counter_bottom = 1  # Main value
        self.digits_on_page_counter_top = 1  # Main value
        self.digits_on_page_counter = 0

        # Training screen settings counters
        self.digit_multipliers = [1, 10, 50, 100, 1000]
        self.digit_multiplier_counter = 1
        self.start_digit_counter = 1

        # Training screen
        self.digits_display_offset = 30
        self.switch_position = 1
        self.keys_layout = 1
        self.digit_counter = 1
        self.hint_counter = 4


    # Main screen initialization
    def main_screen(self):
        main_running = True
        self.screens_objects()

        while main_running:
            self.screen.fill('black')

            # Text displayed
            title_text = self.calibri_40_font.render("PiGameLogo", True, 'white')
            title_rect = title_text.get_rect(center=(self.screen_width * 0.5, self.screen_height * 0.20))

            # Text drawing on the screen
            self.screen.blit(title_text, title_rect)

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
                        main_running = False
                    if self.learning_button_rect.collidepoint(event.pos):
                        self.learning_screen()
                    if self.training_button_rect.collidepoint(event.pos):
                        self.training_screen_settings()
                    if self.challenge_button_rect.collidepoint(event.pos):
                        self.challenge_screen_settings()

            pg.display.flip()
            self.clock.tick(60)  # Częstotliwość odświeżania

        pg.quit()  # Zamknij Pygame po zakończeniu pętli

    def read_pi_digits(self):
        try:
            with open('pi_digits.txt', 'r') as file:
                pi_digits = file.read().strip().replace('\n', '')
                return pi_digits
        except FileNotFoundError:
            return "Error: pi_digits.txt not found."

    def draw_pi_digits(self):
        # Loading digits (list)
        pi_digits = self.read_pi_digits()

        # Start (main) value of bottom digits counter
        self.digits_on_page_counter_bottom = 1

        # Pages logic
        if self.page_number_counter == 2:
            pi_digits = pi_digits[self.digits_on_page_counter:]
            self.digits_on_page_counter_bottom = self.digits_on_page_counter
        if self.page_number_counter > 2:
            pi_digits = pi_digits[(self.page_number_counter-1) * self.digits_on_page_counter:]
            self.digits_on_page_counter_bottom = (self.page_number_counter - 1) * self.digits_on_page_counter

        x = self.x  # start X position of digits rectangle
        y = 35      # start Y position of digits rectangle

        # Drawing loop
        for i, digit in enumerate(pi_digits):

            # Text rendering
            text = self.calibri_40_font.render(str(pi_digits[:self.digits_in_columns_counter]), True, 'white')
            pi_digits = pi_digits[self.digits_in_columns_counter:]

            # Creating a rectangle for text
            rect = text.get_rect(center=(self.screen_width * 0.075 + x, self.screen_height * 0.1 + y))

            # Checking if the rectangle extends beyond right frame edge
            if (rect.right+15) > self.digits_rect.right:
                x = self.x  # Reset X position
                y += 50  # Start printing from a new line
                rect = text.get_rect(
                    center=(self.screen_width * 0.075 + x, self.screen_height * 0.1 + y))  # Rect position update

            # Checking if the rectangle extends beyond bottom frame edge
            if rect.bottom > self.digits_rect.bottom:

                # Digits in page counter update
                self.digits_on_page_counter = i * self.digits_in_columns_counter
                self.digits_on_page_counter_top = self.page_number_counter * self.digits_on_page_counter

                # Digits in page counter drawing
                self.screens_objects()
                self.screen.blit(self.digits_on_page_counter_text, self.digits_on_page_counter_rect)
                break

            # Space between columns for next digits
            x += ((1100 - (self.digits_in_columns_counter * 20 * self.columns)) / self.columns) + self.digits_in_columns_counter * 20

           # pg.draw.rect(self.screen, 'red', rect, 2)  # 2 - grubość linii

            # Text drawing
            self.screen.blit(text, rect)

    def screens_objects(self):
        ### Text displayed
        # Main screen
        self.learning_button_text = self.cambria_35_font.render("Learning", True, 'white')
        self.training_button_text = self.cambria_35_font.render("Training", True, 'white')
        self.challenge_button_text = self.cambria_35_font.render("Challenge", True, 'white')
        self.quit_button_text = self.cambria_35_font.render("Quit", True, 'white')

        # Learning screen
        self.digits_in_columns_text = self.calibri_40_font.render("Digits in columns:", True, 'white')
        self.page_number_text = self.calibri_40_font.render("Page number:", True, 'white')
        self.page_change_mulltiplier_text = self.calibri_40_font.render("Page change multiplier:", True, 'white')
        self.digits_on_page_text = self.calibri_40_font.render("Digits on page:", True, 'white')

        # Training screen settings
        self.training_mode_title_text = self.candara_72_font.render("Training mode", True, 'white')
        self.choose_start_point_text = self.candara_60_font.render("Choose a start point", True, 'white')

        self.start_digit_text = self.calibri_40_font.render("Digit:", True, 'white')
        self.digit_multiplier_text = self.calibri_40_font.render("Multiplier:", True, 'white')

        self.t_s_s_start_button_text = self.candara_60_font.render("Start", True, 'white')
        self.t_s_s_back_button_text = self.candara_60_font.render("Back", True, 'white')

        # Training screen
        self.switch_keys_layout_text = self.calibri_40_font.render("Switch the keys layout", True, 'white')
        if self.switch_position == 0:
            self.hint_text = self.calibri_40_font.render("Hint after: " + str(self.hint_counter) + " seconds", True, (59, 59, 59))
        elif self.switch_position == 1:
            self.hint_text = self.calibri_40_font.render("Hint after: " + str(self.hint_counter) + " seconds", True, 'white')
        self.your_time_text = self.candara_72_font.render("Your time:", True, 'white')
        self.t_s_back_button_text = self.t_s_s_back_button_text

        #   Squares
        self.square_0_text = self.calibri_72_font.render("0", True, 'white')
        self.square_1_text = self.calibri_72_font.render("1", True, 'white')
        self.square_2_text = self.calibri_72_font.render("2", True, 'white')
        self.square_3_text = self.calibri_72_font.render("3", True, 'white')
        self.square_4_text = self.calibri_72_font.render("4", True, 'white')
        self.square_5_text = self.calibri_72_font.render("5", True, 'white')
        self.square_6_text = self.calibri_72_font.render("6", True, 'white')
        self.square_7_text = self.calibri_72_font.render("7", True, 'white')
        self.square_8_text = self.calibri_72_font.render("8", True, 'white')
        self.square_9_text = self.calibri_72_font.render("9", True, 'white')


        ### Counters text
        # Learning screen
        self.l_s_back_button_text = self.cambria_35_font.render("Back", True, 'white')

        self.digits_in_columns_counter_text = self.calibri_40_font.render(str(self.digits_in_columns_counter), True, 'white')
        self.page_number_counter_text = self.calibri_40_font.render(str(self.page_number_counter), True, 'white')
        self.page_change_multiplier_counter_text = self.calibri_40_font.render("x"+str(self.page_change_multiplier_counter), True, 'white')
        self.digits_on_page_counter_text = self.calibri_40_font.render(str(self.digits_on_page_counter_bottom) + " - " + str(self.digits_on_page_counter_top), True, 'white')

        # Training screen settings
        self.start_digit_counter_text = self.candara_50_font.render(str(self.start_digit_counter), True, 'white')
        self.digit_multiplier_counter_text = self.candara_50_font.render("x" + str(self.digit_multiplier_counter), True, 'white')


        ### Rectangles
        # Main screen (buttons)
        self.learning_button_rect = pg.Rect(self.screen_width * 0.42, self.screen_height * 0.30,
                                            self.screen_width * 0.16, self.screen_height * 0.08)
        self.training_button_rect = pg.Rect(self.learning_button_rect.left, self.learning_button_rect.bottom + 20,
                                            self.screen_width * 0.16, self.screen_height * 0.08)
        self.challenge_button_rect = pg.Rect(self.learning_button_rect.left, self.training_button_rect.bottom + 20,
                                            self.screen_width * 0.16, self.screen_height * 0.08)
        self.quit_button_rect = pg.Rect(self.learning_button_rect.left, self.challenge_button_rect.bottom + 120,
                                            self.screen_width * 0.16, self.screen_height * 0.08)

        self.learning_button_text_rect = self.learning_button_text.get_rect(center=self.learning_button_rect.center)
        self.training_button_text_rect = self.training_button_text.get_rect(center=self.training_button_rect.center)
        self.challenge_button_text_rect = self.challenge_button_text.get_rect(center=self.challenge_button_rect.center)
        self.quit_button_text_rect = self.quit_button_text.get_rect(center=self.quit_button_rect.center)


        # Learning screen (buttons)
        #   Learning screen main digit surface
        self.digits_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,      # Position
             self.screen_width * 0.6, self.screen_height * 0.8)                             # Size)

        #   Learning screen back button
        self.l_s_back_button_rect = pg.Rect(self.digits_rect.right + 0.5 * (self.screen_width-self.digits_rect.right) - self.screen_width * 0.08,    # Position X
             self.digits_rect.bottom - self.screen_height * 0.08,       # Position Y
             self.screen_width * 0.16, self.screen_height * 0.08)       # Size

        self.l_s_back_button_text_rect = self.l_s_back_button_text.get_rect(center=self.l_s_back_button_rect.center)

        # Learning screen (rectangles)
        self.digits_in_columns_rect = self.digits_in_columns_text.get_rect(
            center=(self.digits_rect.right + 0.5 * (self.screen_width - self.digits_rect.right), self.digits_rect.top + 25)
        )
        self.page_number_rect = self.page_number_text.get_rect(
            center=(self.digits_in_columns_rect.centerx, self.digits_in_columns_rect.centery + self.digits_in_columns_rect.height*4)
        )
        self.page_change_mulltiplier_rect = self.page_change_mulltiplier_text.get_rect(
            center=(self.digits_in_columns_rect.centerx, self.page_number_rect.centery + self.digits_in_columns_rect.height*4)
        )
        self.digits_on_page_rect = self.digits_on_page_text.get_rect(
            center=(self.digits_in_columns_rect.centerx, self.page_change_mulltiplier_rect.centery + 5 * self.digits_in_columns_rect.height)
        )



        # Training screen settings (rectangles)
        self.training_mode_title_rect = self.training_mode_title_text.get_rect(
            center=(self.screen_width * 0.5, self.screen_height * 0.2)
        )
        self.choose_start_point_rect = self.choose_start_point_text.get_rect(
            center=(
            self.screen_width * 0.5, self.training_mode_title_rect.bottom + self.training_mode_title_rect.height * 2)
        )
        self.start_digit_rect = self.start_digit_text.get_rect(
            center=(self.training_mode_title_rect.left,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )
        self.digit_multiplier_rect = self.digit_multiplier_text.get_rect(
            center=(self.training_mode_title_rect.right,
                    self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 0.5)
        )


        # Training screen settings (buttons)
        self.t_s_s_start_button_rect = pg.Rect(self.training_mode_title_rect.centerx - self.screen_width * 0.08,                                         # Position X
                                               self.choose_start_point_rect.bottom + self.choose_start_point_rect.height * 4,                            # Position Y
                                               self.screen_width * 0.16, self.screen_height * 0.08)                                                      # Size
        self.t_s_s_back_button_rect = pg.Rect(self.t_s_s_start_button_rect.left,                                                                         # Position X
                                               self.t_s_s_start_button_rect.bottom + 20,                                                                 # Position Y
                                               self.screen_width * 0.16, self.screen_height * 0.08)                                                      # Size

        self.t_s_s_start_button_text_rect = self.t_s_s_start_button_text.get_rect(center=self.t_s_s_start_button_rect.center)
        self.t_s_s_back_button_text_rect = self.t_s_s_back_button_text.get_rect(center=self.t_s_s_back_button_rect.center)

        # Training screen (rectangles)
        self.guessing_rect = pg.Rect(self.screen_width * 0.06, self.screen_height * 0.1,    # Position
                                     self.screen_width * 0.88, self.screen_height * 0.12)       # Size)

        self.switch_keys_layout_rect = pg.Rect(self.guessing_rect.left, self.guessing_rect.bottom + self.guessing_rect.height,
                                               self.screen_width * 0.24, self.screen_height * 0.12)

        self.hint_rect = pg.Rect(self.guessing_rect.left, self.switch_keys_layout_rect.bottom + self.switch_keys_layout_rect.height * 0.4,
                                            self.screen_width * 0.24, self.screen_height * 0.12)


        self.switch_keys_layout_text_rect = self.switch_keys_layout_text.get_rect(center=self.switch_keys_layout_rect.center)
        self.hint_text_rect = self.hint_text.get_rect(center=self.hint_rect.center)

        # Training screen (buttons)
        self.t_s_back_button_rect = pg.Rect(self.guessing_rect.right - self.screen_width * 0.24,         # Position X
                                            self.hint_rect.bottom + self.hint_rect.height * 0.4,         # Position Y
                                            self.screen_width * 0.24, self.screen_height * 0.12)         # Size

        self.t_s_back_button_text_rect = self.t_s_back_button_text.get_rect(center=self.t_s_back_button_rect.center)

        self.your_time_rect = self.your_time_text.get_rect(
            center=(self.t_s_back_button_rect.centerx, self.switch_keys_layout_rect.centery)
        )

        # Keys layout options
        if self.keys_layout == 0:
            self.square_1_y_pos = self.switch_keys_layout_rect.y
            self.square_7_y_pos = self.t_s_back_button_rect.y
        elif self.keys_layout == 1:
            self.square_1_y_pos = self.t_s_back_button_rect.y
            self.square_7_y_pos = self.switch_keys_layout_rect.y

            # Squares with digits
        self.square_0_rect = pg.Rect(self.guessing_rect.centerx - 0.06 * self.screen_height,                # Position X
                                     self.t_s_back_button_rect.bottom + self.t_s_back_button_rect.height * 0.4,   # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_1_rect = pg.Rect(self.square_0_rect.left - self.square_0_rect.width - self.guessing_rect.height * 0.5,             # Position X
                                     self.square_1_y_pos,                # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_2_rect = pg.Rect(self.square_0_rect.x,                                                  # Position X
                                     self.square_1_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_3_rect = pg.Rect(self.square_0_rect.left + self.square_0_rect.width + self.guessing_rect.height * 0.5,             # Position X
                                     self.square_1_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_4_rect = pg.Rect(self.square_1_rect.x,                                                  # Position X
                                     self.hint_rect.y,                                                      # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_5_rect = pg.Rect(self.square_2_rect.x,                                                  # Position X
                                     self.square_4_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_6_rect = pg.Rect(self.square_3_rect.x,                                                  # Position X
                                     self.square_4_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_7_rect = pg.Rect(self.square_1_rect.x,                                                  # Position X
                                     self.square_7_y_pos,                                           # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_8_rect = pg.Rect(self.square_2_rect.x,                                                  # Position X
                                     self.square_7_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_9_rect = pg.Rect(self.square_3_rect.x,                                                  # Position X
                                     self.square_7_rect.y,                                                  # Position Y
                                     self.screen_height * 0.12, self.screen_height * 0.12)                    # Size

        self.square_0_text_rect = self.square_0_text.get_rect(center=self.square_0_rect.center)
        self.square_1_text_rect = self.square_1_text.get_rect(center=self.square_1_rect.center)
        self.square_2_text_rect = self.square_2_text.get_rect(center=self.square_2_rect.center)
        self.square_3_text_rect = self.square_3_text.get_rect(center=self.square_3_rect.center)
        self.square_4_text_rect = self.square_4_text.get_rect(center=self.square_4_rect.center)
        self.square_5_text_rect = self.square_5_text.get_rect(center=self.square_5_rect.center)
        self.square_6_text_rect = self.square_6_text.get_rect(center=self.square_6_rect.center)
        self.square_7_text_rect = self.square_7_text.get_rect(center=self.square_7_rect.center)
        self.square_8_text_rect = self.square_8_text.get_rect(center=self.square_8_rect.center)
        self.square_9_text_rect = self.square_9_text.get_rect(center=self.square_9_rect.center)

        ### Counters rectangles
        # Learning screen
        self.digits_in_columns_counter_rect = self.digits_in_columns_counter_text.get_rect(
            center=(self.digits_in_columns_rect.centerx, self.digits_in_columns_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.page_number_counter_rect = self.page_number_counter_text.get_rect(
            center=(self.page_number_rect.centerx, self.page_number_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.page_change_multiplier_counter_rect = self.page_change_multiplier_counter_text.get_rect(
            center=(self.page_change_mulltiplier_rect.centerx, self.page_change_mulltiplier_rect.bottom + self.digits_in_columns_rect.height)
        )
        self.digits_on_page_counter_rect = self.digits_on_page_counter_text.get_rect(
            center=(self.digits_on_page_rect.centerx, self.digits_on_page_rect.bottom + self.digits_in_columns_rect.height)
        )

        # Training screen settings
        self.start_digit_counter_rect = self.start_digit_counter_text.get_rect(
            center=(self.start_digit_rect.centerx, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_counter_rect = self.digit_multiplier_counter_text.get_rect(
            center=(self.digit_multiplier_rect.centerx, self.digit_multiplier_rect.bottom + self.digit_multiplier_rect.height)
        )


        # Images
        minus_image = pg.image.load('images/minus.png')
        plus_image = pg.image.load('images/plus.png')
        switch_on_image = pg.image.load('images/switch_on.png')
        switch_off_image = pg.image.load('images/switch_off.png')
        switch_neutral_image = pg.image.load('images/switch_neutral.png')

        # Scaling images
        self.minus_image = pg.transform.scale(minus_image, (self.screen_width * 0.035, self.screen_width * 0.035))
        self.plus_image = pg.transform.scale(plus_image, (self.screen_width * 0.035, self.screen_width * 0.035))

        self.t_s_minus_image = pg.transform.scale(minus_image, (self.screen_width * 0.06, self.screen_width * 0.06))
        self.t_s_plus_image = pg.transform.scale(plus_image, (self.screen_width * 0.06, self.screen_width * 0.06))

        self.switch_on_image = pg.transform.scale(switch_on_image, (self.screen_width * 0.06, self.screen_width * 0.03))
        self.switch_off_image = pg.transform.scale(switch_off_image, (self.screen_width * 0.06, self.screen_width * 0.03))
        self.switch_neutral_image = pg.transform.scale(switch_neutral_image, (self.screen_width * 0.06, self.screen_width * 0.03))

        ### Images rectangles
        # Learning screen
        self.digits_in_columns_minus = self.minus_image.get_rect(
            center=(self.digits_in_columns_rect.centerx - 80, self.digits_in_columns_rect.bottom + self.digits_in_columns_rect.height)
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
            center=(self.page_number_minus.centerx, self.page_change_mulltiplier_rect.bottom + self.page_change_mulltiplier_rect.height)
        )
        self.page_change_multiplier_plus = self.plus_image.get_rect(
            center=(self.page_number_plus.centerx, self.page_change_multiplier_minus.centery)
        )

        # Training screen settings
        self.start_digit_plus = self.plus_image.get_rect(
            center=(self.start_digit_rect.centerx + 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.start_digit_minus = self.minus_image.get_rect(
            center=(self.start_digit_rect.centerx - 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_plus = self.plus_image.get_rect(
            center=(self.digit_multiplier_rect.centerx + 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )
        self.digit_multiplier_minus = self.minus_image.get_rect(
            center=(self.digit_multiplier_rect.centerx - 95, self.start_digit_rect.bottom + self.start_digit_rect.height)
        )

        # Training screen
        self.hint_minus = self.t_s_minus_image.get_rect(
            center=(self.hint_rect.centerx - (self.hint_rect.width * 0.5) + self.screen_width * 0.03, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.hint_plus = self.t_s_plus_image.get_rect(
            center=(self.hint_rect.centerx, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_on = self.switch_on_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_off = self.switch_off_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )
        self.switch_neutral = self.switch_neutral_image.get_rect(
            center=(self.hint_rect.centerx + (self.hint_rect.width * 0.5) - self.screen_width * 0.03, self.hint_rect.bottom + self.hint_rect.height * 0.7)
        )



    def learning_screen_logic(self):
        self.screens_objects()

        if self.digits_in_columns_counter == 1:
            self.x = 25
            self.columns = 20
        elif self.digits_in_columns_counter == 2:
            self.x = 35
            self.columns = 15
        elif self.digits_in_columns_counter == 3:
            self.x = 50
            self.columns = 10
        elif self.digits_in_columns_counter == 4 or self.digits_in_columns_counter == 5:
            self.x = 65
            self.columns = 8
        elif self.digits_in_columns_counter == 6:
            self.x = 90
            self.columns = 6
        elif self.digits_in_columns_counter == 7 or self.digits_in_columns_counter == 8:
            self.x = 105
            self.columns = 5
        elif self.digits_in_columns_counter == 9 or self.digits_in_columns_counter == 10:
            self.x = 135
            self.columns = 4

    def learning_screen(self):
        learning_running = True
        self.main_values()
        self.learning_screen_logic()

        while learning_running:
            self.screen.fill((69, 69, 69))  # Dark gray color

            # Text drawing on the screen
            self.screen.blit(self.digits_in_columns_text, self.digits_in_columns_rect)
            self.screen.blit(self.page_number_text, self.page_number_rect)
            self.screen.blit(self.page_change_mulltiplier_text, self.page_change_mulltiplier_rect)
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
            self.draw_pi_digits()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    learning_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.l_s_back_button_rect.collidepoint(event.pos):
                        return

                    # digits_in_columns - and + handling
                    if self.digits_in_columns_minus.collidepoint(event.pos):
                        self.draw_pi_digits()
                        if self.digits_in_columns_counter > 1:
                            self.digits_in_columns_counter -= 1
                            self.learning_screen_logic()
                        self.digits_in_columns_counter_text = self.calibri_40_font.render(
                            str(self.digits_in_columns_counter), True, 'white')

                    if self.digits_in_columns_plus.collidepoint(event.pos):
                        self.draw_pi_digits()
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
        self.screens_objects()


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
            pg.draw.rect(self.screen, 'white', self.t_s_s_start_button_rect, 5)
            pg.draw.rect(self.screen, 'white', self.t_s_s_back_button_rect, 5)

            self.screen.blit(self.t_s_s_start_button_text, self.t_s_s_start_button_text_rect)
            self.screen.blit(self.t_s_s_back_button_text, self.t_s_s_back_button_text_rect)


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    training_settings_running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.t_s_s_back_button_rect.collidepoint(event.pos):
                        return
                    if self.t_s_s_start_button_rect.collidepoint(event.pos):
                        self.training_screen()

                    # start_digit - and + handling
                    if self.start_digit_minus.collidepoint(event.pos):
                        if self.start_digit_counter - self.digit_multiplier_counter >= 1:
                            self.start_digit_counter -= self.digit_multiplier_counter
                        else:
                            self.start_digit_counter = 1
                        self.screens_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    if self.start_digit_plus.collidepoint(event.pos):
                        self.start_digit_counter += self.digit_multiplier_counter
                        self.screens_objects()
                        self.start_digit_counter_text = self.candara_50_font.render(
                            str(self.start_digit_counter), True, 'white')

                    # digit_multiplier - and + handling
                    if self.digit_multiplier_minus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)

                        # Choose previous index, if it is not the beginning of the list
                        if current_index > 0:
                            self.digit_multiplier_counter = self.digit_multipliers[current_index - 1]
                            self.screens_objects()
                            self.digit_multiplier_counter_text = self.candara_50_font.render(
                                "x" + str(self.digit_multiplier_counter), True, 'white')

                    if self.digit_multiplier_plus.collidepoint(event.pos):
                        # Current multiplier index
                        current_index = self.digit_multipliers.index(self.digit_multiplier_counter)

                        # Choose next index, if it is not the end of the list
                        if current_index < len(self.digit_multipliers) - 1:
                            self.digit_multiplier_counter = self.digit_multipliers[current_index + 1]
                            self.screens_objects()
                            self.digit_multiplier_counter_text = self.candara_50_font.render(
                                "x" + str(self.digit_multiplier_counter), True, 'white')

            pg.display.flip()
            self.clock.tick(60)

    def training_screen(self):
        self.main_values()
        training_running = True

        start_time = time.time()  # Start time initialization
        reset_time = time.time()  # Time of last interaction with digit squares

        self.user_input = []
        self.incorrect_square_number = None
        self.next_correct_digit = None  # Initially no digit highlighted

        self.max_display_digits = int(self.guessing_rect.width/37.53) # Number of digits visible in guessing_rect


        while training_running:
            self.screens_objects()
            self.screen.fill((39, 39, 39))  # Dark gray color

            # Time calculation
            self.time_to_hint = time.time() - reset_time
            self.training_elapsed_time = time.time() - start_time
            formatted_time = time.strftime('%M:%S', time.gmtime(self.training_elapsed_time))  # Time formatted to MM:SS

            # Time rendering
            time_text = self.calibri_72_font.render(f"{formatted_time}", True, 'white')
            time_rect = time_text.get_rect(center=(self.your_time_rect.centerx, self.your_time_rect.bottom + self.your_time_rect.height * 0.7))
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
            self.digit_number_text = self.calibri_55_font.render("Digit: " + f"{self.digit_counter + self.start_digit_counter-1}", True, 'white')

            self.guessed_digits_text_rect = guessed_digits_text.get_rect(center=(self.guessing_rect.right - self.digits_display_offset, self.guessing_rect.centery))
            self.base_text_rect = base_text.get_rect(center=(self.guessed_digits_text_rect.left - 25, self.guessing_rect.centery))
            self.digit_number_rect = self.digit_number_text.get_rect(
                center=(self.guessing_rect.centerx, self.guessing_rect.bottom + 0.4 * self.guessing_rect.height)
            )
            self.screen.blit(self.your_time_text, self.your_time_rect)

            if len(self.user_input) < self.max_display_digits-1:
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
            pg.draw.rect(self.screen, 'white', self.t_s_back_button_rect, 3)

            self.screen.blit(self.t_s_back_button_text, self.t_s_back_button_text_rect)

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
                self.incorrect_square_number = None

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
                    if self.t_s_back_button_rect.collidepoint(event.pos):
                        return
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
                        self.hint_counter = max(2, self.hint_counter - 1)
                    if self.switch_keys_layout_rect.collidepoint(event.pos):
                        self.keys_layout = 1 - self.keys_layout
                        self.screens_objects()

                    # Squares with digits
                    for i in range(10):
                        if getattr(self, f'square_{i}_rect').collidepoint(event.pos):
                            self.t_s_draw_digits(str(i))
                            reset_time = time.time()
                            self.next_correct_digit = None

            pg.display.flip()
            self.clock.tick(60)
    def t_s_draw_digits(self, user_input):
        pi_digits = self.read_pi_digits()[self.start_digit_counter-1:]
        pi_tokens = list(pi_digits.replace(".", ""))

        tested_digits = self.user_input + [user_input]
        tested_token = pi_tokens[:len(tested_digits)]


        correct = self.compare_tokens(tested_digits, tested_token)
        if correct:
            self.user_input.append(user_input)
            self.digit_counter += 1
            if len(self.user_input)>1 and len(self.user_input)<self.max_display_digits+1:
                self.digits_display_offset += 18.5

        else:
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
        pass

    def challenge_screen(self):
        challenge_running = True
        pass

if __name__ == '__main__':

    game = PiGame()
    game.main_screen()

# Zająć się challenge screenem
# Zaplanować jak ma wyglądać
# Zacząć coś pisać





