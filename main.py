import os
import json
import requests
from configuration import access_token


class VkPhoto:

    def __init__ (self, token_vk):
        self.token = token_vk

    def _data_photos (self,offset=0, count=50):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': '1',
                    'album_id': 'profile',
                    'access_token': self.token,
                    'v': '5.131',
                    'extended': '1',
                    'photo_sizes': '1',
                    'count': count,
                    'offset': offset
                    }

        request_vk = requests.get(url=url, params=params)
        return request_vk.json()

# TODO: функцию извлечения фотографий так же сделать приватной!!!
    def extracting_photos (self):
        if not os.path.exists('photo'):
            os.mkdir('photo')

        self.extracting_data = self._data_photos()
        self.number_all_photos = self.extracting_data['response']['count']
        self.list_photo = []
        self.name_and_link = {}
        self.step = 0
        self.count = 50

        while self.step <= self.number_all_photos:
            if self.step != 0:
                self.extracting_data = self._data_photos(offset=self.step, count=self.count)

            for self.extracting_photo in self.extracting_data['response']['items']:
                self.size_extracting_photo = 0
                self.info_extracting_photo = {}
                for self.size_photo in self.extracting_photo['sizes']:
                    print(self.size_photo)
                    self.step += 1
            


aaaa = VkPhoto(access_token)
print(aaaa.extracting_photos())

