#! /bin/bash
for number in {1..5}
do
    damine data upload --dataset-name ugc_video_highlights_20180926 --data-info-json data_info_$number.json --processes 4 --retry 2
done
exit 0
