import sys, traceback
import atexit
from Digo import DigoCore

isCrash = False

def check_crash(exc_type, exc_value, exc_traceback):
	global isCrash
	isCrash = True
	traceback.print_exception(exc_type, exc_value, exc_traceback)

def exit_process(stateUpdate, experimentFinished):
	if isCrash is True:
		stateUpdate(2)
		experimentFinished(2)

		print("Digo Exit(1)")
	else:
		stateUpdate(1)
		experimentFinished(1)

		print("Digo Exit(0)")




sys.excepthook = check_crash
