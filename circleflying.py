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
pygame.display.set_caption('Circle Flying (ver 0.1)')


# 리소스 로딩
explosion_anim = []
for i in range(8):
    filename = '{}.png'.format(i + 1)
    # print(filename)
    img = pygame.image.load('images/explosion/' + filename).convert_alpha()
    explosion_anim.append(img)

player_img = pygame.image.load('player_ship.png').convert();

block_img = []
for i in range(5):
    filename = 'meteor{}.png'.format(i + 1)
    img = pygame.image.load('images/meteor/' + filename).convert_alpha()
    block_img.append(img)

player_explode = False



# 메인 함수
def main():
    # 화면 rect
    screen_rect = screen.get_rect()

    # player = PlayerSprite(player_img, screen_rect.center)
    # player_group = pygame.sprite.RenderPlain(player)

    # 스프라이트 전체 그룹
    all_sprites = pygame.sprite.Group()

    # 플레이어 스프라이트 선언
    player = PlayerSprite(player_img, screen_rect.center)
    players = pygame.sprite.Group()
    all_sprites.add(player)
    players.add(player)

    # 장애물 스프라이트 선언
    blocks = pygame.sprite.Group()
    for i in range(8):
        b = BlockSprite()
        all_sprites.add(b)
        blocks.add(b)

    # # 장애물 객체 리스트 선언
    # blocks = [
    #     BlockSprite((200, 200)),
    #     BlockSprite((800, 200)),
    #     BlockSprite((200, 400)),
    #     BlockSprite((800, 400))
    # ]
    # block_group = pygame.sprite.RenderPlain(*blocks)

    # 배경 설정
    background1 = pygame.image.load('images/background3.png').convert_alpha()
    background2 = background1.copy()

    background_width = SCREEN_WIDTH;
    background1_x = 0
    background2_x = background_width;

    while True:
        fps_tick = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # 키입력에 따라 방향 회전 속도를 설정



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
        #     elif event.key == K_a:
        #         # 플레이어 전진 속도
        #         player.user_speed = down * 7
        #
        #
        # if (event.type != KEYDOWN):
        player.user_speed = 3


        # 스프라이트 업데이트
        all_sprites.update()

        # 플레이어, 장애물 충돌 체크
        # hits = pygame.sprite.spritecollide(player, blocks, False)
        hits = pygame.sprite.groupcollide(players, blocks, True, False)
        if hits:
            print("충돌 됨")


        # 플레이어 충돌 체크 (범위 조정 0.85)
        # collisions = pygame.sprite.spritecollide(player, block_group, False, pygame.sprite.collide_rect_ratio(0.85))
        # for hit in collisions:
        #     # player.destory()
        #     expl = ExplosionSprite(hit.rect.center)
        #     expl_group = pygame.sprite.RenderPlain(expl)
        #     expl_group.update()
        #     # ExplosionSprite.update()
        #     # print(hit.rect.center)
        #     # all_sprites.add(expl)

        # collisions = pygame.sprite.spritecollide(player, block_group, False)
        # block_group.update(collisions)

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

        # 랜더링
        all_sprites.draw(screen)
        # block_group.draw(screen)
        pygame.display.flip()


# 플레이어 클래스
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        # self.user_src_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (60, 19))
        img = player_img;
        img.set_colorkey((255,255,255))
        self.user_src_image = pygame.transform.scale(img, (60, 19))
        self.user_src_image = pygame.transform.rotate(self.user_src_image, 90)

        self.user_position = position
        self.user_rotation = -90
        self.user_speed = 0
        self.user_rotation_speed = 0

    def update(self):
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

    def destory(self):
        #TODO : 플레이어 충돌 했을 경우 죽는 애니메이션 나오도록
        #killed = KillAni(self.x, self.y)
        return;


# 장애물 클래스
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_normal = random.choice(block_img)
        # self.image_hit = pygame.image.load("block_hit.png")
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 200)
        self.rect.y = random.randrange(SCREEN_HIGHT - self.rect.height)

        self.speedx = random.randrange(3, 8)
        self.speedy = random.randrange(-3, 3)

        # self.rect.center = self.user_position

    def update(self):
        # # 충돌 체크
        # global player_explode
        # if self in hit_list:
        #     player_explode = True
        #     self.image = self.user_image_hit
        # else:
        #     self.image = self.user_image_normal
        #
        # x, y = self.user_position
        # # x -= 2
        #
        # self.user_position = (x, y)
        # # rad = self.user_rotation * math.pi / 180
        # # x += -self.user_speed * math.sin(rad)
        # # y += -self.user_speed * math.cos(rad)
        #
        # self.rect = self.image.get_rect()
        # self.rect.center = self.user_position

        self.rect.x -= self.speedx
        self.rect.y += self.speedy
        if (self.rect.right < -10) or (self.rect.bottom < -10) or (self.rect.top > SCREEN_HIGHT + 10):
            self.rect.x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH + 100)
            self.rect.y = random.randrange(SCREEN_HIGHT - self.rect.height)

            self.speedx = random.randrange(3, 8)
            # print(self.rect.right)



# 폭발 클래스
class ExplosionSprite(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        print(1)

    def update(self):
        now = pygame.time.get_ticks()
        print(now)
        print(self.last_update)
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_rate += 1
            print(3)
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame_rate]
                self.rect = self.image.get_rect()
                self.rect.center = center
            print(4)


# 이미지 채우는 함수
def fillImg(img, x, y):
    screen.blit(img, (x, y))


# # 플레이어 폭발 애니메이션
# def explode_animation(x, y):
#     loopIter = 0;
#     index = 1
#
#     while True:
#         if (loopIter + 1) % 25 == 0:
#             index += 1
#         loopIter = (loopIter + 1) % 100
#
#         screen.fill((0, 0, 0))
#         fillImg(pygame.image.load('images/explode/' + str(index) + '.png').convert_alpha(), x, y)
#         # print(str(index))
#         pygame.display.flip()
#
#         if (index == 8):
#             return


if __name__ == '__main__':
    main()
