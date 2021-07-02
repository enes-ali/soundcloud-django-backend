from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.files import File
import datetime
from django.conf import settings


class ModelTestCase(TestCase):
    
    def setUp(self):
        base_path = settings.MEDIA_ROOT + "/UnitTest"
        
        ### FILES ### 
        profile_photo_file = ImageFile(open(base_path + "/test_profile_photo.jpg", "rb"),
            "profile.jpg")
        banner_file = ImageFile(open(base_path + "/test_banner.jpg", "rb"),
            "banner.jpg")
        track_file = File(open(base_path + "/Ablaikan - Uletay (feat. VERA).mp3", "rb"),
            "Uletay (feat. VERA).mp3")
        cover_file = ImageFile(open(base_path + "/track_cover.jpg", "rb"),
            "cover.jpg")

        # Create user
        user = User.objects.create(username="TestAccount")
        user.set_password("test_account")
        user.save()

        ## Create artist
        artist = Artist.objects.create(account=user, nickname="Otnicka", profile_photo=profile_photo_file,
        banner=banner_file, description="test account", location="test location")

        ## Create Track
        date = datetime.datetime.now()
        Track.objects.create(artist=artist, title="Uletay (feat. VERA)", 
            source=track_file, duration=3, cover=cover_file, upload_date=date, genre="ELC")


    def test_artist(self):
        artist = Artist.objects.get(nickname="Otnicka")
        self.assertNotEqual(artist, None)

    def test_track(self):
        track = Track.objects.get(title="Uletay (feat. VERA)", artist=1)
        return self.assertNotEqual(track, None)