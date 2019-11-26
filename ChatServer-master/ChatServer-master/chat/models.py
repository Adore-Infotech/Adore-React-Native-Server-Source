import os
import magic
import uuid
from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from django.core.exceptions import ValidationError

def validate_is_image(file):
    valid_mime_types = ['image/jpeg','image/png']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.jpg','.jpeg','.png']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Unacceptable file extension.')

def path_and_rename(instance, filename):
    
    if type(instance)==type(UserProfile()):
        upload_to = 'UserProfileImg'
            
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}-{}.{}'.format(instance.pk,uuid.uuid4().hex, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class UserProfile(models.Model):

    User = models.OneToOneField(User,on_delete=models.CASCADE,blank=False, null=False)
    ProfileImg = models.FileField(upload_to=path_and_rename, validators=(validate_is_image,),blank=True, null=True)
    LastSeen = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profiles'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return str(self.User.get_full_name())
    
class Rooms(PolymorphicModel):
    RoomID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class DirectRooms(Rooms):
    User1 = models.ForeignKey(User,models.PROTECT,related_name="user1")
    User2 = models.ForeignKey(User,models.PROTECT,related_name="user2")

    class Meta:
        unique_together = ('User1', 'User2',)

class GroupRooms(Rooms):
    RoomName = models.CharField("Room Name",max_length=250)
    Members = models.ManyToManyField(User,related_name="members")
    AdminMembers = models.ManyToManyField(User,related_name="adminmembers")

class Messages(PolymorphicModel):
    
    MSG_TEXT = 'text'
    MSG_IMAGE = 'image'
    MSG_VIDEO = 'video'
    MSG_AUDIO = 'audio'
    MSG_FILE = 'file'

    EVENT_ADD_USER = 'adduser'
    EVENT_REMOVE_USER = 'removeuser'
    EVENT_AUDIO_CALL = 'audiocall'
    EVENT_VIDEO_CALL = 'videocall'
    

    MESSAGE_TYPES = [
        (MSG_TEXT, 'Text'),
        (MSG_IMAGE, 'Image'),
        (MSG_VIDEO, 'Video'),
        (MSG_AUDIO, 'Audio'),
        (MSG_FILE, 'File'),

        (EVENT_ADD_USER, 'Add User'),
        (EVENT_REMOVE_USER, 'Add User'),
        (EVENT_AUDIO_CALL, 'Audio Call'),
        (EVENT_VIDEO_CALL, 'Video Call'),
        

    ]

    MessageID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Sender = models.ForeignKey(User,models.DO_NOTHING)
    Room = models.ForeignKey(Rooms,models.DO_NOTHING)
    MessageType = models.CharField("Message Type",max_length=50,choices=MESSAGE_TYPES)
    CreatedOn = models.DateTimeField(auto_now_add=True,db_index=True)

class TextMessage(Messages):
    Content = models.TextField()

class MediaMessage(Messages):
    Media = models.FileField()

class CallsLog(Messages):

    StartedAt = models.DateTimeField(auto_now_add=True)
    AnsweredAt = models.DateTimeField(null=True,blank=True)
    EndedAt = models.DateTimeField(null=True,blank=True)
    Duration = models.IntegerField(null=True,blank=True)

