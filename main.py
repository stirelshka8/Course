import requests
from configuration import access_token


class VkPhoto:

    def __init__ (self, token_vk):
        self.token = token_vk

    def data_photos (self,offset=0, count=50):
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

asdasd = VkPhoto(access_token)
print(asdasd.data_photos())