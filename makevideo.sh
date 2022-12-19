#!/bin/sh

# Create the lugduna animation from the individual png or jpg frames.

# Steps taken in the ffmpeg lines below
#
# 1 ffmpeg command
# 2 title frame is kept static for 15 seconds (stream [0:v])
# 3 input frames for full animation (stream [1:v])
# 4 end frame is kept static for 3 seconds (stream ([2:v])
# 5 start complex filter operating on the above streams
# 6-9 add explanatory text to start frame
# 10-15 add the name of lugduna as text between seconds 7 and 12, and add
#       the start date of the orbit animation between seconds 28 and 30
# 16-18 add the end data of the orbit animation to the end frame
# 19 concatenate the streams v0-v2
# 6 pixel format, video codec, resolution, output file

USAGE="Usage: makevideo [-j] [-e] [-n] [-h]"
USAGELONG="Usage: makevideo [-j] [-e] [-n] [-h]\n -j use jpg frames\n -e use english\n -n do not add explanatory text\n -h help\n"
RESOLUTION="1280x720"
IMFOLDER="frames"
FILEFMT="png"
TAAL="nl"
EXPLFILE="uitleg.txt"
STARTDATE="1 januari 2022"
ENDDATE="31 december 2022"
ADDEXPL=1
FONTFILE="/usr/share/fonts/liberation-fonts/LiberationSans-Bold.ttf"

while getopts "jenh" options;
do
    case $options in
        j) FILEFMT="jpg"
            ;;
        e)
            TAAL="en"
            EXPLFILE="explanation.txt"
            STARTDATE="January 1 2022"
            ENDDATE="December 31 2022"
            ;;
        n)
            ADDEXPL=0
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

if [ $ADDEXPL -eq 1 ]
then
    ffmpeg \
        -loop 1 -framerate 60 -t 20 -i "${IMFOLDER}/startframe.${FILEFMT}" \
        -framerate 60 -i "frames/gs_%05d.${FILEFMT}" \
        -loop 1 -framerate 60 -t 3 -i "${IMFOLDER}/endframe.${FILEFMT}" \
        -filter_complex \
        "[0:v]drawbox=w=iw:h=ih:color=black@0.5:t=fill,drawtext=fontfile=${FONTFILE}: \
        textfile=${EXPLFILE}:fontcolor_expr=ffffff:fontsize=28:line_spacing=14:box=0: \
        x=(w-text_w)/2:y=78, \
        fade=type=out:duration=1:start_time=19,format=yuv420p[v0]; \
        [1:v]drawtext=fontfile=${FONTFILE}: \
        text=Lugduna:fontcolor_expr=19ff19:fontsize=24:box=0: \
        x=(w-text_w)/2-120:y=(h-text_h)/2+40:enable='between(t,7,12)', \
        drawtext=fontfile=${FONTFILE}: \
        text=${STARTDATE}:fontcolor_expr=ffffff:fontsize=32:box=0: \
        x=(w-text_w)/2:y=(h-text_h)/2+250:enable='between(t,28,31)',format=yuv420p[v1]; \
        [2:v]drawtext=fontfile=${FONTFILE}: \
        text=${ENDDATE}:fontcolor_expr=ffffff:fontsize=32:box=0: \
        x=(w-text_w)/2:y=(h-text_h)/2+250,format=yuv420p[v2]; \
        [v0][v1][v2]concat=n=3" \
        -pix_fmt yuv420p -vcodec libx264 -s $RESOLUTION video/lugduna-${TAAL}.mp4
else
    ffmpeg \
        -framerate 60 -i "frames/gs_%05d.${FILEFMT}" \
        -loop 1 -framerate 60 -t 3 -i "${IMFOLDER}/endframe.${FILEFMT}" \
        -filter_complex \
        "[0:v]drawtext=fontfile=${FONTFILE}: \
        text=Lugduna:fontcolor_expr=19ff19:fontsize=24:box=0: \
        x=(w-text_w)/2-120:y=(h-text_h)/2+40:enable='between(t,7,12)', \
        drawtext=fontfile=${FONTFILE}: \
        text=${STARTDATE}:fontcolor_expr=ffffff:fontsize=32:box=0: \
        x=(w-text_w)/2:y=(h-text_h)/2+250:enable='between(t,28,31)',format=yuv420p[v0]; \
        [1:v]drawtext=fontfile=${FONTFILE}: \
        text=${ENDDATE}:fontcolor_expr=ffffff:fontsize=32:box=0: \
        x=(w-text_w)/2:y=(h-text_h)/2+250,format=yuv420p[v1]; \
        [v0][v1]concat=n=2" \
        -pix_fmt yuv420p -vcodec libx264 -s $RESOLUTION video/lugduna-${TAAL}-noexplanation.mp4
fi
