# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import math, sys, random

# 프레임 설정
fps = 60

# 해상도 설정
screen_width = 650
screen_height = 356


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF)
clock = pygame.time.Clock()
pygame.display.set_caption('Circle Flying (ver 0.1)')



# 메인 함수
def main():
    # 화면 rect
    screen_rect = screen.get_rect()

    # 플레이어 객체 선언
    pic = pygame.image.load("image.png")
    screen.blit(pygame.transform.scale(pic, (500, 500)), (0, 0))

    player = PlayerSprite('player_ship.png', screen_rect.center)
    player_group = pygame.sprite.RenderPlain(player)

    # 장애물 객체 리스트 선언
    blocks = [
        BlockSprite((200, 200)),
        BlockSprite((800, 200)),
        BlockSprite((200, 400)),
        BlockSprite((800, 400))
    ]
    block_group = pygame.sprite.RenderPlain(*blocks)

    # 배경 설정
    background1 = pygame.image.load('images/background2.jpg').convert_alpha()
    background2 = background1.copy()

    background_width = 650;
    background1_x = 0
    background2_x = background_width;

    while True:
        fps_tick = clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 키입력에 따라 속도, 회전 속도를 설정
        if hasattr(event, 'key'):
            down = event.type == KEYDOWN
            if event.key == K_RIGHT:
                player.user_rotation_speed = down * -5  # 시계 방향
            elif event.key == K_LEFT:
                player.user_rotation_speed = down * 5
            # elif event.key == K_UP:
            #     player.user_speed = down * 5
            elif event.key == K_DOWN:
                player.user_speed = down * -5

        player.user_speed = 1 * 5
        player_group.update(fps_tick)

        # 플레이어 충돌 (범위 조정 0.85)
        collisions = pygame.sprite.spritecollide(player, block_group, False, pygame.sprite.collide_rect_ratio(0.85))
        # collisions = pygame.sprite.spritecollide(player, block_group, False)
        block_group.update(collisions)

        screen.fill((0, 0, 0))  # 화면 지우기
        fillImg(background1, background1_x, 0)  # 배경 이미지 삽입
        fillImg(background2, background2_x, 0)  # 배경 이미지 복사본 삽입

        # 배경 움직임 설정
        background1_x -= 5
        background2_x -= 5
        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width

        player_group.draw(screen)
        block_group.draw(screen)
        pygame.display.flip()



# 플레이어 클래스
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.user_src_image = pygame.image.load(image)
        self.user_src_image = pygame.transform.rotate(self.user_src_image, 90)

        self.user_position = position
        self.user_rotation = -90
        self.user_speed = 0
        self.user_rotation_speed = 0

    def update(self, deltat):
        # 속도, 회전 속도에 따라 위치 정보를 업데이트
        self.user_rotation += self.user_rotation_speed
        x, y = self.user_position
        rad = self.user_rotation * math.pi / 180
        x += -self.user_speed * math.sin(rad)
        y += -self.user_speed * math.cos(rad)

        # 플레이어가 창 밖으로 안나가도록 조정
        if x < 0 or x > screen_width:
            x -= -self.user_speed * math.sin(rad)
        if y < 0 or y > screen_height:
            y -= -self.user_speed * math.cos(rad)


        self.user_position = (x, y)
        self.image = pygame.transform.rotate(self.user_src_image, self.user_rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.user_position


# 장애물 클래스
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.user_image_normal = pygame.image.load("block_normal.png");
        self.user_image_hit = pygame.image.load("block_hit.png");
        self.user_position = position;

        self.image = self.user_image_normal
        self.rect = self.image.get_rect()
        self.rect.center = self.user_position

    def update(self, hit_list):
        # 충돌 체크
        if self in hit_list:
            self.image = self.user_image_hit
        else:
            self.image = self.user_image_normal


        x, y = self.user_position
        x -= 2

        self.user_position = (x, y)
        # rad = self.user_rotation * math.pi / 180
        # x += -self.user_speed * math.sin(rad)
        # y += -self.user_speed * math.cos(rad)


        self.rect = self.image.get_rect()
        self.rect.center = self.user_position

# 이미지 채우는 함수
def fillImg(img, x, y):
    screen.blit(img, (x, y))


if __name__ == '__main__':
    main()