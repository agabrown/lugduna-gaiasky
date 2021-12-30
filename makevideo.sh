#!/bin/sh

# Create the lugduna animation from the individual png or jpg frames.

# Steps taken in the ffmpeg lines below
#
# 1 ffmpeg command
# 2 set frame rate and input folder
# 3-5 add the name of lugduna as text
# 6 pixel format, resolution, output file

USAGE="Usage: makevideo [-j] [-h]"
USAGELONG="Usage: makevideo [-j] [-h]\n -j use jpg frames \n -h help\n"
RESOLUTION="1280x720"
IMFOLDER="frames"
FILEFMT="png"

while getopts "jh" options;
do
    case $options in
        j) FILEFMT="jpg"
            ;;
        h)
            echo -e $USAGELONG
            exit 0
            ;;
        \?)
            echo $USAGE
            exit 1
            ;;
    esac
done
shift $(($OPTIND-1))

ffmpeg \
    -framerate 60 -i "frames/gs_%05d.${FILEFMT}" \
    -vf "drawtext=fontfile=/usr/share/fonts/mononoki/mononoki-Bold.ttf: \
    text='Lugduna':fontcolor_expr=19ff19:fontsize=24:box=0: \
    x=(w-text_w)/2:y=(h-text_h)/2+120:enable='between(t,7,12)'" \
        -pix_fmt yuv420p -vcodec libx264 -s $RESOLUTION video/lugduna.mp4
