# pi-photo-booth
Photo Booth for Canon EOS 40D

#Required programs
Gphoto2 `sudo apt-get install gphoto2`

wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh

sudo pip-3.2 install gphoto2


# OnScreenPreview
mkfifo filename
gphoto --capture-movie &
omxplayer filename --live

# Mirror Up
gphoto2 --set-config viewfinder=1
#Mirror Down
gphoto2 --set-config viewfinder=0



Photo Booth Options

Initialize
Set Large JPEG

First focus:
    autofocus capture-image

Options
=======
Number of Pictures to take

InitialTime
Time between pictures
Autoupload (facebook group)
Email


Actions
=======
Press Button
Display Viewfinder for 6 seconds
Take Picture
Repeat times

=======
#Installation
