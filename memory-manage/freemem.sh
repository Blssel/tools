#!/bin/sh


while true
do
	sync
	sync
	sync
	sync
	sync
	sync
	sync
	sync
	echo 3 > /proc/sys/vm/drop_caches
	echo 'Memeoy has been Freed Once Again'
  for (( i=1; i<=100; i++ )) 
  do
    free -m
    echo '-----------------------------------------------------------------------'
    sleep 24s
  done
done

	
