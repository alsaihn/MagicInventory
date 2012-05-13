import os
import settings
from django.db import models

# Create your models here.

RARITY_CHOICES=( ('Common', 'Common'), ('Uncommon','Uncommon'), ('Rare','Rare'), ('Mythic Rare', 'Mythic Rare') )
MANA_TYPE_CHOICES=(("Colorless", "Colorless"), ("White","White"), ("Blue", "Blue"), ("Black", "Black"), ("Red", "Red"), ("Green", "Green"), ("Artifact", "Artifact"), ("Land","Land"))

class Set(models.Model):

    def get_image_path(instance, filename):
		path = 'set_icons/' + filename
		return path

    name = models.CharField(max_length=255)
    block = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    
    def __str__(self):
        return self.name
                
    
class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.TextField()
    rarity = models.CharField(choices=RARITY_CHOICES, default='Common', max_length=20)
    collector_number = models.IntegerField(null=True, blank=True)
    mana_cost = models.CharField(max_length=10, null=True, blank=True)
    power = models.CharField(max_length=2, null=True, blank=True)
    toughness = models.CharField(max_length=2, null=True, blank=True)
    loyalty = models.CharField(max_length=2, null=True, blank=True)
    
    count = models.IntegerField(default=0)
    foil_count = models.IntegerField(default=0)
    
    sets = models.ManyToManyField(Set, null=True)
    
    def __str__(self):
        return self.name
        
    def missing(self):
        return 4-self.count
        
    def get_color(self):
    	pass
        
class AlternateArtCard(models.Model):
    card = models.ForeignKey(Card)
    notes = models.CharField(max_length=255)
    
    count = models.IntegerField(default=0)
    foil_count = models.IntegerField(default=0)
        
    def missing(self):
        return 4-self.count
    
class Link(models.Model):
    url = models.CharField(max_length=500)
    link_text = models.CharField(max_length=255)
    card = models.ForeignKey(Card)


from django.forms import ModelForm

class CardForm(ModelForm):
	class Meta: 
		model = Card
		
class SetForm(ModelForm):
	class Meta: 
		model = Set