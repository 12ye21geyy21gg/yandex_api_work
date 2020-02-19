import os
import sys
import pygame
import requests
import threading, copy


pygame.init()
width = 600
height = 450
screen = pygame.display.set_mode((600, 450))
render_colors = [pygame.Color('yellow'), pygame.Color('orange'),
                 pygame.Color('red')]
render_modes = ['map', 'sat', 'skl']
r = 30
render_mode = 0
response = None
running = True
x, y, d = 37.0, 57.0, 0.2
last_waypoint = None
isUpdated = False
data = None
isIndex = False
isAddress = False
str_data = ''


def get_object_at(pos):
    coords = [
        x + (pos[0] - width / 2) / (width / 2) * d * 2.02,
        ((height - pos[1]) - height / 2) / (height / 2) * d * 0.82 + y]
    global last_waypoint
    last_waypoint = copy.copy(coords)


def draw_misc():
    pygame.draw.rect(screen, render_colors[render_mode % 3],
                     ((width - r * 2, height - r * 2), (r * 2, r * 2)), 0)
    font = pygame.font.Font(None, 25)
    text = font.render(render_modes[render_mode % 3], 1, pygame.Color('black'))
    screen.blit(text, (width - r - 10, height - r - 10))
    pygame.draw.rect(screen, render_colors[1],
                     ((0, height - r * 2), (r * 2, r * 2)))
    font = pygame.font.Font(None, 25)
    text = font.render("menu", 1, pygame.Color('black'))
    screen.blit(text, (5, height - r - 10))


def get_data_of(name):
    global x, y, data
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]

    x, y = toponym_coodrinates.split(" ")
    data = toponym

def call_menu():
    pass


def make_str():
    global s
    s = ''
    s = s + 'name:'

def restart():
    global data, last_waypoint, isUpdated
    data = None
    last_waypoint = None
    isUpdated = False


# menu_thread = threading.Thread(target=, (,))
# manu_thread.start()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            isUpdated = False
            if event.key == pygame.K_UP:
                y += (d) / 2 * height / width
            elif event.key == pygame.K_DOWN:
                y -= (d) / 2 * height / width
            elif event.key == pygame.K_LEFT:
                x -= (d) / 2
            elif event.key == pygame.K_RIGHT:
                x += (d) / 2
            elif event.key == pygame.K_PAGEUP:
                d *= 0.5
                if d <= 0.001:
                    d = 0.001
            elif event.key == pygame.K_PAGEDOWN:
                d *= 2
                if d >= 10:
                    d = 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (event.pos[0] <= width and event.pos[0] >= width - r * 2 and
                        event.pos[1] <= height and event.pos[1] >= height - r * 2):

                    render_mode += 1
                    isUpdated = False
                elif (event.pos[0] <= r * 2 and event.pos[0] >= 0 and event.pos[
                    1] <= height and event.pos[1] >= height - r * 2):
                    call_menu()
                else:
                    get_object_at(event.pos)
                    isUpdated = False


    if not isUpdated:
        screen.fill((0, 0, 0))
        if last_waypoint is None:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={d},{d}&l={render_modes[render_mode % 3]}"
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={d},{d}&l={render_modes[render_mode % 3]}&pt={last_waypoint[0]},{last_waypoint[1]}"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason,
                  ")")
            sys.exit(1)
        isUpdated = True
        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        # Инициализируем pygame

        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        draw_misc()

        pygame.display.flip()
pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
