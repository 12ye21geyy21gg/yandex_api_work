import os
import sys
import pygame
import requests

response = None
pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
x, y, d = 37.0, 57.0, 0.2
isUpdated = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            isUpdated = False
            if event.key == pygame.K_UP:
                y += (d - 0.1)
            elif event.key == pygame.K_DOWN:
                y -= (d - 0.1)
            elif event.key == pygame.K_LEFT:
                x -= (d - 0.1)
            elif event.key == pygame.K_RIGHT:
                x += (d - 0.1)
            elif event.key == pygame.K_PAGEUP:
                d *= 0.1
            elif event.key == pygame.K_PAGEDOWN:
                d *= 10
    if not isUpdated:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={d},{d}&l=sat"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason,
                  ")")
            sys.exit(1)
        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        # Инициализируем pygame

        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
