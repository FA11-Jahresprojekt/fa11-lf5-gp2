'''''
 TODO: 
    - Higscores Dame
	- Benutzernamen kriegen und anzeigen
	- Spielvorschau Bilder
	- Logout Button
	- Game selected
	   - expand Spielvorschau Bild
	   - Schwierigkeitsgrad auswählen (ausgewählten hervorheben)
	   - Spielhistorie
	   - Bisherige Statistiken
	- Highscore Image / Layout
	   - Eigenen Score anzeigen
'''''

import pygame

import Bauernschach
from database import Database

pygame.init()
clock = pygame.time.Clock()  # Zeitgeber
FPS = 60  # Anzahl der Frames pro Sekunde

# SCREEN
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# IMAGES
IMAGE_BACKGROUND = pygame.image.load('assets/image/background.png')
IMAGE_HIGHSCORES = pygame.image.load('assets/image/leaderboard_background_240x480.png')
IMAGE_HIGHSCORES_PLAYER_BACKGROUND = pygame.image.load('assets/image/leaderboard_player-background_240x365.png')
IMAGE_USER = pygame.image.load('assets/image/profile_default.png')

# BUTTONS
buttons = []

## Button Liste mit allen Buttons
## - Wenn Overlay aufgerufen wird, müssen die Buttons deaktiviert werden
## name, rect, active

# TEXT
pygame.font.init()
FONT_ARIAL_BLACK_32 = pygame.font.SysFont('Arial Black', 32)
FONT_ARIAL_BOLD_32 = pygame.font.SysFont('Arial Bold', 32)
FONT_ARIAL_BOLD_25 = pygame.font.SysFont('Arial Bold', 25)
FONT_ARIAL_REGULAR_20 = pygame.font.SysFont('Arial', 20)
FONT_ARIAL_REGULAR_12 = pygame.font.SysFont('Arial', 12)

# COLORS
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE10 = (230, 230, 230)
COLOR_BLACK90 = (25, 25, 25)
COLOR_BLACK80 = (50, 50, 50)


