import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


def start_screen():
    with open('progress_lvl.txt', mode='r', encoding='UTF-8') as f:
        lvl = f.read()
        intro_text = ['Лабиринт', '', f'Уровень: {lvl}']
        if lvl == '1':
            fon = pygame.transform.scale(load_image('fon_green.jpg'), screen_size)
        elif lvl == '2':
            fon = pygame.transform.scale(load_image('fon_blue.jpg'), screen_size)
        elif lvl == '3':
            fon = pygame.transform.scale(load_image('fon_red.jpg'), screen_size)
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


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
                new_player = Player(x, y)
                level[y][x] = "."

            elif level[y][x] == '!':
                Tile('empty', x, y)
                Tile('final', x, y)
                level[y][x] = "#"
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            hero.move(x + 1, y)


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 60
player_image = load_image('person.png')
tile_width = tile_height = 50
player = None
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()

# заставка
start_screen()

# загрузка уровня
with open('progress_lvl.txt', mode='r', encoding='UTF-8') as f:
    extra = f.read()
    if extra == '1':
        level_map = load_level("map1.map")
        tile_images = {
            'wall': load_image('yellow_brick.png'),
            'empty': load_image('grass1.png'),
            'final': load_image('final.png')
        }
    elif extra == '2':
        level_map = load_level("map2.map")
        tile_images = {
            'wall': load_image('box.png'),
            'empty': load_image('floor.png'),
            'final': load_image('final.png')
        }
    elif extra == '3':
        level_map = load_level("map3.map")
        tile_images = {
            'wall': load_image('box.png'),
            'empty': load_image('grass.png'),
            'final': load_image('final.png')
        }

# создание карты
hero, max_x, max_y = generate_level(level_map)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # кнопки перемещения
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move(hero, "up")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move(hero, "down")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move(hero, "right")
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()