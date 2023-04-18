import pygame

from MainMenu import MainMenu
from database import Database

pygame.init()
clock = pygame.time.Clock()  # Zeitgeber
FPS = 60  # Anzahl der Frames pro Sekunde

# SCREEN
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE10 = (230, 230, 230)
COLOR_BLACK90 = (25, 25, 25)
COLOR_BLACK80 = (50, 50, 50)
COLOR_BLACK85 = (60, 60, 60)
COLOR_GREEN = (144, 190, 109)
COLOR_ORANGE_1 = (248, 150, 30)
COLOR_ORANGE_2 = (243, 114, 44)
COLOR_RED = (249, 65, 68)

# IMAGES
IMAGE_BACKGROUND = pygame.image.load('assets/image/background.png')

# BUTTONS
buttons = []

# TEXT
pygame.font.init()
FONT_ARIAL_BLACK_32 = pygame.font.SysFont('Arial Black', 32)
FONT_ARIAL_BOLD_32 = pygame.font.SysFont('Arial Bold', 32)
FONT_ARIAL_BOLD_25 = pygame.font.SysFont('Arial Bold', 25)
FONT_ARIAL_REGULAR_20 = pygame.font.SysFont('Arial', 20)
FONT_ARIAL_REGULAR_12 = pygame.font.SysFont('Arial', 12)




