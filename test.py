# coding = utf-8

import pygame

pygame.init();

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('파이게임 테스트')

finish = False
colorBlue = False;
color = None;

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

    pygame.draw.rect(screen, color, pygame.Rect(0, 0, 60, 60))
    pygame.display.flip()
