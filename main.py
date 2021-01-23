import requests
import pathlib
import os

img_path = 'images'

def get_file_extension(url: str) -> str:
    parts_path = url.split('/')
    file_name = parts_path[-1]
    return file_name.split('.')[-1]

def download_save(url: str, full_path: str) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(full_path, 'wb') as photo:
        photo.write(response.content)

def fetch_spacex_last_launch() -> None:
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response = response.json()
    rocket_photos = response['links']['flickr']['original']

    for num, image_url in enumerate(rocket_photos):
            img_full_path = os.path.join(img_path, f'rocket_spacex{num}.jpg')
            download_save(image_url, img_full_path)

def fetch_hubble_photo_by_id(id: int) -> None:
    hubble_url = f'http://hubblesite.org/api/v3/image/{id}'
    schema = 'https:'
    response = requests.get(hubble_url)
    photos = response.json()['image_files']
    fine_photo_url = photos[-1]['file_url']
    fine_photo_url = f'{schema}{fine_photo_url}'
    photo_full_path = os.path.join(img_path, f'image_{id}.{get_file_extension(fine_photo_url)}')
    download_save(fine_photo_url, photo_full_path)


def main():
    try:
        os.mkdir(img_path)
    except FileExistsError:
        pass
    fetch_spacex_last_launch()
    fetch_hubble_photo_by_id(1)

if __name__=="__main__":
    main()