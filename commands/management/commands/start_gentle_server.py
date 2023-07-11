from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Starts the Gentle Server @ 8765'
    def handle(self, *args, **options):
        command = "docker run -d -p 8765:8765 lowerquality/gentle"
        subprocess.run(command, shell=True)

    # Call the function to start the Gentle Docker container
