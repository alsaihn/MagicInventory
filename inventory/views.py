from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.encoding import smart_unicode

import simplejson
from BeautifulSoup import BeautifulSoup 

from models import *

def render_to_json(j):
    response = HttpResponse()
    response.write('%s' % simplejson.dumps(j))
    response['Content-length'] = str(len(response.content))
    response['Content-Type'] = 'text/plain'
    return response


def get_set_list(request):
    sets = Set.objects.all().order_by('block')
    return render_to_response('set-list.html', RequestContext(request,{'sets': sets}))

def get_set(request, id):
    set = Set.objects.get(pk=id)
    return render_to_response('card-list.html', RequestContext(request,{'set': set}))

def add_set(request):
    set_name = request.POST['name']
    set_block = request.POST['block']
    set = Set(name=set_name, block=set_block)
    set.save()
    return render_to_json({'success': 'true'})

def get_card(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render_to_response('card.html', RequestContext(request,{'card': card}))

def add_card(request, card_id, count=1):
    count = int(count)
    card = Card.objects.get(pk=card_id)
    card.count = card.count + count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def subtract_card(request, card_id, count=1):
    count = int(count)
    card = Card.objects.get(pk=card_id)
    card.count = card.count - count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def add_foil(request, card_id, count=1):
    count = int(count)
    card = Card.objects.get(pk=card_id)
    card.foil_count = card.foil_count + count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def subtract_foil(request, card_id, count=1):
    count = int(count)
    card = Card.objects.get(pk=card_id)
    card.foil_count = card.foil_count - count
    card.save()
    return redirect(request.META['HTTP_REFERER'])
    
def add_card_alt(request, card_id, count=1):
    count = int(count)
    card = AlternateArtCard.objects.get(pk=card_id)
    card.count = card.count + count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def subtract_card_alt(request, card_id, count=1):
    count = int(count)
    card = AlternateArtCard.objects.get(pk=card_id)
    card.count = card.count - count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def add_foil_alt(request, card_id, count=1):
    count = int(count)
    card = AlternateArtCard.objects.get(pk=card_id)
    card.foil_count = card.foil_count + count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def subtract_foil_alt(request, card_id, count=1):
    count = int(count)
    card = AlternateArtCard.objects.get(pk=card_id)
    card.foil_count = card.foil_count - count
    card.save()
    return redirect(request.META['HTTP_REFERER'])

def create_card_alt(request, card_id):    
    card = Card.objects.get(pk=card_id)
    alt = AlternateArtCard(card=card)
    alt.save()
    return redirect(request.META['HTTP_REFERER'])    

def delete_card_alt(request, alt_id):
    alt = AlternateArtCard(pk=alt_id)
    alt.delete()
    return redirect(request.META['HTTP_REFERER'])

def update_alt_notes(request, alt_id):
    alt = AlternateArtCard.objects.get(pk=alt_id)
    alt.notes = request.POST['notes']
    alt.save()
    return redirect('/card/' + str(alt.card.id))

def import_card_list(request, set_id):
    file = request.FILES["set_file"]
    set = Set.objects.get(pk=set_id)
    html_blob = file.read()
    soup = BeautifulSoup(html_blob)
    
    cardstart = soup.find('table', "cardItemTable")
    cards = cardstart.findAllNext('table')
    
    for index, c in enumerate(cards):
        card = Card()
        #print c.prettify()
        card.name = c.find('span', 'cardTitle').a.string
        card.description = c.find('div', 'rulesText').p.string
        
        type_line = c.find('span', 'typeLine')
        card.type = type_line.string.split('(')[0].strip(' \t\n\r')

        print card.type.encode('ascii', 'replace')
        card.collector_number = index
        
        mana_images = c.find('span', 'manaCost').findAll('img')
        mana_string = ""
        for m in mana_images:
            mana_string = mana_string + m['alt'] + " "
        	
        card.mana_cost = mana_string
        print card.mana_cost.encode('ascii', 'replace')
        
        version = c.find('td', 'setVersions').find('img')
        card.rarity = version['title'].split('(')[1].strip(')')
        print card.rarity.encode('ascii', 'replace')
        
        pt = type_line.string.split('(')
        if len(pt) > 1:
            if "Planeswalker" in card.type:
        	card.loyalty = type_line.string.split('(')[1].strip(')')
            else:
        	card.power = type_line.string.split('(')[1].split('/')[0].strip(')')
        	print card.power
        	
        	card.toughness = type_line.string.split('(')[1].split('/')[1].strip(')')
        	print card.toughness
        
        card.save()
        card.sets.add(set)
        
        link = Link()
        link.url = "http://gatherer.wizards.com/Pages" + c.find('td', 'leftCol').find('a')['href'].strip('.')
        link.link_text = "Gatherer"
        link.card = card
        link.save()
                
        print card.name
    
    return redirect('/set/' + set_id)
    

    