class LoginScreen:

    def __init__(self):
        self.db = Database.getInstance()
        self.mainMenu = MainMenu()
        self.username = ''
        self.password = ''
        self.password_validation = ''
        self.username_input_active = False
        self.password_input_active = False
        self.password_validation_input_active = False


    def runLoginScreen(self):
        global username_input_active, password_input_active, button_password
        running = True
        clock.tick(FPS) # 60 FPS
        self.drawLoginScreen()


        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                # Button Click Event
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        # if clicked inside button bounds
                        if button['rect'].collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:

                                # show Register
                                if button['name'] == 'sel_register':
                                    self.drawRegisterScreen()

                                # show Login
                                if button['name'] == 'sel_login':
                                    self.drawErrorScreen('Dies ist ein Test-Error')
                                    # self.drawLoginScreen()

                                # activate username input
                                if button['name'] == 'input_username':
                                    print(button['name'])
                                    self.username_input_active = True
                                    pygame.draw.rect(SCREEN, COLOR_WHITE10, button['rect'])
                                    username_button_text = FONT_ARIAL_REGULAR_20.render(self.username, True,
                                                                                        COLOR_BLACK)
                                    SCREEN.blit(username_button_text,
                                                (button['rect'].x + 20, button['rect'].centery - (
                                                        username_button_text.get_height() / 2)))
                                    pygame.display.update()

                                # deactive username input
                                else:
                                    self.username_input_active = False
                                    print('username input false')

                                # activate password input
                                if button['name'] == 'input_password':
                                    print(button['name'])
                                    self.password_input_active = True
                                    pygame.draw.rect(SCREEN, COLOR_WHITE10, button['rect'])
                                    password_stars = ''
                                    for x in range(len(self.password)):
                                        password_stars += '*'
                                    password_button_text = FONT_ARIAL_REGULAR_20.render(password_stars, True,
                                                                                        COLOR_BLACK)
                                    SCREEN.blit(password_button_text,
                                                (button['rect'].x + 20, button['rect'].centery - (
                                                        password_button_text.get_height() / 2)))
                                    pygame.display.update()

                                # deactivate password input
                                else:
                                    self.password_input_active = False
                                    self.password = hash(self.password)

                                # activate password validation input
                                if button['name'] == 'input_password_validation':
                                    print(button['name'] + '1')
                                    self.password_validation_input_active = True
                                    pygame.draw.rect(SCREEN, COLOR_WHITE10, button['rect'])
                                    password_validation_stars = ''
                                    for x in range(len(self.password_validation)):
                                        password_validation_stars += '*'
                                    password_validation_button_text = FONT_ARIAL_REGULAR_20.render(password_validation_stars, True, COLOR_BLACK)
                                    SCREEN.blit(password_validation_button_text,
                                                (button['rect'].x + 20, button['rect'].centery - (
                                                        password_validation_button_text.get_height() / 2)))
                                    pygame.display.update()

                                # deactivate password validation input
                                else:
                                    self.password_validation_input_active = False
                                    self.password_validation = hash(self.password_validation)


                                # wants to register
                                # Im folgenden Props ersetzen durch die Benutzer-Eingabefelder
                                if button['name'] == 'REGISTER':
                                    print('try to register')
                                    if self.db.getPersonByUserName(self.username) is None:
                                        if self.password == self.password_validation:
                                            self.db.registerNewPerson(self.username, hash(self.password))
                                            playerIDCache = self.db.getPersonByUserName(self.username)
                                            userNameCache = self.username
                                        else:
                                            self.drawErrorScreen('Die eingegebenen Passwörter stimmen nicht überein.')
                                    else:
                                        self.drawErrorScreen('Username wird bereits verwendet.')

                                # wants to login
                                if button['name'] == 'LOGIN':
                                    print('try to log in')
                                    buttons.clear()
                                    self.mainMenu.runMenu()
                                    user = self.db.getPersonByUserNameWithPassword("usernameProp")
                                    if user[2] == hash("passwordProp"):
                                        playerIDCache = user[0]
                                        userNameCache = user[1]
                                        self.mainMenu.runMenu()
                                    else:
                                        self.drawErrorScreen('User existiert nicht, oder das Passwort stimmt nicht überein')

                                # guest login
                                if button['name'] == 'GUEST':
                                    print('log in as guest')
                                    playerIDCache = -1
                                    userNameCache = "Gast"

                                # close error message
                                if button['name'] == 'close_error':
                                    self.drawLoginScreen()

                # Keyboard Event
                elif event.type == pygame.KEYDOWN:

                    # if username input got clicked
                    if self.username_input_active:
                        button_username = None

                        # get username input button
                        for button in buttons:
                            if button['name'] == 'input_username':
                                button_username = button

                        # if Keyboard ENTER is pressed
                        if event.key == pygame.K_RETURN:
                            self.username = self.username

                        # if Keyboard RETURN is pressed
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]

                        # any other Keyboard input
                        else:
                            self.username += event.unicode

                        # update display for input
                        if button_username is not None:
                            pygame.draw.rect(SCREEN, COLOR_WHITE10, button_username['rect'])
                            username_button_text = FONT_ARIAL_REGULAR_20.render(self.username, True, COLOR_BLACK)
                            SCREEN.blit(username_button_text,
                                        (button_username['rect'].x + 20, button_username['rect'].centery - (
                                                username_button_text.get_height() / 2)))
                            pygame.display.update()

                    # if password input got clicked
                    elif self.password_input_active:
                        button_password = None
                        for button in buttons:

                            # get password input button
                            if button['name'] == 'input_password':
                                button_password = button

                        # if Keyboard ENTER is pressed
                        if event.key == pygame.K_RETURN:
                            self.password = self.password

                        # if Keyboard RETURN is pressed
                        elif event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]

                        # any other Keyboard input
                        else:
                            self.password += event.unicode

                        # update display for input
                        if button_password is not None:
                            pygame.draw.rect(SCREEN, COLOR_WHITE10, button_password['rect'])
                            password_stars = ''
                            for x in range(len(self.password)):
                                password_stars += '*'

                            password_button_text = FONT_ARIAL_REGULAR_20.render(password_stars, True, COLOR_BLACK)
                            SCREEN.blit(password_button_text,
                                        (button_password['rect'].x + 20, button_password['rect'].centery - (
                                                password_button_text.get_height() / 2)))
                            pygame.display.update()

                    # if password validation input got clicked
                    elif self.password_validation_input_active:
                        button_password_validation = None
                        for button in buttons:
                            if button['name'] == 'input_password_validation':
                                button_password_validation = button

                        # if Keyboard ENTER is pressed
                        if event.key == pygame.K_RETURN:
                            self.password_validation = self.password_validation

                        # if Keyboard RETURN is pressed
                        elif event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]

                        # any other Keyboard input
                        else:
                            self.password_validation += event.unicode

                        # update display for input
                        if button_password_validation is not None:
                            pygame.draw.rect(SCREEN, COLOR_WHITE10, button_password_validation['rect'])
                            password_validation_stars = ''
                            for x in range(len(self.password_validation)):
                                password_validation_stars += '*'

                            password_validation_button_text = FONT_ARIAL_REGULAR_20.render(password_validation_stars, True, COLOR_BLACK)
                            SCREEN.blit(password_validation_button_text, (button_password_validation['rect'].x + 20, button_password_validation['rect'].centery - (password_validation_button_text.get_height() / 2)))
                            pygame.display.update()



        pygame.quit()

    def drawLoginScreen(self):
        self.username = ''
        self.password = ''
        buttons.clear()
        # Hintergrundbild zeichnen
        SCREEN.blit(IMAGE_BACKGROUND, (0, 0))

        # login x320 y160 w440 h400
        login_screen = pygame.Surface.fill(SCREEN, COLOR_BLACK85, rect=(320, 160, 440, 400))

        # draw Register Button
        register_button_name = 'sel_register'
        register_button_text = FONT_ARIAL_BLACK_32.render('REGISTER', True, COLOR_WHITE)
        register_button_rect = pygame.Rect((login_screen.right - register_button_text.get_width() - 20), (login_screen.top + 15), register_button_text.get_width(), register_button_text.get_height())
        register_button_surf = pygame.draw.rect(SCREEN, COLOR_BLACK85, register_button_rect)
        register_button_dict = {'surface': register_button_surf, 'rect': register_button_rect, 'name': register_button_name}
        buttons.append(register_button_dict)
        SCREEN.blit(register_button_text, ((login_screen.right - register_button_text.get_width() - 20), (login_screen.top + 15)))

        # draw Login Text
        login_text = FONT_ARIAL_BLACK_32.render('LOGIN', True, COLOR_GREEN)
        SCREEN.blit(login_text, ((login_screen.left + 20), (login_screen.top + 15)))

        # draw spacer
        spacing_line = pygame.Surface.fill(SCREEN, COLOR_WHITE, rect=(
            login_screen.left + 25, (login_screen.top + 15 + login_text.get_height()) + 15, (login_screen.width - 50), 3
        ))

        # draw input fields
        username_input_background = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=((login_screen.left + 30), (spacing_line.bottom + 15), (login_screen.width - 60), 45))
        username_button_name = 'input_username'
        username_button_text = FONT_ARIAL_REGULAR_20.render('Username', True, COLOR_BLACK)
        username_button_rect = pygame.Rect(username_input_background.x, username_input_background.y, username_input_background.width, username_input_background.height)
        username_button_dict = {'surface': username_input_background, 'rect': username_button_rect, 'name': username_button_name}
        buttons.append(username_button_dict)
        SCREEN.blit(username_button_text, (username_input_background.x + 20, username_input_background.centery - (username_button_text.get_height() / 2)))

        password_input_background = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect = (
            username_input_background.x, (username_input_background.y + username_input_background.height + 15),
            username_input_background.width, username_input_background.height))
        password_button_name = 'input_password'
        password_button_text = FONT_ARIAL_REGULAR_20.render('Password', True, COLOR_BLACK)
        password_button_rect = pygame.Rect(password_input_background.x, password_input_background.y, password_input_background.width, password_input_background.height)
        password_button_dict = {'surface': password_input_background, 'rect': password_button_rect, 'name': password_button_name}
        buttons.append(password_button_dict)
        SCREEN.blit(password_button_text, (password_input_background.x + 20, password_input_background.centery - (password_button_text.get_height() / 2)))

        # draw GUEST button
        guest_button_name = 'GUEST'
        guest_button_text = FONT_ARIAL_BOLD_25.render('PLAY AS GUEST', True, COLOR_WHITE)
        guest_button_rect = pygame.Rect(username_input_background.x, (login_screen.bottom - username_input_background.height - 15), username_input_background.width, username_input_background.height)
        guest_button_surf = pygame.draw.rect(SCREEN, COLOR_ORANGE_1, guest_button_rect)
        guest_button_dict = {'surface': guest_button_surf, 'rect': guest_button_rect, 'name': guest_button_name}
        buttons.append(guest_button_dict)
        SCREEN.blit(guest_button_text, ((guest_button_rect.centerx - (guest_button_text.get_width() / 2)),
                                        guest_button_rect.centery - (guest_button_text.get_height() / 2)))

        # draw OR spacer
        spacing_or_line = pygame.Surface.fill(SCREEN, COLOR_WHITE, rect=(
            guest_button_rect.x, (guest_button_rect.top - 15), guest_button_rect.width, 3))
        spacing_or_text = FONT_ARIAL_REGULAR_12.render('OR', True, COLOR_WHITE)
        spacing_or_surf = pygame.Surface.fill(SCREEN, COLOR_BLACK85,
                                              rect=((spacing_or_line.centerx - 50), spacing_or_line.top, 100, 3))

        SCREEN.blit(spacing_or_text, ((spacing_or_line.centerx - (spacing_or_text.get_width() / 2),
                                       (spacing_or_line.centery - (spacing_or_text.get_height() / 2)))))

        # draw PLAY button
        play_button_name = 'LOGIN'
        play_button_text = FONT_ARIAL_BOLD_25.render('LOGIN', True, COLOR_WHITE)
        play_button_rect = pygame.Rect(guest_button_rect.x, (spacing_or_line.top - guest_button_rect.height - 15),
                                       guest_button_rect.width, guest_button_rect.height)
        play_button_surf = pygame.draw.rect(SCREEN, COLOR_GREEN, play_button_rect)
        play_button_dict = {'surface': play_button_surf, 'rect': play_button_rect, 'name': play_button_name}
        buttons.append(play_button_dict)
        SCREEN.blit(play_button_text, ((play_button_rect.centerx - (play_button_text.get_width() / 2)),
                                       play_button_rect.centery - (play_button_text.get_height() / 2)))

        pygame.display.update()

    def drawRegisterScreen(self):
        self.username = ''
        self.password = ''
        self.password_validation = ''
        buttons.clear()
        # Hintergrundbild zeichnen
        SCREEN.blit(IMAGE_BACKGROUND, (0, 0))

        # register x320 y120 w440 h480
        register_screen = pygame.Surface.fill(SCREEN, COLOR_BLACK85, rect=(320, 120, 440, 480))

        # draw Login Button
        login_button_name = 'sel_login'
        login_button_text = FONT_ARIAL_BLACK_32.render('LOGIN', True, COLOR_WHITE)
        login_button_rect = pygame.Rect((register_screen.left + 20),
                                           (register_screen.top + 15), login_button_text.get_width(),
                                           login_button_text.get_height())
        login_button_surf = pygame.draw.rect(SCREEN, COLOR_BLACK85, login_button_rect)
        login_button_dict = {'surface': login_button_surf, 'rect': login_button_rect, 'name': login_button_name}
        buttons.append(login_button_dict)
        SCREEN.blit(login_button_text, ((register_screen.left + 20), (register_screen.top + 15)))

        # draw Register Text
        register_text = FONT_ARIAL_BLACK_32.render('REGISTER', True, COLOR_GREEN)
        SCREEN.blit(register_text, ((register_screen.right - register_text.get_width() - 20), (register_screen.top + 15)))

        # draw spacer
        spacing_line = pygame.Surface.fill(SCREEN, COLOR_WHITE, rect=(
            register_screen.left + 25, (register_screen.top + 15 + register_text.get_height()) + 15, (register_screen.width - 50), 3
        ))

        # draw input fields
            # username
        username_input_background = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=(
        (register_screen.left + 30), (spacing_line.bottom + 15), (register_screen.width - 60), 45))
        username_button_name = 'input_username'
        username_button_text = FONT_ARIAL_REGULAR_20.render('Username', True, COLOR_BLACK)
        username_button_rect = pygame.Rect(username_input_background.x, username_input_background.y,
                                           username_input_background.width, username_input_background.height)
        username_button_dict = {'surface': username_input_background, 'rect': username_button_rect,
                                'name': username_button_name}
        buttons.append(username_button_dict)
        SCREEN.blit(username_button_text, (
        username_input_background.x + 20, username_input_background.centery - (username_button_text.get_height() / 2)))

            # password
        password_input_background = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=(
            username_input_background.x, (username_input_background.y + username_input_background.height + 15),
            username_input_background.width, username_input_background.height))
        password_button_name = 'input_password'
        password_button_text = FONT_ARIAL_REGULAR_20.render('Password', True, COLOR_BLACK)
        password_button_rect = pygame.Rect(password_input_background.x, password_input_background.y,
                                           password_input_background.width, password_input_background.height)
        password_button_dict = {'surface': password_input_background, 'rect': password_button_rect,
                                'name': password_button_name}
        buttons.append(password_button_dict)
        SCREEN.blit(password_button_text, (
        password_input_background.x + 20, password_input_background.centery - (password_button_text.get_height() / 2)))

            # validate password
        password_validation_input_background = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=(
            password_input_background.x, (password_input_background.y + password_input_background.height + 15),
            password_input_background.width, password_input_background.height))
        password_validation_button_name = 'input_password_validation'
        password_validation_button_text = FONT_ARIAL_REGULAR_20.render('Validate Password', True, COLOR_BLACK)
        password_validation_button_rect = pygame.Rect(password_validation_input_background.x, password_validation_input_background.y,
                                           password_validation_input_background.width, password_validation_input_background.height)
        password_validation_button_dict = {'surface': password_validation_input_background, 'rect': password_validation_button_rect,
                                'name': password_validation_button_name}
        buttons.append(password_validation_button_dict)
        SCREEN.blit(password_validation_button_text, (
            password_validation_input_background.x + 20,
            password_validation_input_background.centery - (password_validation_button_text.get_height() / 2)))


        # draw GUEST button
        guest_button_name = 'GUEST'
        guest_button_text = FONT_ARIAL_BOLD_25.render('PLAY AS GUEST', True, COLOR_WHITE)
        guest_button_rect = pygame.Rect(username_input_background.x, (register_screen.bottom - username_input_background.height - 15), username_input_background.width, username_input_background.height)
        guest_button_surf = pygame.draw.rect(SCREEN, COLOR_ORANGE_1, guest_button_rect)
        guest_button_dict = {'surface': guest_button_surf, 'rect': guest_button_rect, 'name': guest_button_name}
        buttons.append(guest_button_dict)
        SCREEN.blit(guest_button_text, ((guest_button_rect.centerx - (guest_button_text.get_width() / 2)),
                                        guest_button_rect.centery - (guest_button_text.get_height() / 2)))

        # draw OR spacer
        spacing_or_line = pygame.Surface.fill(SCREEN, COLOR_WHITE, rect=(
            guest_button_rect.x, (guest_button_rect.top - 15), guest_button_rect.width, 3))
        spacing_or_text = FONT_ARIAL_REGULAR_12.render('OR', True, COLOR_WHITE)
        spacing_or_surf = pygame.Surface.fill(SCREEN, COLOR_BLACK85,
                                              rect=((spacing_or_line.centerx - 50), spacing_or_line.top, 100, 3))

        SCREEN.blit(spacing_or_text, ((spacing_or_line.centerx - (spacing_or_text.get_width() / 2),
                                       (spacing_or_line.centery - (spacing_or_text.get_height() / 2)))))

        # draw PLAY button
        play_button_name = 'REGISTER'
        play_button_text = FONT_ARIAL_BOLD_25.render('REGISTER', True, COLOR_WHITE)
        play_button_rect = pygame.Rect(guest_button_rect.x, (spacing_or_line.top - guest_button_rect.height - 15),
                                       guest_button_rect.width, guest_button_rect.height)
        play_button_surf = pygame.draw.rect(SCREEN, COLOR_GREEN, play_button_rect)
        play_button_dict = {'surface': play_button_surf, 'rect': play_button_rect, 'name': play_button_name}
        buttons.append(play_button_dict)
        SCREEN.blit(play_button_text, ((play_button_rect.centerx - (play_button_text.get_width() / 2)),
                                       play_button_rect.centery - (play_button_text.get_height() / 2)))

        pygame.display.update()


    def drawErrorScreen(self, error_message: str):
        buttons.clear()
        # Hintergrundbild zeichnen
        SCREEN.blit(IMAGE_BACKGROUND, (0, 0))

        # error x320 y120 w440 h480
        error_screen = pygame.Surface.fill(SCREEN, COLOR_RED, rect=(320, 240, 440, 240))

        text_error = FONT_ARIAL_BOLD_32.render(error_message, True, COLOR_WHITE)
        SCREEN.blit(text_error, (error_screen.centerx - (text_error.get_width() / 2),
                                 error_screen.centery - (text_error.get_height() / 2)))

        # close error button
        close_button_size = 20
        close_button_rect = pygame.Rect(error_screen.right - close_button_size - 20, error_screen.top + 20, close_button_size, close_button_size)
        close_button_surf = pygame.draw.rect(SCREEN, (230, 230, 230), close_button_rect, border_radius=20, width=1)
        close_button_gradient = pygame.Surface((close_button_size, close_button_size)).convert_alpha()
        close_button_gradient.fill((0, 0, 0, 0))
        SCREEN.blit(close_button_gradient, close_button_surf)
        close_button_text = FONT_ARIAL_REGULAR_20.render('x', True, COLOR_WHITE)
        SCREEN.blit(close_button_text, ((close_button_rect.centerx - (close_button_text.get_width() / 2)),
                                        close_button_rect.centery - (close_button_text.get_height() / 2)))

        close_button_name = 'close_error'
        close_button_dict = {'surface': close_button_surf, 'rect': close_button_rect, 'name': close_button_name}
        buttons.append(close_button_dict)

        pygame.display.update()


login_screen = LoginScreen()
login_screen.runLoginScreen()
