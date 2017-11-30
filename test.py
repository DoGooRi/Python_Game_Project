# coding = utf-8

import pygame

pygame.init();
pygame.mixer.music.load('music/background_music.mp3')
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((650, 365))
pygame.display.set_caption('파이게임 테스트')

finish = False
colorBlue = False;
color = None;
x = 30
y = 30

clock = pygame.time.Clock()

background_width = 650

background1 = pygame.image.load('images/background2.jpg').convert_alpha()
background2 = background1.copy()

background1_x = 0
background2_x = background_width


def fillImg(img, x, y):
    screen.blit(img, (x, y))


while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        colorBlue = not colorBlue

    if colorBlue == True:
        color = (0, 0, 255)
    else:
        color = (255, 0, 0)

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3
    screen.fill((0, 0, 0))  # 화면 지우기
    fillImg(background1, background1_x, 0)  # 배경 이미지 삽입
    fillImg(background2, background2_x, 0)  # 배경 이미지 복사본 삽입

    background1_x -= 5
    background2_x -= 5

    if background1_x == -background_width:
        background1_x = background_width

    if background2_x == -background_width:
        background2_x = background_width

    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
quit()
