false
while [ $? -ne 0 ]; do sleep 5; $(python __version__.py); done
