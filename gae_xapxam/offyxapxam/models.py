from google.appengine.ext import db

# Create your models here.

class Deck(db.Model):
    cards = db.ListProperty(int)
    created_on = db.DateTimeProperty(auto_now_add = 1)
    created_by = db.UserProperty()

    def __str__(self):
        return '%s' % str(self.cards)

    def get_absolute_url(self):
        return '/deck/%s/' % self.key()

class Set(db.Model):
    deck = db.ReferenceProperty(Deck)
    cards = db.ListProperty(int)
    clientIP = db.StringProperty()
    position = db.IntegerProperty()

    def __str__(self):
        return '%s' % str(self.cards)

    def get_absolute_url(self):
        return '/set/%s/' % self.key()