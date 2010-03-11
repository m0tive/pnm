#!/bin/bash

SCRIPTDIR=scripts

#mkdir $1 && echo "# keep me" > $1/__init__.py
if [ ! -e $SCRIPTDIR/$1.py ] ; then
	echo -e "## Event function.\n#  @param eman - event manager\n#  @param data - information passed\n#  @return True if the event is successful\ndef e (eman, data):\n\t# event script...\n\t\n\treturn True" > $SCRIPTDIR/$1.py
	echo "$SCRIPTDIR/$1.py"
fi
