# coding = utf-8

import pygame

pygame.init();

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('파이게임 테스트')

finish = False
colorBlue = False;
color = None;
x = 30
y = 30

clock = pygame.time.Clock()

myImg = pygame.image.load('images/background.jpg')

def myimg(x, y):
    screen.blit(myImg, (x, y))


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
    myimg(0, 0) # 배경 이미지 삽입
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
quit()