class MainMenu:

    def __init__(self):
        self.db = Database.getInstance()

    def runMenu(self):
        running = True
        clock.tick(FPS)  # 60 FPS
        self.drawMainMenu()

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Button Click
                    for button in buttons:
                        if button['rect'].collidepoint(pygame.mouse.get_pos()):
                            if pygame.mouse.get_pressed()[0]:

                                # Highscores
                                if button['name'].startswith('bauernschach_difficulty'):
                                    difficulty = int(button['name'].split("_")[2])
                                    self.updateHighscoreBauernschach(difficulty, 10)
                                if button['name'].startswith('dame_difficulty'):
                                    difficulty = int(button.name.split("_")[1])
                                    self.updateHighscoreDame(difficulty, 10)

                                # Game selection
                                if button['name'].startswith('game_selection'):
                                    if button['name'].endswith('bauernschach'):
                                        self.gameSelectedBauernschach(3)
                                    if button['name'].endswith('dame'):
                                        self.gameSelectedDame(3)

                                if button['name'].startswith('bauernschach_game_start'):
                                    Bauernschach.game_loop()

                                # Back to Main Menu
                                if button['name'] == 'to_mainmenu':
                                    buttons.clear()  # clear button list to avoid stacking them
                                    self.drawMainMenu()

        pygame.quit()

    def drawMainMenu(self):
        # Hintergrundbild zeichnen
        SCREEN.blit(IMAGE_BACKGROUND, (0, 0))

        # Rest des Menüs zeichnen und aktualisieren
        self.drawHeader('Spielesammlung')
        self.drawGameBauernschach()
        self.drawGameDame()
        self.drawHighscores()
        pygame.display.update()

    def drawHeader(self, title):
        headline_text = FONT_ARIAL_BLACK_32.render(title, True, COLOR_WHITE)
        pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(0, 0, 1080, 60))
        pygame.Surface.fill(SCREEN, COLOR_BLACK80, rect=(0, 60, 1080, 3))
        SCREEN.blit(headline_text, (80, 5))
        self.show_user('Achim')

    def drawGameBauernschach(self):
        posX_bauernschach = 80
        posY_bauernschach = 160
        width_bauernschach = 320
        height_bauernschach = 220

        button_rect = pygame.Rect(posX_bauernschach, posY_bauernschach, width_bauernschach, height_bauernschach)
        button = pygame.draw.rect(SCREEN, COLOR_WHITE10, button_rect)
        button_name = 'game_selection_bauernschach'
        button_dict = {'surface': button, 'rect': button_rect, 'name': button_name}
        buttons.append(button_dict)

        text_placeholder = FONT_ARIAL_REGULAR_20.render('Bauernschach', True, COLOR_BLACK90)
        SCREEN.blit(text_placeholder, (120, 180))

    def drawGameDame(self):
        pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=(80, 420, 320, 220))
        text_placeholder = FONT_ARIAL_REGULAR_20.render('Spielvorschau', True, COLOR_BLACK90)
        SCREEN.blit(text_placeholder, (120, 440))

    def drawHighscores(self):
        self.drawHighscoreDame()
        self.drawHighscoreBauernschach(3, 10)

    def drawHighscoreDame(self):
        # position: x760, y160    # size: 240x480
        SCREEN.blit(IMAGE_HIGHSCORES, (760, 160))
        text_headline_highscore_2 = FONT_ARIAL_BOLD_32.render('Dame', True, COLOR_WHITE)
        SCREEN.blit(text_headline_highscore_2, (760, 120))

    def updateHighscoreDame(self, difficulty_int, player_count_int):
        print(f'updated Highscore Dame - difficulty {difficulty_int}')
        print()

    def drawHighscoreBauernschach(self, difficulty_int, player_count_int):
        """""
        Draws the Highscore Liste for "Bauernschach"

        Args:
            difficulty_int (int)
            player_count_int (int): Top numbers of players to return

        Returns:
            top [playerCount] players in [gameType] at [difficulty]
        """""

        highscore_posX = 480
        highscore_posY = 160
        width = 240
        height = 480

        # Background
        backgroundImage = SCREEN.blit(IMAGE_HIGHSCORES, (highscore_posX, highscore_posY))

        # Headline
        text_game_name = FONT_ARIAL_BOLD_32.render('Bauernschach', True, COLOR_WHITE)
        SCREEN.blit(text_game_name, (highscore_posX, (highscore_posY - 40)))

        # Inside Screen
        text_highscore = FONT_ARIAL_BOLD_32.render('HIGHSCORES', True, COLOR_WHITE10)
        SCREEN.blit(text_highscore,
                    (((width - text_highscore.get_width()) / 2) + highscore_posX, (highscore_posY + 20)))  # centered

        # Title
        title_y = 260
        text_title_pos = FONT_ARIAL_BOLD_25.render('POS', True, COLOR_WHITE10)
        text_title_name = FONT_ARIAL_BOLD_25.render('NAME', True, COLOR_WHITE10)
        text_title_score = FONT_ARIAL_BOLD_25.render('SCORE', True, COLOR_WHITE10)
        title_width = (text_title_pos.get_width() + text_title_name.get_width() + text_title_score.get_width())
        spacing_width = (width - title_width) / 4

        SCREEN.blit(text_title_pos, ((highscore_posX + spacing_width), title_y))
        SCREEN.blit(text_title_name,
                    (highscore_posX + spacing_width + text_title_pos.get_width() + spacing_width, title_y))
        SCREEN.blit(text_title_score, (
            highscore_posX + spacing_width + text_title_pos.get_width() + spacing_width + text_title_name.get_width() + spacing_width,
            title_y))

        # difficulty Buttons
        button_x = highscore_posX + 20
        button_y = 10
        button_width = (((width - 40) - 40) / 5)
        button_height = 30
        button_spacing = 10
        difficulty = 5
        for i in range(difficulty):
            button_x = highscore_posX + 20 + i * (button_width + button_spacing)
            button_y = highscore_posY + 50
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # draw button border
            button = pygame.draw.rect(SCREEN, (230, 230, 230), button_rect, border_radius=15, width=3)

            # draw button background
            gradient = pygame.Surface((button_width, button_height)).convert_alpha()
            gradient.fill((0, 0, 0, 0))
            pygame.draw.rect(gradient, (255, 255, 255, 50), gradient.get_rect(), border_radius=15)
            pygame.draw.rect(gradient, (255, 255, 255, 30), gradient.get_rect().inflate(-5, -5), border_radius=15)
            SCREEN.blit(gradient, button_rect)

            button_name = f'bauernschach_difficulty_{i + 1}'
            button_dict = {'surface': button, 'rect': button_rect, 'name': button_name}
            buttons.append(button_dict)

            # draw button text
            text = FONT_ARIAL_BOLD_32.render(str(i + 1), True, COLOR_WHITE10)
            text_rect = text.get_rect(center=button_rect.center)
            SCREEN.blit(text, text_rect)

            print(f'{i}. button created')

        self.updateHighscoreBauernschach(5, 10)

    def updateHighscoreBauernschach(self, difficulty_int, player_count_int):
        # Get top 10 players for Bauernschach difficulty level 3
        players = self.getHighscores("Bauernschach", difficulty_int, player_count_int)

        title_y = 260
        highscore_posX = 480
        player_rank_x = 510  # x Position for player rank
        player_name_x = 560  # x Position for first player name
        player_score_x = 670  # x Position for first player score
        player_rank_y = title_y + 30  # y Position

        # Background
        backgroundImage = SCREEN.blit(IMAGE_HIGHSCORES_PLAYER_BACKGROUND, (highscore_posX, (title_y + 15)))

        # Draw each player name and score
        for i, player in enumerate(players):
            player_rank = f"{i + 1}. "
            player_name = str(player[1])
            games_won = str(player[4])

            # Render player name and score
            player_rank_text = FONT_ARIAL_REGULAR_20.render(str(player_rank), True, COLOR_WHITE)
            player_name_text = FONT_ARIAL_REGULAR_20.render(str(player_name), True, COLOR_WHITE)
            player_score_text = FONT_ARIAL_REGULAR_20.render(str(games_won), True, COLOR_WHITE)

            # Blit player name and score to screen
            SCREEN.blit(player_rank_text, (player_rank_x, player_rank_y))
            SCREEN.blit(player_name_text, (player_name_x, player_rank_y))
            SCREEN.blit(player_score_text, (player_score_x, player_rank_y))

            # Increment y position for next player
            player_rank_y += 30

        pygame.display.update()
        print(f'{len(players)} highscore players found for difficulty {difficulty_int}')
        print(f'highscore difficulty {difficulty_int} updated')
        print()

    def getHighscores(self, game_type, difficulty, player_count):
        """"
        Get current Highscores for top [playerCount] players in [gameType] at [difficulty]

        Args:
            game_type (string)
            difficulty (int)
            player_count (int): Top numbers of players to return

        Returns:
            top [playerCount] players in [gameType] at [difficulty]
        """

        bestPlayers = self.db.getTopPlayersForGameAndDifficulty(game_type, difficulty, player_count)
        return bestPlayers

    def show_user(self, username):
        # Load and scale profile image
        profile_image = IMAGE_USER.convert_alpha()
        profile_image_scaled = pygame.transform.smoothscale(profile_image, (30, 30))
        profile_image_pos_y = 15
        username_text = FONT_ARIAL_REGULAR_20.render(username, True, COLOR_WHITE)
        username_pos_x = 1000 - username_text.get_width()  # username_pos_x = profile_image_pos_x + 30 + 10
        username_pos_y = profile_image_pos_y + (
                (profile_image_scaled.get_height() / 2) - (username_text.get_height() / 2))
        profile_image_pos_x = username_pos_x - 20 - profile_image.get_width()

        # Create circular mask for profile image
        mask_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (15, 15), 15)

        # Apply mask to profile image
        masked_profile_image = profile_image_scaled.copy()
        masked_profile_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw
        SCREEN.blit(masked_profile_image, (profile_image_pos_x, profile_image_pos_y))
        SCREEN.blit(username_text, (username_pos_x, username_pos_y))

    def drawBackToMainMenuButton(self):
        # Back to Main Menu Button
        mainmenu_button_x = 20
        mainmenu_button_y = 15
        mainmenu_button_width = 30
        mainmenu_button_height = 30

        button_to_mainmenu_rect = pygame.Rect(mainmenu_button_x, mainmenu_button_y, mainmenu_button_width,
                                              mainmenu_button_height)
        button_to_mainmenu = pygame.draw.rect(SCREEN, (230, 230, 230), button_to_mainmenu_rect, border_radius=10,
                                              width=3)
        gradient = pygame.Surface((mainmenu_button_width, mainmenu_button_height)).convert_alpha()
        gradient.fill((0, 0, 0, 0))
        SCREEN.blit(gradient, button_to_mainmenu)
        text_to_mainmenu = FONT_ARIAL_REGULAR_20.render('<', True, COLOR_WHITE)
        SCREEN.blit(text_to_mainmenu, ((button_to_mainmenu_rect.centerx - (text_to_mainmenu.get_width() / 2)),
                                       (button_to_mainmenu_rect.centery - (text_to_mainmenu.get_height() / 2))))

        button_to_mainmenu_name = 'to_mainmenu'
        button_dict = {'surface': button_to_mainmenu, 'rect': button_to_mainmenu_rect, 'name': button_to_mainmenu_name}
        buttons.append(button_dict)

        pygame.display.update()

    def gameSelectedBauernschach(self, difficulty):
        # x80 y80 w920 h560
        print('Game selected Bauernschach')
        print()
        buttons.clear()

        # Background
        background_screen = pygame.Surface.fill(SCREEN, COLOR_WHITE10, rect=(80, 80, 920, 560))

        # Game Image
        image_game = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(160, 120, 200, 200))
        text_game_image = FONT_ARIAL_BOLD_32.render('Game Image', True, COLOR_WHITE)
        SCREEN.blit(text_game_image, (image_game.centerx - (text_game_image.get_width() / 2),
                                      image_game.centery - (text_game_image.get_height() / 2)))

        # Game Text
        self.drawHeader('Bauernschach')
        self.drawBackToMainMenuButton()

        # Player stats
        game_history = self.db.getGameHistoryForChosenPlayer(1)

        # calculate stats based on game history
        total_games_played = len(game_history)
        total_games_won = sum(1 for game in game_history if game[2] == "won")
        total_games_lost = sum(1 for game in game_history if game[2] == "lost")
        total_games_canceled = sum(1 for game in game_history if game[2] == "cancelled")
        total_pawns_destroyed = sum(game[3] for game in game_history)


        # Games played
        games_played_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=((image_game.right + 20), (image_game.bottom - 80), 80, 80))
        text_title_games_played = FONT_ARIAL_REGULAR_12.render('games played', True, COLOR_WHITE)
        SCREEN.blit(text_title_games_played, (games_played_background.centerx - (text_title_games_played.get_width() / 2), games_played_background.top + 10))

        text_value_games_played = FONT_ARIAL_BOLD_32.render(str(total_games_played), True, COLOR_WHITE10)
        SCREEN.blit(text_value_games_played, (games_played_background.centerx - (text_value_games_played.get_width() / 2),
                                              games_played_background.centery - (text_value_games_played.get_height() / 2) + 5))


        # Games won
        games_won_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(
            (games_played_background.right + 10), games_played_background.top, games_played_background.width, games_played_background.height))
        text_games_won = FONT_ARIAL_REGULAR_12.render('games won', True, COLOR_WHITE)
        SCREEN.blit(text_games_won, (games_won_background.centerx - (text_games_won.get_width() / 2), games_won_background.top + 10))

        text_value_games_won = FONT_ARIAL_BOLD_32.render(str(total_games_won), True, COLOR_WHITE10)
        SCREEN.blit(text_value_games_won,(games_won_background.centerx - (text_value_games_won.get_width() / 2),
                                             games_won_background.centery - (text_value_games_won.get_height() / 2) + 5))

        # Games lost
        games_lost_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(
            (games_won_background.right + 10), games_won_background.top, games_won_background.width, games_won_background.height))
        text_games_lost = FONT_ARIAL_REGULAR_12.render('games lost', True, COLOR_WHITE)
        SCREEN.blit(text_games_lost, (games_lost_background.centerx - (text_games_lost.get_width() / 2),
                                      games_lost_background.top + 10))

        text_value_games_lost = FONT_ARIAL_BOLD_32.render(str(total_games_lost), True, COLOR_WHITE10)
        SCREEN.blit(text_value_games_lost, (games_lost_background.centerx - (text_value_games_lost.get_width() / 2),
                                           games_lost_background.centery - (text_value_games_lost.get_height() / 2) + 5))

        # Games canceled
        games_canceled_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(
            (games_lost_background.right + 10), games_lost_background.top, games_lost_background.width, games_lost_background.height))
        text_games_canceled = FONT_ARIAL_REGULAR_12.render('games canceled', True, COLOR_WHITE)
        SCREEN.blit(text_games_canceled, (games_canceled_background.centerx - (text_games_canceled.get_width() / 2),
                                          games_canceled_background.top + 10))

        text_value_games_canceled = FONT_ARIAL_BOLD_32.render(str(total_games_canceled), True, COLOR_WHITE10)
        SCREEN.blit(text_value_games_canceled, (games_canceled_background.centerx - (text_value_games_canceled.get_width() / 2),
                                            games_canceled_background.centery - (text_value_games_canceled.get_height() / 2) + 5))

        # Pawns destroyed total_pawns_destroyed
        pawns_destroyed_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(
            (games_canceled_background.right + 10), games_canceled_background.top, games_canceled_background.width,
            games_canceled_background.height))  # Pawns destroyed
        text_pawns = FONT_ARIAL_REGULAR_12.render('pawns destroyed', True, COLOR_WHITE)
        SCREEN.blit(text_pawns, (pawns_destroyed_background.centerx - (text_pawns.get_width() / 2),
                                 pawns_destroyed_background.top + 10))

        text_value_pawns_destroyed = FONT_ARIAL_BOLD_32.render(str(total_pawns_destroyed), True, COLOR_WHITE10)
        SCREEN.blit(text_value_pawns_destroyed,(pawns_destroyed_background.centerx - (text_value_pawns_destroyed.get_width() / 2),
                                               pawns_destroyed_background.centery - (text_value_pawns_destroyed.get_height() / 2) + 5))

        button_difficulty_x = image_game.right + 10
        button_difficulty_y = games_played_background.top - 90
        button_difficulty_width = games_played_background.width
        button_difficulty_height = games_played_background.height
        button_difficulty_spacing = 10
        difficulty = 5
        for i in range(difficulty):
            button_difficulty_x += button_difficulty_spacing
            button_difficulty_rect = pygame.Rect(button_difficulty_x, button_difficulty_y, button_difficulty_width, button_difficulty_height)
            button_difficulty = pygame.draw.rect(SCREEN, COLOR_BLACK90, button_difficulty_rect)
            button_difficulty_name = f'game-preview_bauernschach_game-history_{i + 1}'
            button_dict = {'surface': button_difficulty, 'rect': button_difficulty_rect, 'name': button_difficulty_name}
            buttons.append(button_dict)

            text_button_difficulty = FONT_ARIAL_BOLD_32.render(f'{i + 1}', True, COLOR_WHITE)
            SCREEN.blit(text_button_difficulty, (button_difficulty.centerx - (text_button_difficulty.get_width() / 2),
                                                 (button_difficulty.centery - (text_button_difficulty.get_height() / 2))))
            button_difficulty_x += button_difficulty_width

        # title
        text_difficulty = FONT_ARIAL_BOLD_32.render('Schwierigkeitsgrad', True, COLOR_BLACK)
        SCREEN.blit(text_difficulty, (image_game.right + (button_difficulty_spacing * 2), image_game.top))

        # Game History
        game_history_background = pygame.Surface.fill(SCREEN, COLOR_BLACK, rect=(160, 340, 760, 260))
        text_game_history = FONT_ARIAL_BOLD_32.render('Game History', True, COLOR_WHITE)
        SCREEN.blit(text_game_history, (game_history_background.centerx - (text_game_history.get_width() / 2),
                                        game_history_background.centery - (text_game_history.get_height() / 2)))

        # Start Game
        footer_background = pygame.Surface.fill(SCREEN, COLOR_BLACK90, rect=(0, 620, 1080, 100))
        text_game_start = FONT_ARIAL_BOLD_32.render('Spiel starten >', True, COLOR_WHITE)
        SCREEN.blit(text_game_start, ((footer_background.centerx - (text_game_start.get_width() / 2)),
                                      (footer_background.centery - (text_game_start.get_height() / 2))))
        # draw button border
        game_start_button_rect = pygame.Rect(footer_background.centerx - (text_game_start.get_width() / 2),
                                             footer_background.centery - (text_game_start.get_height() / 2),
                                             text_game_start.get_width(), text_game_start.get_height())
        button_name = f'bauernschach_game_start'
        button_dict = {'surface': text_game_start, 'rect': game_start_button_rect, 'name': button_name}
        buttons.append(button_dict)

        pygame.display.update()


    def gameSelectedDame(self, difficulty):
        print('Game selected Dame')
        print()


main_menu = MainMenu()
main_menu.runMenu()

'''
    def start_game(self, game_name):
        # Methode zum Starten des ausgewählten Spiels

    def update_user(self, username):
        self.user = username    
'''
