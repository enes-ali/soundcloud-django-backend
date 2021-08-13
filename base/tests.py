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
            password="Enes123", name="Enes", surname="Karakobak", age=17, gender=Account.MALE,
            location_node_id=246853179)

        ## Create artist /* Profile */
        artist = Artist.objects.create(account=account, profile_photo=profile_photo_file,
        banner=banner_file, description="test account")

        ## Create Track and TrackGenre
        date = datetime.datetime.now()
        genre = TrackGenre.objects.create(name="Deep House")
        track = Track.objects.create(artist=artist, title="Uletay (feat. VERA)", 
            source=track_file, duration=3, cover=cover_file, upload_date=date, genre=genre, tag="Deep",
            description="My new Track!")

        ## Creare comments
        new_comment = TrackComment.objects.create(account=account, track=track, content="Love it!",
            time=1.25, replied_to=None, date=None)

        reply_comment = TrackComment.objects.create(account=account, track=track, content="Me To!",
        time=1.25, replied_to=new_comment, date=None)

        reply_to_reply_comment = TrackComment.objects.create(account=account, track=track, content="I love it to!",
        time=1.25, replied_to=reply_comment, date=None)

        ## Create Playlist
        playlist_cover_file = ImageFile(open(base_path + "/playlist_cover.jpeg", "rb"), "playlist_cover.jpg")
        playlist = Playlist.objects.create(account=account, title="Best Playlist", cover=playlist_cover_file,
            description="fresh playlist", tags="chill fresh")
        playlist.tracks.add(track)

        ## Create Reposts
        repost_account = Account.objects.create_user(email="reposter@gmail.com", username="RepostMaster",
            password="repost123", name="Re", surname="Post", age=25, gender=Account.MALE,
            location_node_id=246818179)
        track_repost = Repost.objects.create(account=repost_account, track=track)
        playlist_repost = Repost.objects.create(account=repost_account, playlist=playlist)

        ## Create Play
        play = Play.objects.create(account=account, track=track, date=datetime.datetime.now())
        play.play()

    def test_artist(self):
        print("Test artist creation", "\n")
        account = Account.objects.get(username="LastShoot")
        self.assertNotEqual(account, None)
        self.assertNotEqual(account.profile, None)

    def test_genre(self):
        print("Test genre creation", "\n")
        genre = TrackGenre.objects.get(name="Deep House")

        self.assertNotEqual(genre, None)

    def test_track(self):
        print("Test track creation", "\n")
        track = Track.objects.get(title="Uletay (feat. VERA)", artist=1)

        self.assertNotEqual(track, None)
        self.assertEqual(track.duration, 190.584) # test duration function
        
    def test_track_like(self):
        print("Test track liking", "\n")
        track = Track.objects.get(title="Uletay (feat. VERA)", artist=1)
        account = Account.objects.get(username="LastShoot")
        account.profile.liked_tracks.add(track)
        
        self.assertEqual(account.profile.liked_tracks.get(title="Uletay (feat. VERA)"), track)
        self.assertEqual(track.likes.count(), 1)

        
    def test_track_comment(self):
        print("Test track comment creation", "\n")
        new_comment = TrackComment.objects.get(content="Love it!")
        
        self.assertEqual(new_comment.content, "Love it!")


    def test_track_comment_reply(self):
        print("Test replying to track comment", "\n")
        new_comment = TrackComment.objects.get(content="Love it!")
        reply_comment = TrackComment.objects.get(content="Me To!")
        
        try:
            reply_to_reply_comment = TrackComment.objects.get(content="I love it to!")
        except ObjectDoesNotExist as e:
            reply_to_reply_comment = None

        self.assertEqual(reply_comment.content, "Me To!")
        self.assertEqual(reply_to_reply_comment, None)


    def test_playlist(self):
        print("Test playlist creation", "\n")
        try:
            playlist = Playlist.objects.get(title="Best Playlist")
        except ObjectDoesNotExist as e:
            playlist = None

        self.assertNotEqual(playlist, None)
        
    def test_playlist_like(self):
        print("Test playlist liking", "\n")
        playlist = Playlist.objects.get(title="Best Playlist")
        account = Account.objects.get(username="LastShoot")
        account.profile.liked_playlists.add(playlist)
        
        self.assertEqual(account.profile.liked_playlists.get(title="Best Playlist"), playlist)
        self.assertEqual(playlist.likes.count(), 1)


    def test_repost(self):
        print("Test repost creation", "\n")
        repost_account = Account.objects.get(email="reposter@gmail.com")
        track = Track.objects.get(title="Uletay (feat. VERA)")
        playlist = Playlist.objects.get(title="Best Playlist")

        try:
            track_repost = Repost.objects.get(account=repost_account, track=track)
        except ObjectDoesNotExist as e:
            track_repost = None

        try:
            playlist_repost = Repost.objects.get(account=repost_account, playlist=playlist)
        except ObjectDoesNotExist as e:
            playlist_repost = None

        self.assertNotEqual(track_repost, None)
        self.assertNotEqual(playlist_repost, None)

        
    def test_repost_none(self):
        print("Test repost creation with track and playlist None", "\n")
        repost_account = Account.objects.get(email="reposter@gmail.com")
        
        try:
            repost_none = Repost.objects.create(account=repost_account)
        except Exception as e:
            print("\t" + str(e), "\n")
            repost_none = None

        self.assertEqual(repost_none, None)


    def test_repost_both(self):
        print("Test repost creation with track and playlist Not None", "\n")
        repost_account = Account.objects.get(email="reposter@gmail.com")
        track = Track.objects.get(title="Uletay (feat. VERA)")
        playlist = Playlist.objects.get(title="Best Playlist")

        try:
            repost_both = Repost.objects.create(account=repost_account, track=track, playlist=playlist)
        except Exception as e:
            print("\t" + str(e), "\n")
            repost_both = None

        self.assertEqual(repost_both, None)
        
    
    def test_plays_by_account(self):
        print("Test plays by account", "\n")
        account = Account.objects.get(username="LastShoot")
        track = Track.objects.get(title="Uletay (feat. VERA)")
        
        play, is_created = Play.objects.get_or_create(account=account, track=track, date=datetime.datetime.now())
        self.assertEqual(is_created, False)
        
        play.play()
        self.assertEqual(play.play_count, 2)
        

    def test_plays_by_date(self):
        print("Test plays by date", "\n")
        track = Track.objects.get(title="Uletay (feat. VERA)")
        date_today = datetime.datetime.now()

        play1, is_created = Play.objects.get_or_create(track=track, date=date_today, account=None)
        play1.play()

        play2, is_created = Play.objects.get_or_create(track=track, date=date_today, account=None)
        play2.play()
        
        play3, is_created = Play.objects.get_or_create(track=track, date=date_today, account=None)
        play3.play()
        
        play4, is_created = Play.objects.get_or_create(track=track, date=date_today, account=None)
        play4.play()

        todays_anonymous_plays = Play.objects.get(track=track, date=date_today, account=None)
        self.assertEqual(todays_anonymous_plays.play_count, 4)

        todays_all_plays = Play.objects.filter(track=track, date=date_today)
        todays_all_pcount = 0
        for play in todays_all_plays:
            todays_all_pcount += play.play_count
        self.assertEqual(todays_all_pcount, 5)

        self.assertEqual(track.plays.count(), 2)

