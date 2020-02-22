import os
import sys
import pygame
import requests
import threading, copy
from PyQt5.QtWidgets import QApplication


# import settings

class pygame_thread():
    def __init__(self):

        pygame.init()
        self.width = 600
        self.height = 450
        self.screen = pygame.display.set_mode((600, 450))
        self.render_colors = [pygame.Color('yellow'), pygame.Color('orange'),
                              pygame.Color('red')]
        self.render_modes = ['map', 'sat', 'skl']
        self.r = 30
        self.render_mode = 0
        self.response = None
        self.running = True
        self.x, self.y, self.d = (40.0), (57.5), 0.2
        self.last_waypoint = None
        self.isUpdated = False
        self.data = None
        self.isIndex = False
        self.isAddress = False
        self.str_data = ''

    def get_object_at(self, pos):
        coords = [
            self.x + (pos[0] - self.width / 2) / (self.width / 2) * self.d * 2.02,
            ((self.height - pos[1]) - self.height / 2) / (self.height / 2) * self.d * 0.82 + self.y]
        # self.last_waypoint = copy.copy(coords)
        # self.x = self.last_waypoint[0]
        # self.y = self.last_waypoint[1]
        self.get_data_of(','.join(map(lambda x: str(x), coords)))
        self.last_waypoint = copy.copy(coords)

    def draw_misc(self):
        pygame.draw.rect(self.screen, self.render_colors[self.render_mode % 3],
                         ((self.width - self.r * 2, self.height - self.r * 2), (self.r * 2, self.r * 2)), 0)
        font = pygame.font.Font(None, 25)
        text = font.render(self.render_modes[self.render_mode % 3], 1, pygame.Color('black'))
        self.screen.blit(text, (self.width - self.r - 10, self.height - self.r - 10))
        pygame.draw.rect(self.screen, self.render_colors[1],
                         ((0, self.height - self.r * 2), (self.r * 2, self.r * 2)))
        font = pygame.font.Font(None, 25)
        text = font.render("menu", 1, pygame.Color('black'))
        self.screen.blit(text, (5, self.height - self.r - 10))

    def get_data_of(self, name, setCoords=False):
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
        # print(toponym_coodrinates)
        self.last_waypoint = list(map(lambda x: float(x), toponym_coodrinates.split(" ")))
        if setCoords:
            self.x, self.y = map(lambda x: float(x), toponym_coodrinates.split(" "))
        self.data = toponym
        print(self.data)

    def call_menu(self):
        os.system('python settings.py')

    def make_str(self):
        s = ''
        if self.data is not None:
            s = s + f'Наименование:{self.data["name"]}\n'
            if self.isAddress:
                try:
                    s = s + f'Доп. Информация:{self.data["description"]}\n'
                    s = s + f'Тип:{self.data["metaDataProperty"]["GeocoderMetaData"]["kind"]}\n'
                    if self.isIndex:
                        s = s + f'Код почты:{self.data["metaDataProperty"]["GeocoderMetaData"]["Address"][
                            "postal_code"]}\n'
                except Exception:
                    print('error try again')
            s = s + f'Координаты: {self.data["Point"]["pos"]}'
        with open('taxi2', mode='w', encoding='utf8') as f:
            f.write(s)

    def restart(self):
        self.data = None
        self.last_waypoint = None
        self.isUpdated = False

    def check_for_data(self):
        if os.path.isfile('taxi1'):
            with open('taxi1', mode='r', encoding='utf8') as f:
                data = f.read()
                if data.split(':')[0] == 'reset':
                    self.restart()
                elif data.split(':')[0] == 'search':
                    print(data.split(':')[1])
                    self.get_data_of(data.split(':')[1], True)
                elif data.split(':')[0] == 'check':
                    if data.split(':')[1][0] == '1':
                        self.isIndex = True
                    else:
                        self.isIndex = False
                    if data.split(':')[1][1] == '1':
                        self.isAddress = True
                    else:
                        self.isAddress = False
                elif data.split(':')[0] == 'move':
                    temp = data.split(':')[1].split(',')
                    self.x = float(temp[0])
                    if self.x >= 180 - self.d:
                        self.x = 180 - self.d
                    if self.x <= -180 + self.d:
                        self.x = -180 + self.d
                    self.y = float(temp[1])
                    if self.y >= 85 - self.d:
                        self.y = 85 - self.d
                    if self.y <= -85 + self.d:
                        self.y = -85 + self.d
                    self.d = float(temp[2])
                    if self.d >= 10:
                        self.d = 10
                    if self.d <= 0.001:
                        self.d = 0.001
            self.isUpdated = False
            os.remove('taxi1')

    def loop(self):
        while self.running:
            self.check_for_data()
            self.make_str()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.isUpdated = False
                    if event.key == pygame.K_UP:
                        self.y += (self.d) / 2 * self.height / self.width
                        if self.y >= 85 - self.d:
                            self.y = 85 - self.d
                    elif event.key == pygame.K_DOWN:
                        self.y -= (self.d) / 2 * self.height / self.width
                        if self.y <= -85 + self.d:
                            self.y = -85 + self.d
                    elif event.key == pygame.K_LEFT:
                        self.x -= (self.d) / 2
                        if self.x <= -180 + self.d:
                            self.x = -180 + self.d
                    elif event.key == pygame.K_RIGHT:
                        self.x += (self.d) / 2
                        if self.x >= 180 - self.d:
                            self.x = 180 - self.d
                    elif event.key == pygame.K_PAGEUP:
                        self.d *= 0.5
                        if self.d <= 0.001:
                            self.d = 0.001
                    elif event.key == pygame.K_PAGEDOWN:
                        self.d *= 2
                        if self.d >= 10:
                            self.d = 10
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (event.pos[0] <= self.width and event.pos[0] >= self.width - self.r * 2 and
                                event.pos[1] <= self.height and event.pos[1] >= self.height - self.r * 2):

                            self.render_mode += 1
                            self.isUpdated = False
                        elif (event.pos[0] <= self.r * 2 and event.pos[0] >= 0 and event.pos[
                            1] <= self.height and event.pos[1] >= self.height - self.r * 2):
                            self.call_menu()
                        else:
                            self.get_object_at(event.pos)
                            self.isUpdated = False

            if not self.isUpdated:
                self.screen.fill((0, 0, 0))
                if self.last_waypoint is None:
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn={self.d},{self.d}&l={
                    self.render_modes[self.render_mode % 3]}"
                else:
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn={self.d},{self.d}&l={
                    self.render_modes[self.render_mode % 3]}&pt={self.last_waypoint[0]},{self.last_waypoint[1]}"
                response = requests.get(map_request)
                if not response:
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason,
                          ")")
                    sys.exit(1)
                self.isUpdated = True
                # Запишем полученное изображение в файл.
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                # Инициализируем pygame

                # Рисуем картинку, загружаемую из только что созданного файла.
                self.screen.blit(pygame.image.load(map_file), (0, 0))
                self.draw_misc()

                pygame.display.flip()
        pygame.quit()
        # Удаляем за собой файл с изображением.
        os.remove(map_file)


pg = pygame_thread()
pg.loop()
