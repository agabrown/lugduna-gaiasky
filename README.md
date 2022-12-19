# lugduna-gaiasky
Visualize the orbit of the asteroid 1133 Lugduna with GaiaSky. This video was made in connection with the Leiden City of
Science 2022 events.

![animation still](./frames/still.png)

## How to reproduce the video

### GaiaSky setup
* Install [GaiaSky](https://zah.uni-heidelberg.de/gaia/outreach/gaiasky)
* Run GaiaSky first to configure it properly for reproducing the video:
    * Make sure that the Hipparcos data set is installed (in addition to the base data set
    * Run GaiaSky and change the GUI _Graphics settings_ to _windowed mode_ with a size of 1280x720 pixels
* Exit GaiaSky

### GaiaSky config files
* To use PNG output frames edit `~/.xdg/gaiasky/config.yaml` and change the "JPG" occurences to "PNG"
    * This step is only needed after the first time running GaiaSky
* Copy the file `orbit-lugduna.json` from the `gsfiles` folder to `~/.local/share/gaiasky/data/default-data/`
* Copy the file `dataset.json` from the `gsfiles` folder to `~/.local/share/gaiasky/data/default-data/`, replacing the
  existing `dataset.json`

### Create the video
* Start GaiaSky and while GaiaSky is running execute the following instruction from the command line:
```cli
python lugduna.py -s
```
* Generate the video by running (can be done without GaiaSky running):
```cli
./makevideo.sh [-e] [-n]
```
* The output videos can be found in the `video` folder.

## Dependencies
* [py4j](https://www.py4j.org/)
* [pygaia](https://pypi.org/project/PyGaia/)
