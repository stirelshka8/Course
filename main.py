import os, json, requests, getpass, logging, datetime
from configuration import access_token
from progress.bar import IncrementalBar

logging.basicConfig(filename="logging.log", level=logging.INFO)

def startup():
    name_temp_folder = 'photo'
    if not os.path.exists(name_temp_folder):
        os.mkdir(name_temp_folder)
        print("[INFO] Директория для загружки фотографий создана")
        logging.info(f"{datetime.datetime.now()} Директория {name_temp_folder} создана")
    else:
        print("[INFO] Директория для загружки фотографий уже существует")
        logging.info(f"{datetime.datetime.now()} Директория {name_temp_folder} уже существует")

    input_user_id = str(input("Введите ID пользователя ВКонтакте - > "))
    input_yandex_token = str(input("Введите токен Я.Диска для загрузки фотографий - > "))

    startup_vk = VkPhoto(access_token, input_user_id, name_temp_folder)
    startup_vk.extracting_photos()
    startup_ya = YandexUpload(input_yandex_token)
    startup_ya.creating_directory()

    dir_photos = os.listdir(name_temp_folder)
    photo_counter = 0
    print('[INFO] Начало загрузки фотографий на Я.Диск')
    bar_upload = IncrementalBar('[INFO] Загрузка', max = len(dir_photos))
    for dir_photo in dir_photos:
        bar_upload.next() 
        file_photo_name = dir_photo      
        file_path = f'{os.getcwd()}/{name_temp_folder}/{dir_photo}'
        startup_ya.upload_photo(file_path, file_photo_name)         
        photo_counter += 1
    bar_upload.finish()    
    print(f'[INFO] Загружено {photo_counter} фотографий на Я.Диск')
    
    logging.info(f"{datetime.datetime.now()} На Я.Диск, в папку \{getpass.getuser()}\ загружено {photo_counter} фотографий")

class VkPhoto:

    def __init__ (self, token_vk, user_id, name_temp_folder):
        self.name_temp_folder = name_temp_folder
        self.token = token_vk
        self.user_id = user_id

    def _data_photos (self, offset=0, count=50):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_id,
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

        self.extracting_data = self._data_photos()
        self.number_all_photos = self.extracting_data['response']['count']
        self.list_photo = []
        self.name_and_link = {}
        self.step = 0
        self.count = 50
        self.counter_download_photo = 0

        while self.step <= self.number_all_photos:
            if self.step != 0:
                self.extracting_data = self._data_photos(offset=self.step, count=self.count)

            for self.extracting_photo in self.extracting_data['response']['items']:
                self.size_extracting_photo = 0
                self.info_extracting_photo = {}
                
                for self.size_photo in self.extracting_photo['sizes']:
                    if self.size_photo['height'] >= self.size_extracting_photo:
                        self.size_extracting_photo = self.size_photo['height']

                if self.extracting_photo['likes']['count'] not in self.name_and_link.keys():
                    self.name_and_link[self.extracting_photo['likes']['count']] = self.size_photo['url']
                    self.info_extracting_photo['file_name'] = f"{self.extracting_photo['likes']['count']}.jpg"
                else:
                    self.name_and_link[f"{self.extracting_photo['likes']['count']}_{self.extracting_photo['date']}"] = self.size_photo['url']
                    self.info_extracting_photo['file_name'] = f"{self.extracting_photo['likes']['count']}_{self.extracting_photo['date']}.jpg"

                self.info_extracting_photo['size'] = self.size_photo['type']
                self.list_photo.append(self.info_extracting_photo)
            print("[INFO] Начало загрузки фотографий из профиля ВК")
            bar_download = IncrementalBar('[INFO] Загрузка', max = len(self.name_and_link.items()))
            for self.name_and_link_key, self.name_and_link_val in self.name_and_link.items():
                with open('photo/%s' % f'{self.name_and_link_key}.jpg', 'wb') as self.open_file:
                    self.images_open = requests.get(self.name_and_link_val)
                    self.open_file.write(self.images_open.content)
                    self.counter_download_photo += 1
                bar_download.next()
            bar_download.finish()  
            print(f'[INFO] Загружено {self.counter_download_photo} фотографий с профиля ВК')
            logging.info(f"{datetime.datetime.now()} Из профиля Вконтакте ID - {self.user_id}, в папку \{self.name_temp_folder}\ загружено {self.counter_download_photo} фотографий")
            with open('info_photo.json', 'w') as self.open_json:
                json.dump(self.list_photo, self.open_json, indent=4)
            
            self.step += self.count

class YandexUpload:

    def __init__(self, yandex_token):
        self.yandex_token = yandex_token       
        self.name_folder = getpass.getuser()
            
    def creating_directory(self):
        self.yandex_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.yandex_token}'}
        self.params = {'path': f'{self.name_folder}', 'overwrite': 'false'}
        self.send_request = requests.put(url=self.yandex_url, headers=self.headers, params=self.params)
    
    def upload_photo(self, file_path, file_photo_name):
        self.file_path = file_path
        self.startup_list = file_photo_name
        self.yandex_upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.yandex_token}'}
        self.params = {'path': f'{self.name_folder}/{self.startup_list}', 'overwrite': 'true'}

        self.request_yandex = requests.get(url=self.yandex_upload_url, headers=self.headers, params=self.params)
        self.received_link = self.request_yandex.json().get('href')
        self.uploader_photo = requests.put(self.received_link, data=open(self.file_path, 'rb'))
        return

if __name__ == '__main__':
    startup()
