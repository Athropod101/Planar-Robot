import sys
import importlib.util

# Check if Module is in sys.path and can be found
spec = importlib.util.find_spec("Systems")
if spec is not None:
    print("Module is importable")
else:
    print("Module is not importable")   
