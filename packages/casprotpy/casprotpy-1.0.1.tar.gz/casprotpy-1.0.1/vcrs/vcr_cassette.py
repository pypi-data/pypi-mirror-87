import os
import vcr
from vcrs.vcr_timer import vcr_timer

class vcr_cassette:
    @classmethod
    def use(cls, file_path: str, block):
        cls.validate_cassette(file_path)

        with vcr.use_cassette(file_path, record_mode='new_episodes'):
            return block()

    @classmethod
    def validate_cassette(cls, file_path):
        if cls.cassette_exists(file_path) and vcr_timer.is_cassette_expired(file_path):
            cls.remove_cassette(file_path)

    @classmethod
    def cassette_exists(cls, file_path):
        return os.path.exists(file_path)

    @classmethod
    def remove_cassette(cls, file_path):
        os.remove(file_path)
