#!/bin/bash

SCRIPTDIR=scripts

#mkdir $1 && echo "# keep me" > $1/__init__.py
if [ ! -e $SCRIPTDIR/$1.py ] ; then
	echo -e "## @file $SCRIPTDIR/$1.py\n#  @brief Script file, see $SCRIPTDIR.$1\n\n## @package $SCRIPTDIR.$1\n#  @brief \n\n#-------------------------------------------------------------------------------\n\n#from pnm.application import Application as App\n#from pnm.logger import Log\n\n## Event function.\n#  @param eman - event manager\n#  @param data - information passed\n#  @return True if the event is successful\ndef e (eman, data):\n  # event script...\n  \n  return True" > $SCRIPTDIR/$1.py
	echo "$SCRIPTDIR/$1.py"
fi
