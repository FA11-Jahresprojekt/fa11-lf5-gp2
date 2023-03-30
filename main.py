# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()

surface = pygame.Surface
fill = surface.fill # (x, y, widht, height)

# Screen
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load('assets/image/background.png')
highscores = pygame.image.load('assets/image/highscores.png')
user_image = pygame.image.load('assets/image/user_image.png')

# Colors
white = (255, 255, 255)
white10p = (230, 230, 230)
black90p = (25, 25, 25)

#Text
font_heading = pygame.font.SysFont('Arial Black', 32)
font_sub_head = pygame.font.SysFont('Arial Bold', 32)
font_regular = pygame.font.SysFont('Arial', 12)


clock = pygame.time.Clock()
running = True

def draw_game_1():
    fill(screen, white10p, rect=(80, 160, 320, 220))
    text_placeholder = font_regular.render('Spielvorschau', True, black90p)
    screen.blit(text_placeholder, (120, 180))

def draw_game_2():
    fill(screen, white10p, rect=(80, 420, 320, 220))
    text_placeholder = font_regular.render('Spielvorschau', True, black90p)
    screen.blit(text_placeholder, (120, 440))

def draw_highscore1():
    # fill(screen, white10p, rect=(480, 160, 240, 480))  # Highscore 1
    screen.blit(highscores, (480, 160))
    text_headline_highscore_1 = font_sub_head.render('Dame', True, white)
    screen.blit(text_headline_highscore_1, (480, 120))

def draw_highscore2():
    # fill(screen, white10p, rect=(760, 160, 240, 480)) # Highscore 2
    screen.blit(highscores, (760, 160))
    text_headline_highscore_2 = font_sub_head.render('Bauernschach', True, white)
    screen.blit(text_headline_highscore_2, (760, 120))

def draw_highscores():
    draw_highscore1()
    draw_highscore2()


def draw_user(user_image, user_name, user_profile_url):
    # Set the circle's radius and center coordinates
    radius = 14
    center = (890, 90)

    # Create a new surface to draw the circle and image on
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    # Draw the circle on the surface
    pygame.draw.circle(surface, black90p, (radius, radius), radius)

    # Scale the user's image to fit inside the circle
    image = pygame.transform.scale(user_image, (radius * 2 - 2, radius * 2 - 2))

    # Blit the user's image onto the surface, using the circle as a mask
    surface.blit(image, (1, 1), special_flags=pygame.BLEND_RGBA_MULT)

    # Blit the surface onto the main screen, at the center position
    screen.blit(surface, (center[0] - radius, center[1] - radius))

    # Create a new text surface for the user's name
    text_username = font_regular.render(user_name, True, white)

    # Blit the text surface onto the main screen, next to the circle
    screen.blit(text_username, (910, 90))

    # Calculate the rectangle's position based on the circle and text positions
    rect_username = pygame.Rect(
        (center[0] - radius + 30, center[1] - radius, text_username.get_width(), text_username.get_height()))

    # Add the user's information to a dictionary
    user_info = {
        'name': user_name,
        'profile_url': user_profile_url,
        'rect_username': rect_username
    }

    # Update the Pygame window
    pygame.display.update()

    # Return the user's information
    return user_info


def draw_login():
    loginField = fill(screen, white10p, rect=(545, 120, 240, 430))
    loginText = font_regular.render('Login', True, white)
    screen.blit(loginText, (545, 70))

def draw_guest_login():
    fill(screen, white10p, rect=(545, 560, 240, 60))  # Gast Login


while running:

    # fill the screen with a color to wipe away anything from last frame
    fill(screen, black90p)
    screen.blit(background, (0, 0))
        # fill(screen, black90p, rect=(440, 80, 3, 560))  # Trennstrich

    headline_text = font_heading.render('Spielesammlung', True, white)
    screen.blit(headline_text, (80, 60))

    # RENDER YOUR GAME HERE
    draw_game_1()
    draw_game_2()
    # draw_login()
    # draw_guest_login()
    draw_highscores()

    user_info = draw_user(user_image, 'Achim', 'test/url')
    user_name = user_info['name']
    rect_username = user_info['rect_username']
    profile_url = user_info['profile_url']

    # Create a dictionary of user information
    users = {user_name: user_info}

    # Draw a user and add their information to the dictionary

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.MOUSEBUTTONDOWN:

        ## FUNKTIONIERT NOCH NICHT ##
        # Check if the mouse click was on a username text rectangle
        for user_info in users.values():
            if user_info['rect_username'].collidepoint(pygame.mouse.get_pos()):
                # Direct the user to the profile URL here
                print('Clicked on username:', user_info['name'], 'profile URL:', user_info['profile_url'])
        ## --- --- --- --- --- --- ##

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()