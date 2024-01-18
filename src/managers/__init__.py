import os
from dotenv import dotenv_values


for key in dotenv_values():
    os.environ.pop(key, None)
