# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import math, sys, random, time

# 프레임 설정
FPS = 60
# 해상도 설정
SCREEN_WIDTH = 900
SCREEN_HIGHT = 600

# 파이게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT), DOUBLEBUF)
clock = pygame.time.Clock()
pygame.display.set_caption('Circle Flying (ver 1.0)')

# 전역 변수
HIGH_SCORE = 0
SCORE = 0

# 이미지 리소스 로딩
player_img = []
for i in range(10):
    filename = 'player{}.png'.format(i + 1)
    img = pygame.image.load('images/player/' + filename).convert_alpha()
    player_img.append(img)

block_img = []
for i in range(5):
    filename = 'meteor{}.png'.format(i + 1)
    img = pygame.image.load('images/meteor/' + filename).convert_alpha()
    block_img.append(img)

collision_img = []
for i in range(6):
    filename = 'player_killed{}.png'.format(i + 1)
    img = pygame.image.load('images/player_killed/' + filename).convert_alpha()
    collision_img.append(img)

main_menu = [pygame.image.load('images/START1.png').convert_alpha(),
             pygame.image.load('images/START2.png').convert_alpha()]

game_over_menu = [pygame.image.load('images/END1.png').convert_alpha(),
                  pygame.image.load('images/END2.png').convert_alpha()]

# 폰트 로딩
font = pygame.font.Font('font/Minecraftia-Regular.ttf', 32)

# 메인 함수
def main():


    global HIGH_SCORE, SCORE

    # 화면 rect
    screen_rect = screen.get_rect()

    # 스프라이트 전체 그룹
    all_sprites = pygame.sprite.Group()

    # 플레이어 스프라이트 선언
    player = PlayerSprite(player_img, (20, SCREEN_HIGHT / 2))
    players = pygame.sprite.Group()
    all_sprites.add(player)
    players.add(player)

    # 장애물 스프라이트 선언 (8개)
    blocks = pygame.sprite.Group()
    for i in range(8):
        b = BlockSprite()
        all_sprites.add(b)
        blocks.add(b)

    # 배경 설정
    background1 = pygame.image.load('images/background/background.png').convert_alpha()
    background2 = background1.copy()

    background_width = SCREEN_WIDTH;
    background1_x = 0
    background2_x = background_width;

    coll = False
    gmae_start = True
    game_over = False

    while True:
        if (gmae_start):
            showMainMenu()
            gmae_start = False

        if (game_over):
            showGameOverMenu()
            game_over = False

            #초기화
            SCORE = 0
            coll = False
            # 스프라이트 전체 그룹
            all_sprites = pygame.sprite.Group()
            # 플레이어 스프라이트 선언
            player = PlayerSprite(player_img, (20, SCREEN_HIGHT / 2))
            players = pygame.sprite.Group()
            all_sprites.add(player)
            players.add(player)
            # 장애물 스프라이트 선언 (8개)
            blocks = pygame.sprite.Group()
            for i in range(8):
                b = BlockSprite()
                all_sprites.add(b)
                blocks.add(b)

        fps_tick = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if hasattr(event, 'key'):
                down = event.type == KEYDOWN
                if event.key == K_RIGHT:
                    player.user_rotation_speed = down * -5  # 시계 방향
                elif event.key == K_LEFT:
                    player.user_rotation_speed = down * 5
                # elif event.key == K_UP:
                #     player.user_speed = down * 5
                # elif event.key == K_DOWN:
                #     player.user_speed = down * -5

        player.user_speed = 3

        # 스프라이트 업데이트
        all_sprites.update()

        # 플레이어, 장애물 충돌 체크
        # hits = pygame.sprite.spritecollide(player, blocks, False)
        hits = pygame.sprite.groupcollide(players, blocks, True, False, pygame.sprite.collide_circle)
        for hit in hits:
            print("충돌 됨")
            coll = True
            player_collision = CollisionAniSprite(hit.rect.center)
            all_sprites.add(player_collision)

        if (coll):
            if not (player_collision.alive()):
                # 스프라이트 모두 삭제
                all_sprites.empty()
                players.empty()
                blocks.empty()
                game_over = True

        # 배경 무한 스크롤을 위해 배경 복제
        screen.fill((0, 0, 0))  # 화면 지우기
        fillImg(background1, background1_x, 0)  # 배경 이미지 삽입
        fillImg(background2, background2_x, 0)  # 배경 이미지 복사본 삽입

        # 배경 좌표 설정
        background1_x -= 5
        background2_x -= 5
        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width

        # 점수 추가 및 점수 표시
        if (player.alive()):
            SCORE += 0.3
        text = font.render(str(round(SCORE)), False, (255, 255, 255));
        screen.blit(text, (10, 10))

        # 랜더링
        all_sprites.draw(screen)
        pygame.display.flip()


