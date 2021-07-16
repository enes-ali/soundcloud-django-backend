from django.db import models
from .utils import get_duration
from django.conf import settings


def profilePhotoPath(instance, default_name):
    return f"Artists/{instance.nickname}/photos/profile/{default_name}"

def bannerPath(instance, default_name):
    return f"Artists/{instance.nickname}/photos/banner/{default_name}"

def trackSourcePath(instance, default_name):
    return f"Artists/{instance.artist.nickname}/tracks/{instance.title}/sources/{default_name}"

def trackCoverPath(instance, default_name):
    return f"Artists/{instance.artist.nickname}/tracks/{instance.title}/covers/{default_name}"



class Artist(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=80, unique=True)
    profile_photo = models.ImageField(upload_to=profilePhotoPath)
    banner = models.ImageField(upload_to=bannerPath)
    description = models.TextField(max_length=256)
    #TODO: Use a appropriate location field
    location = models.CharField(max_length=70, help_text="this is a placeholder, and will be changed with a location field")

    def __str__(self):
        return self.nickname


class Track(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="tracks")
    title = models.CharField(max_length=120)
    source = models.FileField(upload_to=trackSourcePath)
    duration = models.FloatField(editable=False)
    cover = models.ImageField(upload_to=trackCoverPath)
    upload_date = models.DateField(auto_now_add=True)
    
    ELECTRONIC = "ELC"
    COUNTRY = "CTR"
    HIP_HOP = "HPHP"
    ROCK = "RCK"
    JAZZ = "JAZZ"
    METAL = "MTL"
    POP = "POP"
    FUNK = "FUNK"
    GENRE_CHOICES = [
        (ELECTRONIC, "Electronic"),
        (COUNTRY, "Country"),
        (HIP_HOP, "Hip-Hop"),
        (ROCK, "Rock"),
        (JAZZ, "Jazz"),
        (METAL, "Metal"),
        (POP, "Pop"),
        (FUNK, "Funk")
    ]
    genre = models.CharField(max_length=4, choices=GENRE_CHOICES)

    def __str__(self):
        return self.title + "   " + self.artist.nickname
        
    
    def save(self, *args, **kwargs):
        self.duration = get_duration(self.source.file)
        super().save(*args, **kwargs)
    
    
    
    
    
    
    
        
        
