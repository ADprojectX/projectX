from django.core.management.base import BaseCommand
import subprocess
import time
import os
from django.conf import settings

dis_bot_path = os.path.join(settings.BASE_DIR, 'utility', 'dis_bot.py')

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Command(BaseCommand):
    help = 'Starts the Discord bot'

    def handle(self, *args, **options):
        subprocess.Popen(["python", dis_bot_path])
        # keep the main process running in a while loop
        while True:
            time.sleep(1)
