import os, json, requests
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
                    if self.size_photo['height'] >= self.size_extracting_photo:
                        self.size_extracting_photo = self.size_photo['height']
                        print(self.size_extracting_photo)
                if self.extracting_photo['likes']['count'] not in self.name_and_link.keys():
                    self.name_and_link[self.extracting_photo['likes']['count']] = self.size_photo['url']
                    self.info_extracting_photo['file_name'] = f"{self.extracting_photo['likes']['count']}.jpg"
                else:
                    self.name_and_link[f"{self.extracting_photo['likes']['count']} + {self.extracting_photo['date']}"] = self.size_photo['url']
                    self.info_extracting_photo['file_name'] = f"{self.extracting_photo['likes']['count']} + {self.extracting_photo['date']}.jpg"

                self.info_extracting_photo['size'] = self.size_photo['type']
                self.list_photo.append(self.info_extracting_photo)

            for self.name_and_link_key, self.name_and_link_val in self.name_and_link.items():
                with open('photo/%s' % f'{self.name_and_link_key}.jpg', 'wb') as self.open_file:
                    self.images_open = requests.get(self.name_and_link_val)
                    self.open_file.write(self.images_open.content)
            
            with open('info_photo.json', 'w') as self.open_json:
                json.dump(self.list_photo, self.open_json, indent=4)
            
            self.step += self.count


aaaa = VkPhoto(access_token)
print(aaaa.extracting_photos())

