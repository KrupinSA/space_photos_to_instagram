import requests
import pathlib
import os
from PIL import Image

def get_file_extension(url: str) -> str:
    parts_path = url.split('/')
    file_name = parts_path[-1]
    return file_name.split('.')[-1]

def download_save(url: str, full_path: str) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(full_path, 'wb') as photo:
        photo.write(response.content)

def fetch_spacex_last_launch(source_path) -> None:
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response = response.json()
    rocket_photos = response['links']['flickr']['original']

    for num, image_url in enumerate(rocket_photos):
            img_full_path = os.path.join(source_path, f'rocket_spacex{num}.jpg')
            download_save(image_url, img_full_path)

def fetch_hubble_photo_by_id(id: int, source_path) -> None:
    hubble_url = f'http://hubblesite.org/api/v3/image/{id}'
    schema = 'https:'
    response = requests.get(hubble_url)
    photos = response.json()['image_files']
    fine_photo_url = photos[-1]['file_url']
    fine_photo_url = f'{schema}{fine_photo_url}'
    photo_full_path = os.path.join(source_path, f'image_{id}.{get_file_extension(fine_photo_url)}')
    download_save(fine_photo_url, photo_full_path)

def convert_images(source_path, dist_path):
    MAX_IMG_WIDTH = 1080
    MAX_IMG_HEIGHT = 1080
    for filename in os.listdir(source_path):
        origin_img_full_path = os.path.join(source_path, filename)
        if os.path.isdir(origin_img_full_path):
            continue
        head_image_name = filename.split('.')[0]
        new_image_name = f'{head_image_name}.jpg'
        conv_img_full_path = os.path.join(dist_path, new_image_name)
        origin_img = Image.open(origin_img_full_path)
        img_width = MAX_IMG_WIDTH if origin_img.width > MAX_IMG_WIDTH else origin_img.width
        img_height = MAX_IMG_HEIGHT if origin_img.height > MAX_IMG_HEIGHT else origin_img.height
        origin_img.thumbnail((img_width, img_height))
        origin_img = origin_img.convert('RGB')
        print(conv_img_full_path)
        origin_img.save(conv_img_full_path, "JPEG")


def main():
    base_img_path = 'images'
    original_images_path = 'original'
    converted_images_path = 'convert'
    path_to_convert_images = os.path.join(base_img_path, converted_images_path)
    path_to_original_images = os.path.join(base_img_path, original_images_path)
    os.makedirs(path_to_original_images,exist_ok=True)
    os.makedirs(path_to_convert_images, exist_ok=True)
    hubble_url = 'http://hubblesite.org/api/v3/images/spacecraft'
    params = {'page': 'all'}
    #response = requests.get(hubble_url, params=params)
    #for photo in response.json():
   #     fetch_hubble_photo_by_id(photo['id'], path_to_original_images)
    #fetch_spacex_last_launch(path_to_original_images)
    convert_images(path_to_original_images, path_to_convert_images)
    

if __name__=="__main__":
    main()