import os
import requests
from configuration import access_token


class VkPhoto:

    def __init__ (self, token_vk):
        self.token = token_vk

    def __data_photos (self,offset=0, count=50):
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

    def extracting_photos (self):
        if not os.path.exists('photo'):
            os.mkdir('photo')

        self.extracting_data = self.__data_photos()
        self.number_all_photos = self.extracting_data['response']['count']
        self.list_photo = []
        self.name_and_link = {}
        self.step = 0
        self.count = 50

        while self.step <= self.number_all_photos:
            if self.step != 0:
                self.extracting_data = self._data_photos(offset=self.step, count=self.count)



aaaa = VkPhoto(access_token)
print(aaaa.__data_photos())

