from django.db import models

"""Schema for current data stories - feel free to add new ones, this is as
modular as you need it to be - just update this + views.py + urls.py to point
to the proper html file and ensure they connect, but pretty simple to modify - you
can inject into this however you like, I've made a script for this one you can
find in the main Scripts folder - note, this Schema can be made more complicated, 
up to future developers - for now, it's a simple get/set schema which does the job well and
creates any datastory of 4 paragraphs and a title"""
class DataStories(models.Model):
    infographicName = models.TextField()
    infographicIntro = models.TextField()
    infographicMiddle = models.TextField()
    infographicEnd = models.TextField()
    infographicExtra = models.TextField(blank=True)
