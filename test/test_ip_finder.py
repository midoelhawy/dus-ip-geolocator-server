

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
print(sys.path)

from lib.db import DBHandler

db =  DBHandler()


x = db.resolve_ip('194.243.217.66');
print(x)