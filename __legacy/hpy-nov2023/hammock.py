
"""
hamlib
cool tools fr
"""


from dask import dataframe as dd
from pathlib import Path
from kit import core as kit

msg = kit.Radio()

if __name__ == "__main__":
    
    msg.status(message='hamlib ~ hammads open code toolkit')