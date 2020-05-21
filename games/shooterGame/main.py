# Pygame template - skeleton for a new pygame project
from __future__ import annotations
import pygame
from pygame import sprite, image, Surface, mixer, Rect
import random
from dataclasses import dataclass
from pathlib import Path

from typing import Dict, Tuple, List
from typing import Any, ClassVar
from typing_extensions import Final as Fin, Literal as Lit

curr_dir = Path.cwd()
img_dir = curr_dir / 'img'
snd_dir = curr_dir / 'snd'

WIDTH: Fin[int] = 480
HEIGHT: Fin[int] = 600
FPS: Fin[int] = 60

# define colorstbh

_colorT = Tuple[int, int, int]


@dataclass
class color():
    WHITE: ClassVar[_colorT] = (255, 255, 255)
    BLACK: ClassVar[_colorT] = (0, 0, 0)
    RED: ClassVar[_colorT] = (255, 0, 0)
    ORANGE: ClassVar[_colorT] = (255, 125, 0)
    YELLOW: ClassVar[_colorT] = (255, 255, 0)
    GREEN: ClassVar[_colorT] = (0, 255, 0)
    D_GREEN: ClassVar[_colorT] = (65, 155, 125)
    BLUE: ClassVar[_colorT] = (0, 0, 255)


def draw_text(surf: Surface,
              # /,  # py3.8
              text: str,
              size: int,
              x: int,
              y: int,
              font_name: str = 'arial',
              color: _colorT = color.YELLOW,
              ) -> None:
    font_name_match = pygame.font.match_font(font_name)
    font = pygame.font.Font(font_name_match, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob() -> None:
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf: Surface,
                    x: int,
                    y: int,
                    pct: float,
                    *,
                    colors: Tuple[_colorT, _colorT, _colorT, _colorT, _colorT] = (color.D_GREEN, color.GREEN, color.YELLOW, color.ORANGE, color.RED),
                    outline: _colorT = color.WHITE,
                    ) -> None:
    color_full = colors[0]
    color_empty = colors[-1]
    other_colors: Tuple[_colorT, _colorT, _colorT] = colors[1:4]

    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH

    BAR_FULL = BAR_LENGTH
    BAR_NEARFULL = BAR_LENGTH * 0.8
    BAR_HALF = BAR_LENGTH * 0.5
    BAR_EMPTY = BAR_LENGTH * 0.2

    if fill >= BAR_FULL:
        color = color_full
    elif BAR_NEARFULL <= fill < BAR_FULL:
        color = other_colors[0]
    elif BAR_HALF <= fill < BAR_NEARFULL:
        color = other_colors[1]
    elif BAR_EMPTY <= fill < BAR_HALF:
        color = other_colors[2]
    elif fill < BAR_EMPTY:
        color = color_empty

    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, outline, outline_rect, 2)


def draw_lives(surf: Surface, x: int, y: int, lives: int, img: Surface) -> None:
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# initialize pygame and create window
pygame.init()
mixer.init()
screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock: pygame.time.Clock = pygame.time.Clock()


class Player(sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(color.GREEN)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(color.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, color.RED, self.rect.center, self.radius)

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10  # 10 px away from bottom
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.hidden = False
        self.shield = 100.0
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.hide_timer = pygame.time.get_ticks()

    def update(self) -> None:
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0  # if not set, continuous move
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.shoot()
        elif keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8
        elif keystate[pygame.K_UP]:
            self.speedy = -4
        elif keystate[pygame.K_DOWN]:
            self.speedy = 4

        self.rect.x += self.speedx

        if self.rect.y <= HEIGHT - 10:
            self.rect.y += self.speedy
        else:
            self.rect.y = HEIGHT - 10

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self) -> None:
        # global bullets
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self) -> None:
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # self.image = meteor_img
        # self.image.set_colorkey(color.BLACK)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(color.BLACK)
        self.image = self.image_orig.copy()
        self.rect: Rect = self.image.get_rect()
        # self.image = pygame.Surface((30, 40))
        # self.image.fill(color.RED)
        self.radius: int = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, color.RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self) -> None:
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)


class Bullet(sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(color.YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(color.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self) -> None:
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center: Tuple[int, int], size: Lit['sm', 'med', 'lg', 'player']) -> None:
        super().__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all game graphics
background = image.load(str(img_dir / "starfield.png")).convert()
background_rect = background.get_rect()

player_img: Surface = image.load(str(img_dir / "plyrShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(color.BLACK)
bullet_img: Surface = image.load(str(img_dir / "laserRed16.png")).convert()

meteor_fnl = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
              'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
meteor_images = [image.load(str(img_dir / fn)).convert() for fn in meteor_fnl]

explosion_anim: Dict[str, List[Surface]] = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(str(img_dir / filename)).convert()
    img.set_colorkey(color.BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    img.set_colorkey(color.BLACK)

    filename2 = 'sonicExplosion0{}.png'.format(i)
    img2 = pygame.image.load(str(img_dir / filename2)).convert()
    img2.set_colorkey(color.BLACK)
    explosion_anim['player'].append(img2)

# Load all game sounds
shoot_sound = mixer.Sound(str(snd_dir / 'pew.wav'))
player_die_sound = mixer.Sound(str(snd_dir / 'rumble1.ogg'))
expl_sounds_fnl = ['expl3.wav', 'expl6.wav']
expl_sounds = [mixer.Sound(str(snd_dir / fn)) for fn in expl_sounds_fnl]
mixer.music.load(str(snd_dir / 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
mixer.music.set_volume(0.4)

# create sprite groups
all_sprites = sprite.Group()
mobs = sprite.Group()
bullets = sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(8):
    newmob()


# Game loop
pygame.mixer.music.play(loops=-1)
score = 0
running = True
died_countdown = []
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    bullet_hits: Dict[Mob, List[Bullet]] = sprite.groupcollide(mobs, bullets, True, True)
    for hit in bullet_hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # check to see if a mob hit the player
    mob_hits: List[Mob] = sprite.spritecollide(player, mobs, False, sprite.collide_circle)
    for hit in mob_hits:
        player.shield -= hit.radius * 0.1
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if the player died and the explosion has finished playing

    # Draw / render
    screen.fill(color.BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    if player.lives <= 0:   # and not death_explosion.alive():
        draw_text(screen, 'Game Over!', size=68, x=WIDTH // 2, y=HEIGHT // 2, color=color.RED)
        died_countdown.append(1)
        if len(died_countdown) >= FPS * 3:
            running = False

    draw_text(screen, str(score), size=28, x=WIDTH // 2, y=10, color=color.YELLOW)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()

# if __name__ == "__main__":
