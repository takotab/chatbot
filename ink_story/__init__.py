import os
import logging
import clr # pylint: disable=E0401
import codecs

path_engine = os.path.join(os.getcwd(), "ink", "ink-engine-runtime.dll")
ink_file = os.path.join(os.getcwd(), "ink", "current_inky.ink")
# ink_file = os.path.join(os.getcwd(), "ink", "alt_test_inky_tako.ink")
path_ink_json = ink_file + ".json"

command = 'mono ' + os.path.join(os.getcwd(),
                                 "ink", "inklecate.exe") + " " + ink_file
logging.info(command)
os.system(command)

clr.AddReference(path_engine)
with codecs.open(path_ink_json, 'r', 'utf-8-sig') as data_file:
    ink_json = data_file.read()
from Ink.Runtime import Story  # pylint: disable=E0401
