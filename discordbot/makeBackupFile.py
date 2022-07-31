import os
import shelve

backup = os.path.join(os.path.dirname(__file__), 'backup')

with shelve.open(backup, 'c') as db:
    pass
