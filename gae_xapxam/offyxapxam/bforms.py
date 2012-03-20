from django import newforms as forms
import models
from google.appengine.ext.db import djangoforms

class DeckForm(djangoforms.ModelForm):
    class Meta:
        model = models.Deck
        exclude = ['created_by']