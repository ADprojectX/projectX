from django.db import models, transaction
from django.contrib.auth import get_user_model
from time import sleep
import uuid

BUFFER = 12

User = get_user_model()

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    voice = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    final_video_asset = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.topic}'


class Script(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    script_scenes = models.JSONField(default=list)  # list of UUIDs
    current_scenes = models.JSONField(default=list)  # list of UUIDs

    class Meta:
        unique_together = ['request']

    def add_entire_script(self, script_list):
        self.request.final_video_asset = None
        self.request.save()
        if "script_scenes" not in self.__dict__ or self.script_scenes is None:
            self.script_scenes = []

        if "current_scenes" not in self.__dict__ or self.current_scenes is None:
            self.current_scenes = []

        self.current_scenes.clear()
        new_current_scenes = []
        for i, scene_uuid_str, narr, img in script_list:
            narration = narr
            img_desc = img if img else None
            # Get or create the scene, and check if it was created a new
            scene, created = Scene.objects.update_or_create(
                    id=uuid.UUID(scene_uuid_str) if scene_uuid_str else str(uuid.uuid4()),
                    defaults={
                        'narration': narration,
                        'image_desc': img_desc,
                        'script': self.request.id
                    }
                )
            new_current_scenes.append(str(scene.id))
            if created:
                # If the scene was created a new, add it to the relationships
                self.script_scenes.append(str(scene.id))
            self.save()
        
        self.current_scenes = new_current_scenes
        self.save()

    def get_current_script(self):
        cur_script = []
        for i, uuid in enumerate(self.current_scenes):
            try:

                scene = Scene.objects.get(id=uuid)
                cur_script.append([i, uuid, scene.narration])
            except Scene.DoesNotExist:
                # Handle the case where the scene does not exist
                cur_script.append([i])
                pass
        return cur_script

class Scene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    narration = models.TextField(null=True)
    image_desc = models.TextField(null=True)
    script = models.UUIDField()
    # script = models.OneToOneField(Script, on_delete=models.CASCADE, related_name='scenes')

    def get_script_id(self):
        return self.script

    def get_scene(self):
        return self.narration, self.image_desc

class ProjectAssets(models.Model):
    scene_id = models.OneToOneField(Scene, on_delete=models.CASCADE, primary_key=True, editable=False)
    asset_path = models.JSONField(null=True)
    currently_used_asset = models.JSONField(null=True)

    def get_scene_object(self):
        return self.scene_id

    def add_new_asset(self, **kwargs):
        script = self.get_scene_object().get_script_id()
        req = Request.objects.get(id=str(script))
        req.final_video_asset = None
        req.save()
        if self.asset_path is None:
            self.asset_path = {}
        if self.currently_used_asset is None:
            self.currently_used_asset = {}
        else:
            self.currently_used_asset.clear()
            self.currently_used_asset = {}
        for k, v in kwargs.items():
            self.asset_path.setdefault(k, []).append(v)
            self.currently_used_asset[k] = v
        self.save()

class PendingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.TextField(max_length=1000)  # Set a key length for the unique index
    folder = models.CharField(max_length=255)  # Set a key length for the unique index
    request = models.ForeignKey(Request, on_delete=models.CASCADE, unique=False)
    class Meta:
        # Add a unique constraint for the combination of 'request', 'prompt', and 'folder'
        unique_together = ('request', 'folder')

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
                if prompt and len(prompt) > 1000:
                # Truncate the prompt if it's too long
                    prompt = prompt[:1000]
                with transaction.atomic():
                    created = cls.objects.create(request=request, prompt=prompt, folder=folder)
                    return created
        else:
            # Implement waiting logic or raise an exception to handle the situation when the buffer is full
            raise Exception("Buffer is full. Please wait and retry later.")










########################################################################################################################################################################################################            
# SERVICES = {'image':['mjx', 'sdxl'],
#             'audio':['XIL'],
#             'music':['beatO','shutter'],
#             'avatar':[],
#             'imv':[],
#             'finalV':[]
#             }
# class Script(models.Model):
#     request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
#     script_data = models.JSONField()

#     class Meta:
#         # Add a unique constraint for the combination of 'request', 'prompt', and 'folder'
#         unique_together = ['request']



# class Scene(models.Model):
#     project_assets = models.ForeignKey('ProjectAssets', on_delete=models.CASCADE)
#     scene_name = models.CharField(max_length=100)
#     img_path = models.CharField(max_length=100)
#     audio_path = models.CharField(max_length=100)
#     music = models.CharField(max_length=100)
#     video = models.CharField(max_length=100)
#     prev_scene = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)

# class ProjectAssets(models.Model):
#     request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
#     # asset_path = models.JSONField(null=True)
#     currently_used_asset = models.JSONField(null=True)

#     class Meta:
#         db_table = "project_assets"

#     # only for first attempt
#     def add_first_scene(self, scene_name, img_path, audio_path):
#         # Add a new scene to the asset_path field
#         if "asset_path" not in self.__dict__ or self.asset_path is None:
#             self.asset_path = {}
#         if "currently_used_asset" not in self.__dict__ or self.currently_used_asset is None:
#             self.currently_used_path = {}
#         if scene_name not in self.asset_path:
#             self.asset_path[scene_name] = 1 #implement this
#             self.currently_used_asset[scene_name] = 1#implement this
#         else:
#             return
#         self.save()
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
