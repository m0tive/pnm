#!/bin/bash

#mkdir $1 && echo "# keep me" > $1/__init__.py
if [ -e pywav/events/$1.py ] ; then
	echo "Event already exists"
else 
	echo -e "\ndef e(app, maker, data):\n\tapp.log.debug(\"$1 fired\")\n\treturn True" > pywav/events/$1.py
	echo "pywav/events/$1.py"
fi
