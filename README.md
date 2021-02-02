# space_photos_to_instagram
Uploads photos of spacex launches and photos of the Hubble telescope to instagram using public API. 

### How to install

You must be registered in the instagram. For access, a password and login are used.
You must create a file: 
```
.env
```
File contents:
```
inst_user='...'
inst_pass='...'
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## Run

Launch on Linux(Python 3) or Windows:

```sh
$ python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
