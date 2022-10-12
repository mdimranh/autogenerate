from dotenv import load_dotenv
load_dotenv()

import os
SECRET_KEY = os.getenv("MY_SECRET")
DB_URL = os.getenv("DB_URL")