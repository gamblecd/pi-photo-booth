# pi-photo-booth

### Description
Designed to implement a Photo booth with a Raspberry Pi, and using a Canon EOS 40D as the camera.
Goals were to be able to take a series of pictures, while showing a live preview, and the ability to review those images.
Currently uses Kivy as an interface.


# Prerequisites

### Python3.6
Uses format Strings syntax. much simpler but 3.6 was running into issue with other areas, such is the life of a guinea pig.

### pip
  ```bash
  sudo apt-get update
  sudo apt-get install python-setuptools python-dev build-essential git-core -y
  sudo easy_install pip
  ```
### virtualenv
```bash
pip install virtualenv
```
### Gphoto2:
```bash
sudo apt-get install gphoto2
```
OR for raspberry pi
```bash
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh
```

# Installation

```sh
git clone git@github.com/cgamble/pi-photo-booth.git
virtualenv pi-photo-booth # For a clean workspace
cd pi-photo-booth
source bin/activate # Activates virtual environment
pip install -r requirements.txt # installs to virtual environment
#Install KivyMD
git submodule update --init KivyMD
cd KivyMD
sudo python ./setup.py install

cd ../pi_photobooth
git submodule update --init kivygallery
cd ..
```

# Run Tests

```
TODO #Will update with new tests
```

# Usage

Plug a camera into the computer. Make sure the camera is turned on.

```
source bin/activate # if not in the virtual environment already
python pi_photobooth/main.py
```

Follow the on screen instructions.

# Development Notes

* Kivy's use of canvas lines does not work on raspberry pi, causes interface to be super slow on any rerender
  * NavigationDrawerToolbar used lines, so I had to add an override of it. will not be updated if KivyMD is not updated.

# Features

* Capture multiple images
* Compiles Images into Photo Booth print
* Uploads to Facebook Event
* In App Gallery to see previous pictures. 

# Future Tasks (see projects)

* Cognitive Services API
* Adjust interface for Usability
* Add Functionality for GPIO Buttons.
* ~~Remove use of pygame, it has issues trying to show text over what should essentially be a video stream~~(Replaced with Kivy)
* Upload to multiple social sites, Instagram? Twitter?
* ~~Proper logging to the console, and to the screen~~ (Visual Log on Kivy)
* ~~Adjust the UI to look cleaner, need to find references for better UI~~ (Resolved With Kivy)
