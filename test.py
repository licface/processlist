import sys
import traceback

try:
	print sys.argv[1]
except:
	traceback.format_exc()