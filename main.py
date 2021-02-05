import requests
import pathlib
import os
from PIL import Image
from dotenv import dotenv_values
from instabot import Bot
import time

WAIT_TIME = 5


def save_file(url: str, filepath: str) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(filepath, 'wb') as photo:
        photo.write(response.content)


def fetch_spacex_last_launch(source_path) -> None:
    spacex_url = 'https://api.spacexdata.com/v4/launches/latest'

    response = requests.get(spacex_url)
    response = response.json()
    rocket_photos = response['links']['flickr']['original']

    for num, image_url in enumerate(rocket_photos):
            img_full_path = os.path.join(source_path, f'rocket_spacex{num}.jpg')
            save_file(image_url, img_full_path)


def fetch_hubble_photo(photo_id: int, source_path) -> None:
    hubble_url = f'http://hubblesite.org/api/v3/image/{id}'
    schema = 'https:'
    response = requests.get(hubble_url)
    photos = response.json()['image_files']
    fine_photo_url = photos[-1]['file_url']
    fine_photo_url = f'{schema}{fine_photo_url}'
    photo_full_path = os.path.join(source_path, f'image_{photo_id}{os.path.splitext(fine_photo_url)[1]}')
    save_file(fine_photo_url, photo_full_path)


def fetch_hubble_photo_collection(path_to_images):
    hubble_url = 'http://hubblesite.org/api/v3/images/spacecraft'
    params = {'page': 'all'}
    response = requests.get(hubble_url, params=params)
    for photo in response.json():
        fetch_hubble_photo(photo['id'], path_to_images)


def convert_images(source_path: str, dist_path: str) -> None:
    max_img_width = 1080
    max_img_height = 1080
    for filename in os.listdir(source_path):
        origin_img_full_path = os.path.join(source_path, filename)
        if os.path.isdir(origin_img_full_path):
            continue
        head_image_name = os.path.splitext(filename)[0]
        image_name = f'{head_image_name}.jpg'
        conv_img_full_path = os.path.join(dist_path, image_name)
        origin_img = Image.open(origin_img_full_path)
        origin_img.thumbnail((max_img_width, max_img_height))
        convert_img = origin_img.convert('RGB')
        convert_img.save(conv_img_full_path, 'JPEG')


def upload_photos_to_instagram(username: str, password: str, source_path: str) -> None:
    bot = Bot()
    bot.login(username=username, password=password)
    for filename in os.listdir(source_path):
        origin_img_full_path = os.path.join(source_path, filename)
        if os.path.isdir(origin_img_full_path):
            continue
        if filename.endswith('jpg'):
            bot.upload_photo(origin_img_full_path)
            time.sleep(WAIT_TIME)


def main():
    dotenv_values()
    inst_user = os.getenv('INST_USER')
    inst_pass = os.getenv('INST_PASS')
    base_img_path = 'images'
    original_images_path = 'original'
    converted_images_path = 'convert'
    converted_images_path = os.path.join(base_img_path, converted_images_path)
    original_images_path = os.path.join(base_img_path, original_images_path)
    os.makedirs(original_images_path, exist_ok=True)
    os.makedirs(converted_images_path, exist_ok=True)
    fetch_hubble_photo_collection(original_images_path)
    fetch_spacex_last_launch(original_images_path)
    convert_images(original_images_path, converted_images_path)
    upload_photos_to_instagram(inst_user, inst_pass, converted_images_path)
    

if __name__=='__main__':
    main()
