import requests
import pathlib
import os

img_path = 'images'

def download_save(url, full_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(full_path, 'wb') as photo:
        photo.write(response.content)

def fetch_spacex_last_launch():
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response = response.json()
    rocket_photos = response['links']['flickr']['original']

    for num, image_url in enumerate(rocket_photos):
            img_full_path = os.path.join(img_path, f'rocket_spacex{num}.jpg')
            download_save(image_url, img_full_path)

def main():
    try:
        os.mkdir(img_path)
    except FileExistsError:
        pass
    fetch_spacex_last_launch()
    hubble_url = 'http://hubblesite.org/api/v3/image/3811'
    response = requests.get(hubble_url)
    print(response.text)
    photos = response.json()['image_files']
    for cur_photo in photos:
        print(cur_photo['file_url'])

if __name__=="__main__":
    main()