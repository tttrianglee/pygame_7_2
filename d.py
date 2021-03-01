import pygame
import os
import sys

fps = 50
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Герой двигается"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png', -1)
tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = 0, 0, width, height


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos_x, self.pos_y = pos_x, pos_y

    def move(self, x, y):
        x *= (level[self.pos_y][self.pos_x + x] != '#')
        y *= (level[self.pos_y + y][self.pos_x] != '#')
        self.pos_x += x
        self.pos_y += y
        self.rect = self.rect.move(x * tile_width, y * tile_height)

    def update(self):
        old_x, old_y = self.pos_x, self.pos_y
        while self.pos_x >= level_x:
            self.pos_x -= 1
        while self.pos_x < 0:
            self.pos_x += 1
        while self.pos_y >= level_y:
            self.pos_y -= 1
        while self.pos_y < 0:
            self.pos_y += 1
        self.rect = self.rect.move((self.pos_x - old_x) * tile_width,
                                   (self.pos_y - old_y) * tile_height)


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                plx, ply = x, y
    new_player = Player(plx, ply)
    return new_player, x, y


try:
    level = load_level(input())
except FileNotFoundError:
    print('Произошла ошибка, вашей карты нет!')
    terminate()
player, level_x, level_y = generate_level(level)
running = True
pygame.display.set_caption('Перемещение героя. Дополнительные уровни.')
clock = pygame.time.Clock()
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1)
            if event.key == pygame.K_DOWN:
                player.move(0, 1)
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                player.move(1, 0)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
terminate()