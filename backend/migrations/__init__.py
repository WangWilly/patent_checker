import os
import sys

this_dir = os.path.dirname(__file__)

# TODO: use https://stackoverflow.com/questions/35064426/when-would-the-e-editable-option-be-useful-with-pip-install instead
sys.path.insert(0, os.path.abspath(os.path.join(this_dir, "..")))
