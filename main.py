import pygame

pygame.init()
pygame.font.init()
fontHeading = pygame.font.SysFont('Arial Black', 52)
fontIcon = pygame.font.SysFont('Arial', 32)
font = pygame.font.SysFont('Arial', 24)
background = pygame.image.load('assets/image/background.png')
defaultProfile = pygame.image.load('assets/default.jpg')

TITLE = "Bauernschach"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

WHITE = (255, 255, 255)
BORDER = (114, 74, 44)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)


def draw_board():
    rows = 8
    columns = 8

    square_size = 100

    leftover = SCREEN_HEIGHT - (columns * square_size)
    leftOverX = SCREEN_WIDTH - (rows * square_size)

    light_color = (196, 156, 126)
    dark_color = (114, 74, 44)
    contrast_color = (73, 47, 28)

    fieldWidth = columns * square_size
    fieldHeight = rows * square_size
    gap = 100

    widthScores = SCREEN_WIDTH - (fieldWidth + gap + leftover)

    screen.blit(background, (0, 0))

    for row in range(rows):
        for column in range(columns):
            x = column * square_size + leftover / 2
            y = row * square_size + leftover / 2

            if (row + column) % 2 == 0:
                color = light_color
            else:
                color = dark_color

            # if first or last row and column, draw a circle
            if (row == 0 or row == rows - 1) and (column == 0 or column == columns - 1):
                if(row == 0 and column == 0):
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size), border_top_left_radius=10)
                elif(row == 0 and column == columns - 1):
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size), border_top_right_radius=10)
                elif(row == rows - 1 and column == 0):
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size), border_bottom_left_radius=10)
                elif(row == rows - 1 and column == columns - 1):
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size), border_bottom_right_radius=10)

            else:
                pygame.draw.rect(screen, color, (x, y, square_size, square_size))

    yForText = leftover / 2 - 75

    render_text("Schwierigkeit: 69", leftover / 2,  column * square_size + leftover - 25, WHITE)
    render_text("Bauernschach", leftover / 2, yForText, WHITE, True)

    draw_current_score("22:32", contrast_color, leftover / 2 + fieldWidth + gap, leftover / 2, widthScores)
    draw_high_scores([{"username": "Alice", "score": 10},    {"username": "Bob", "score": 20},    {"username": "Charlie", "score": 15}], contrast_color, (81, 57, 40), leftover / 2 + fieldWidth + gap, leftover / 2 + gap * 2, widthScores)

    draw_help(rows*square_size + leftover / 2, yForText)
    draw_give_up(rows*square_size + leftover / 2 - 75, yForText)
    draw_user(rows*square_size + leftover / 2 + 200, yForText, "default") # geht nicht warum auch immer

def draw_current_score(score, color, x, y, width):
    render_text("Dein Score", x, y - 35, WHITE)
    pygame.draw.rect(screen, color, (x, y, width, 100), border_radius=10)
    render_text("Zeit: " + score, x + 20, y + 10, WHITE, True)


def draw_high_scores(scores, color, contrastColor, x, y, width):
    pygame.draw.rect(screen, color, (x, y, width, 600), border_radius=10)
    render_text("Highscores", x, y - 35, WHITE)

    for i in range(len(scores)):
        pygame.draw.rect(screen, contrastColor, (x + 5, y + i * 42 + 5, width - 10, 40), border_radius=10)
        render_text(scores[i]["username"] + ": " + str(scores[i]["score"]), x + 15, y + i * 42 + 9, WHITE)



def game_loop():
    screen.fill(WHITE)

    draw_board()

    pygame.display.flip()

    running = True

    while running:
        draw_board()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

def draw_user(x, y, name):
    radius = 26

    circle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    image_rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    image_scaled = pygame.transform.scale(defaultProfile, (radius * 2, radius * 2))
    circle_surf.blit(image_scaled, image_rect)

    mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(mask, BLACK, (x - radius, y + radius), radius)
    circle_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    screen.blit(circle_surf, (x - radius, y + radius))
    pygame.display.update()

def draw_help(x, y):
    radius = 26

    if pygame.draw.circle(screen, WHITE, (x - radius, y + radius), radius).collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, WHITE, (x - radius, y + radius), radius + 2)

    screen.blit(fontIcon.render("?", True, BLACK), (x - radius - 9, y + 7))

def draw_give_up(x, y):
    radius = 26

    RED = (255, 76, 79)

    if pygame.draw.circle(screen, RED, (x - radius, y + radius), radius).collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, RED, (x - radius, y + radius), radius + 2)

    screen.blit(fontIcon.render("A", True, BLACK), (x - radius - 11, y + 7))

def draw_help(x, y):
    radius = 26

    if pygame.draw.circle(screen, WHITE, (x - radius, y + radius), radius).collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, WHITE, (x - radius, y + radius), radius + 2)

    screen.blit(fontIcon.render("?", True, BLACK), (x - radius - 9, y + 7))


def render_text(text, x, y, color, heading=False):
    if heading:
        screen.blit(fontHeading.render(text, True, color), (x, y))
    else:
        screen.blit(font.render(text, True, color), (x, y))

game_loop()