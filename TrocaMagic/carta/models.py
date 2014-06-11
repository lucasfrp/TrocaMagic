from django.db import models

class TypeSet(models.Model):
    type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.type

class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10)
    gathererCode = models.CharField(max_length=10)
    oldCode = models.CharField(max_length=10)
    releaseDate = models.DateField()
    border = models.CharField(max_length=25, null=True)
    type = models.ForeignKey(TypeSet)
    block = models.CharField(max_length=50)
    booster = models.TextField()
    def __unicode__(self):
        return self.name

class Layout(models.Model):
    layout = models.CharField(max_length=50)
    def __unicode__(self):
        return self.layout

class Color(models.Model):
    color = models.CharField(max_length=10)
    simbol = models.CharField(max_length=3)
    def __unicode__(self):
        return self.color

class Supertype(models.Model):
    supertype = models.CharField(max_length=50)
    def __unicode__(self):
        return self.supertype

class Type(models.Model):
    type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.type

class Subtype(models.Model):
    subtype = models.CharField(max_length=50)
    def __unicode__(self):
        return self.subtype
    
class Rarity(models.Model):
    rarity = models.CharField(max_length=50)
    def __unicode__(self):
        return self.rarity
    
class Artist(models.Model):
    artist = models.CharField(max_length=100)
    def __unicode__(self):
        return self.artist

class Card(models.Model):
    set = models.ForeignKey(Set)
    layout = models.ForeignKey(Layout)
    name = models.CharField(max_length=200)
    manaCost = models.CharField(max_length=50)
    cmc = models.IntegerField(null=True)
    colors = models.ManyToManyField(Color)
    type = models.CharField(max_length=100)
    supertypes = models.ManyToManyField(Supertype)
    types = models.ManyToManyField(Type)
    subtypes = models.ManyToManyField(Subtype)
    rarity = models.ForeignKey(Rarity)
    text = models.TextField(null=True)
    flavor = models.TextField(null=True)
    artist = models.ForeignKey(Artist)
    number = models.CharField(max_length=10, null=True)
    power = models.CharField(max_length=5, null=True)
    toughness = models.CharField(max_length=5, null=True)
    loyalty = models.IntegerField(null=True)
    multiverseid = models.IntegerField(null=True)
    imageName = models.CharField(max_length=100)
    watermark = models.CharField(max_length=50)
    border = models.CharField(max_length=50, null=True)
    hand = models.IntegerField(null=True)
    life = models.IntegerField(null=True)
    variations = models.CharField(max_length=100, null=True)
    class Meta:
        unique_together = ('set', 'name')
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.set.name)
    
class NamesCard(models.Model):
    nome = models.CharField(max_length=100)
    carta = models.ForeignKey(Card)