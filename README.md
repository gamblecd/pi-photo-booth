# pi-photo-booth

### Description
Designed to implement a Photo booth with a Raspberry Pi, and using a Canon EOS 40D as the camera.
Goals were to be able to take a series of pictures, while showing a live preview, and the ability to review those images.
Currently uses pygame to display


# Prerequisites


### KivyMD

### Gphoto2:

> `sudo apt-get install gphoto2`

OR for raspberry pi

>`wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh`


# Installation

```
git clone git@github.com/cgamble/pi-photo-booth.git
virtualenv pi-photo-booth
cd pi-photo-booth
source bin/activate
pip install -r requirements.txt
#Install KivyMD
git submodule update --init KivyMD
cd KivyMD
sudo python ./setup.py install

cd ../pi_photobooth
git submodule update --init kivygallery
```

# Run Tests

```
python -m pi_photobooth.tests.test_preview
```

# Usage

Plug a camera into the computer.

`python booth.py`

To begin a Photo Shoot, press Enter, or a button

# Features

* Capture multiple images
* Compiles Images into Photo Booth print
* Uploads to Facebook Event

# Future Tasks

* Remove use of pygame, it has issues trying to show text over what should essentially be a video stream,
* Upload to multiple social sites, Instagram? Twitter?
* Proper logging to the console, and to the screen
* Adjust the UI to look cleaner, need to find references for better UI