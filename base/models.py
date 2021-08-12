from django.db import models
from .utils import get_duration
from django.conf import settings


def profilePhotoPath(instance, default_name):
    return f"Artists/{instance.account.username}/photos/profile/{default_name}"

def bannerPath(instance, default_name):
    return f"Artists/{instance.account.username}/photos/banner/{default_name}"

def trackSourcePath(instance, default_name):
    return f"Artists/{instance.artist.account.username}/tracks/{instance.title}/sources/{default_name}"

def trackCoverPath(instance, default_name):
    return f"Artists/{instance.artist.account.username}/tracks/{instance.title}/covers/{default_name}"



class Artist(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")  
    profile_photo = models.ImageField(upload_to=profilePhotoPath)
    banner = models.ImageField(upload_to=bannerPath)
    description = models.TextField(max_length=256)
    following = models.ManyToManyField("self", related_name='followers', blank=True)
    liked_tracks = models.ManyToManyField("base.Track", related_name="likes", blank=True)

    def __str__(self):
        return self.nickname


class Track(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=120)
    source = models.FileField(upload_to=trackSourcePath)
    duration = models.FloatField(editable=False)
    cover = models.ImageField(upload_to=trackCoverPath)
    upload_date = models.DateField(auto_now_add=True)
    genre = models.ForeignKey("base.TrackGenre", related_name="tracks", on_delete=models.CASCADE)
    tag = models.CharField(max_length=64)
    description = models.CharField(max_length=8000)

    def __str__(self):
        return self.title + "   " + self.artist.nickname
        
    
    def save(self, *args, **kwargs):
        self.duration = get_duration(self.source.file)
        super().save(*args, **kwargs)
    
    

    
class TrackComment(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="track_comments")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=600)
    time = models.FloatField()
    replied_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="replies")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.track.title + " By" + self.account.username
        
    def save(self, *args, **kwargs):
        # Check comment depth 
        if self.replied_to is not None and self.replied_to.replied_to is not None:
            return Exception("can't reply to a reply comment")

        super().save(*args, **kwargs)



class TrackGenre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name