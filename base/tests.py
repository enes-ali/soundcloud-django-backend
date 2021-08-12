from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.files import File
import datetime
from django.conf import settings
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist


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

        # Create Account
        account = Account.objects.create_user(email="enes@gmail.com", username="LastShoot",
            password="Enes123", name="Enes", surname="Karakobak", age=17, gender=Account.MALE, location_node_id=246853179)

        ## Create artist /* Profile */
        artist = Artist.objects.create(account=account, profile_photo=profile_photo_file,
        banner=banner_file, description="test account")

        ## Create Track and TrackGenre
        date = datetime.datetime.now()
        genre = TrackGenre.objects.create(name="Deep House")
        track = Track.objects.create(artist=artist, title="Uletay (feat. VERA)", 
            source=track_file, duration=3, cover=cover_file, upload_date=date, genre=genre, tag="Deep")

        ## Creare comments
        new_comment = TrackComment.objects.create(account=account, track=track, content="Love it!",
            time=1.25, replied_to=None, date=None)

        reply_comment = TrackComment.objects.create(account=account, track=track, content="Me To!",
        time=1.25, replied_to=new_comment, date=None)

        reply_to_reply_comment = TrackComment.objects.create(account=account, track=track, content="I love it to!",
        time=1.25, replied_to=reply_comment, date=None)

    def test_artist(self):
        account = Account.objects.get(username="LastShoot")
        self.assertNotEqual(account, None)
        self.assertNotEqual(account.profile, None)

    def test_genre(self):
        genre = TrackGenre.objects.get(name="Deep House")

        self.assertNotEqual(genre, None)

    def test_track(self):
        track = Track.objects.get(title="Uletay (feat. VERA)", artist=1)

        self.assertNotEqual(track, None)
        self.assertEqual(track.duration, 190.584) # test duration function
        
        
    def test_track_comment(self):
        new_comment = TrackComment.objects.get(content="Love it!")
        
        self.assertEqual(new_comment.content, "Love it!")


    def test_track_comment_reply(self):
        new_comment = TrackComment.objects.get(content="Love it!")
        reply_comment = TrackComment.objects.get(content="Me To!")
        
        try:
            reply_to_reply_comment = TrackComment.objects.get(content="I love it to!")
        except ObjectDoesNotExist as e:
            reply_to_reply_comment = None

        self.assertEqual(reply_comment.content, "Me To!")
        self.assertEqual(reply_to_reply_comment, None)

        
        
        
        
        
        

