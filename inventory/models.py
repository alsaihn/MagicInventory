from django.db import models

# Create your models here.

RARITY_CHOICES=( ('Common', 'Common'), ('Uncommon','Uncommon'), ('Rare','Rare'), ('Legendary', 'Legendary') )


class Set(models.Model):
    name = models.CharField(max_length=255)
    block = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name
    
class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    type = models.TextField()
    rarity = models.CharField(choices=RARITY_CHOICES, default='Common', max_length=20)
    collector_number = models.IntegerField(null=True)
    mana_cost = models.CharField(max_length=10, null=True)
    power = models.CharField(max_length=2, null=True)
    toughness = models.CharField(max_length=2, null=True)
    loyalty = models.CharField(max_length=2, null=True)
    
    count = models.IntegerField(default=0)
    foil_count = models.IntegerField(default=0)
    
    sets = models.ManyToManyField(Set, null=True)
    
    def __str__(self):
        return self.name
        
    def missing(self):
        return 4-self.count
        
class AlternateArtCard(models.Model):
    card = models.ForeignKey(Card)
    notes = models.CharField(max_length=255)
    
    count = models.IntegerField(default=0)
    foil_count = models.IntegerField(default=0)
    
class Link(models.Model):
    url = models.CharField(max_length=500)
    link_text = models.CharField(max_length=255)
    card = models.ForeignKey(Card)
