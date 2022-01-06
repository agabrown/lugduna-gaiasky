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
    -loop 1 -framerate 60 -t 15 -i "${IMFOLDER}/startframe.${FILEFMT}" \
    -framerate 60 -i "frames/gs_%05d.${FILEFMT}" \
    -loop 1 -framerate 60 -t 2 -i "${IMFOLDER}/endframe.${FILEFMT}" \
    -filter_complex \
    "[0:v]drawtext=fontfile=/usr/share/fonts/liberation-fonts/LiberationSana-Regular.ttf: \
    textfile=UITLEG:fontcolor_expr=ffffff:fontsize=28:line_spacing=32:box=0: \
    x=(w-text_w)/2:y=(h-text_h)/2, \
        fade=type=out:duration=1:start_time=14,format=yuv420p[v0]; \
    [1:v]drawtext=fontfile=/usr/share/fonts/mononoki/mononoki-Bold.ttf: \
    text=Lugduna:fontcolor_expr=19ff19:fontsize=24:box=0: \
    x=(w-text_w)/2:y=(h-text_h)/2+120:enable='between(t,7,12)', \
    drawtext=fontfile=/usr/share/fonts/mononoki/mononoki-Bold.ttf: \
    text='1 januari 2022':fontcolor_expr=ffffff:fontsize=32:box=0: \
    x=(w-text_w)/2:y=(h-text_h)/2+250:enable='between(t,28,30)',format=yuv420p[v1]; \
    [2:v]drawtext=fontfile=/usr/share/fonts/mononoki/mononoki-Bold.ttf: \
    text='1 januari 2023':fontcolor_expr=ffffff:fontsize=32:box=0: \
    x=(w-text_w)/2:y=(h-text_h)/2+250,format=yuv420p[v2]; \
    [v0][v1][v2]concat=n=3" \
    -pix_fmt yuv420p -vcodec libx264 -s $RESOLUTION video/lugduna.mp4
