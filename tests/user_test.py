import logging

from app import db
from app.db.models import User, Song
from faker import Faker

def test_adding_user(application, client):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('cj236@njit.edu', 'testtest')
        #add it to get ready to be committed
        db.session.add(user)

        resp = client.post('/login', data=dict(email="cj236@njit.edu", password='testtest'), follow_redirects=True)
        assert resp.status_code == 200
        assert b"Welcome" in resp.data

        #call the commit
        #db.session.commit()
        #assert that we now have a new user
        #assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='cj236@njit.edu').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'cj236@njit.edu'
        #this is how you get a related record ready for insert
        user.songs= [Song("test","smap", 1998, "Alternative"),Song("test2","te", 2007, "Rock")]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0