def showMainMenu():
    last_update = pygame.time.get_ticks()
    index = 0

    fillImg(main_menu[0], 0, 0)  # 배경 이미지 삽입

    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                waiting = False

        now = pygame.time.get_ticks()

        if (now - last_update) > 500:
            index = (index + 1) % 2
            last_update = now
            fillImg(main_menu[index], 0, 0)  # 배경 이미지 삽입

        pygame.display.flip()

def showGameOverMenu():
    global HIGH_SCORE, SCORE

    if HIGH_SCORE < SCORE:
        HIGH_SCORE = SCORE

    last_update = pygame.time.get_ticks()
    index = 0

    fillImg(game_over_menu[0], 0, 0)  # 배경 이미지 삽입

    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if hasattr(event, 'key'):
                down = event.type == KEYDOWN
                if (down):
                    waiting = False

        now = pygame.time.get_ticks()
        # screen.fill((0, 0, 0))  # 화면 지우기

        if (now - last_update) > 500:
            index = (index + 1) % 2
            last_update = now
            fillImg(game_over_menu[index], 0, 0)  # 배경 이미지 삽입

        text = font.render(str(round(SCORE)), False, (255, 255, 255));
        screen.blit(text, (530, 92))
        text2 = font.render(str(round(HIGH_SCORE)), False, (255, 255, 255));
        screen.blit(text2, (530, 152))

        pygame.display.flip()


# 플레이어 클래스
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (60, 19))
        # img = player_img[0];
        # img.set_colorkey((255, 255, 255))
        # self.user_src_image = pygame.transform.scale(img, (60, 19))
        # self.user_src_image = pygame.transform.rotate(self.user_src_image, 90)
        # self.user_src_image = pygame.transform.rotate(img, 90)
        self.user_src_image = player_img[0];

        # 충돌 collide_circle 체킹용 radius 변수
        self.rect = self.user_src_image.get_rect()
        self.radius = round(self.rect.width)
        # 충돌 범위 조정 디버깅용
        # pygame.draw.circle(self.user_src_image, (255, 0, 0), self.rect.center, self.radius)

        self.user_position = position
        self.user_rotation = 0
        self.user_speed = 0
        self.user_rotation_speed = 0

        self.last_update = pygame.time.get_ticks()
        self.ani_index = 0


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > FPS * 2:
            self.last_update = now
            self.ani_index = (self.ani_index + 1) % 10
            # print(self.ani_index)
            self.user_src_image = player_img[self.ani_index]

    def update(self):
        # 애니메이션 트리거
        self.animation()
        # 속도, 회전 속도에 따라 위치 정보를 업데이트
        self.user_rotation += self.user_rotation_speed
        x, y = self.user_position
        rad = self.user_rotation * math.pi / 180
        x += -self.user_speed * math.sin(rad)
        y += -self.user_speed * math.cos(rad)

        # 플레이어가 창 밖으로 안나가도록 조정
        if x < 0 or x > SCREEN_WIDTH:
            x -= -self.user_speed * math.sin(rad)
        if y < 0 or y > SCREEN_HIGHT:
            y -= -self.user_speed * math.cos(rad)

        self.user_position = (x, y)
        self.image = pygame.transform.rotate(self.user_src_image, self.user_rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.user_position


# 장애물 클래스
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(block_img)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        # 충돌 collide_circle 체킹용 radius 변수
        self.radius = round(self.rect.width / 2 * 0.85)
        # 충돌 범위 조정 디버깅용
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)

        self.rect.x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 200)
        self.rect.y = random.randrange(SCREEN_HIGHT - self.rect.height)
        self.speedx = random.randrange(3, 8)
        self.speedy = random.randrange(-3, 3)

        # self.rect.center = self.user_position

        self.last_update = pygame.time.get_ticks()
        self.rot = 0
        self.rot_speed = random.randrange(-12, 12)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > FPS:
            # print('tick')
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # 회전 트리거
        self.rotate()
        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if (self.rect.right < -10) or (self.rect.bottom < -10) or (self.rect.top > SCREEN_HIGHT + 10):
            self.rect.x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 100)
            self.rect.y = random.randrange(SCREEN_HIGHT - self.rect.height)

            self.speedx = random.randrange(3, 8)
            # print(self.rect.right)


# 충돌 애니메이션 클래스
class CollisionAniSprite(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = collision_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.ani_index = 0

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > FPS * 2:
            self.last_update = now
            if (self.ani_index != len(collision_img) - 1):
                self.ani_index += 1
            else:
                self.kill()
            # print(self.ani_index)
            self.image = collision_img[self.ani_index]

    def update(self):
        self.animation()


# 이미지 채우는 함수
def fillImg(img, x, y):
    screen.blit(img, (x, y))


if __name__ == '__main__':
    main()
