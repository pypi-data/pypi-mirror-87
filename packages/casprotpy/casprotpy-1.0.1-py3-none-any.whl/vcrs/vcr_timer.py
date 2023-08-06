import os
import time
from datetime import datetime

class vcr_timer:
    CASSETTE_MAX_DURATION = 8 # Hours

    @classmethod
    def is_cassette_expired(cls, file_path):
        return ((datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(os.stat(file_path).st_ctime)).total_seconds() / 3600) > cls.CASSETTE_MAX_DURATION
