from django.db import models, transaction, IntegrityError, OperationalError
from django.contrib.auth import get_user_model
from time import sleep
import uuid


BUFFER = 12
User = get_user_model()

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    voice = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.topic}'


class Script(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    script_data = models.JSONField()

    class Meta:
        # Add a unique constraint for the combination of 'request', 'prompt', and 'folder'
        unique_together = ['request']


class PendingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.CharField(max_length=255, null=True)  # Set a key length for the unique index
    folder = models.CharField(max_length=255, null=True)  # Set a key length for the unique index
    request = models.ForeignKey(Request, on_delete=models.CASCADE, unique=False)
    class Meta:
        # Add a unique constraint for the combination of 'request', 'prompt', and 'folder'
        unique_together = ('request', 'prompt', 'folder')

    @classmethod
    def has_less_than_buffer_entries(cls):
        num_tasks = cls.objects.count()
        # Check if the number of tasks is less than 13
        return num_tasks < BUFFER

    @classmethod
    def create_pending_task(cls, request, prompt=None, folder=None):
        # Wait until there's room in the buffer
        while not cls.has_less_than_buffer_entries():
            sleep(5)  # Wait for 5 seconds before checking again
        if cls.has_less_than_buffer_entries():
            if cls.objects.filter(request=request, prompt=prompt, folder=folder).exists():
                # Handle the case where a duplicate entry already exists
                raise Exception("PendingTask with the same request, prompt, and folder already exists.")
            else:
                with transaction.atomic():
                    created = cls.objects.create(request=request, prompt=prompt, folder=folder)
                    return created
        else:
            # Implement waiting logic or raise an exception to handle the situation when the buffer is full
            raise Exception("Buffer is full. Please wait and retry later.")

class ProjectAssets(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    asset_path = models.JSONField()

    class Meta:
        db_table = "project_assets"

    # only for first attempt
    def add_first_scene(self, scene_name, img_path, audio_path):
        # Add a new scene to the asset_path field
        if "asset_path" not in self.__dict__ or self.asset_path is None:
            self.asset_path = {}
        if scene_name not in self.asset_path:
            self.asset_path[scene_name] = {"img_path": {"retry0": [img_path]}, "audio_path": {self.request.voice: audio_path}}
        else:
            return
        self.save()
        # else:
        #     scene_data = self.asset_path[scene_name]
        #     img_retry_count = len(scene_data["img_path"])  # Get the current number of image retries
        #     scene_data["img_path"][f"retry{img_retry_count}"] = [img_path]

            # You may want to handle audio retries similarly if needed

        # self.asset_path[scene_name] = {"img_path": {"retry0":[img_path]}, "audio_path": {Request.voice:audio_path}}


# # Assuming you have a Request instance called `request_instance`
# project_assets = ProjectAssets(request=request_instance)
# project_assets.add_scene("scene0", img_path="path/to/img0.jpg", audio_path="path/to/audio0.mp3")
# project_assets.add_scene("scene1", img_path="path/to/img1.jpg", audio_path="path/to/audio1.mp3")
# # Add more scenes as needed
