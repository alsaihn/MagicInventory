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
    sets = Set.objects.all().order_by('block', 'name')
    return render_to_response('set-list.html', RequestContext(request,{'sets': sets}))

def get_set(request, id):
    set = Set.objects.get(pk=id)
    return render_to_response('card-list.html', RequestContext(request,{'set': set, 'cards': set.card_set.all}))

def get_add_mode(request, id):
    set = Set.objects.get(pk=id)
    cards = set.card_set.exclude(count__gte=4)
    return render_to_response('card-list.html', RequestContext(request,{'set': set, 'cards': cards}))

def get_set_buylist(request, id):
    set = Set.objects.get(pk=id)    
    return render_to_response('buy-list.html', RequestContext(request,{'set': set, 'cards': set.card_set.all()}))

def add_set(request):
    set_name = request.POST['name']
    set_block = request.POST['block']
    set = Set(name=set_name, block=set_block)
    set.save()
    return render_to_json({'success': 'true'})

def get_card(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render_to_response('card.html', RequestContext(request,{'card': card}))

def search_cards(request):
	if request.GET.__contains__('s'):
		cards = Card.objects.filter(name__icontains=request.GET['s']).order_by("name")
		return render_to_response('results.html', RequestContext(request,{'cards': cards}))
	
	cards = Card.objects.none()
	return render_to_response('results.html', RequestContext(request, {'cards': cards}))
		

def change_card_count(request):
	id = request.GET['id']
	type = request.GET['type']
	count = request.GET['count']
	
	if 'alt' in type: 
		card = AlternateArtCard.objects.get(pk=id)
	else: 
		card = Card.objects.get(pk=id)
		
	if 'foil' in type:
		card.foil_count = card.foil_count + int(count)
	else:
	    card.count = card.count + int(count)
	    
	card.save()
	    
	return render_to_json({'id': card.id, 'type': type, 'count': card.count, 'foil_count': card.foil_count})

def create_card(request):
	if request.method == 'POST':
		form = CardForm(request.POST)
		if form.is_valid():
			form.save()
			
			new_form = CardForm()
			return render_to_response('new_card.html', RequestContext(request,{'form': new_form}))
		
	else:
		form = CardForm()
		
	return render_to_response('new_card.html', RequestContext(request,{'form': form}))

		

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

#fix mana by hand: 
# apocalypse, dissension, invasion, timeshifted: duel cards
# arabian nights: kaiso
# champions of kamigawa, tempest: (name) cards
# judgment, timeshifted: valor
# legends: Aerathi berserker
# oddessy, timeshifted: call of the herd

def import_card_list(request, set_id):
    file = request.FILES["set_file"]
    set = Set.objects.get(pk=set_id)
    html_blob = file.read()
    soup = BeautifulSoup(html_blob)
    
    cardstart = soup.find('table', "cardItemTable")
    cards = cardstart.findAllNext('table')
    
    for index, c in enumerate(cards):
        card = Card()
        card.name = c.find('span', 'cardTitle').a.string
        card.description = c.find('div', 'rulesText').p.string
        
        type_line = c.find('span', 'typeLine')
        card.type = type_line.string.split('(')[0].strip(' \t\n\r')

        print card.type.encode('ascii', 'replace')
        card.collector_number = index
        
        mana_images = c.find('span', 'manaCost').findAll('img')	
        mana = []
        for mp in mana_images:
			m = mp['alt']
			if len(m) > 1:
				m = m[0]
			mana.append(m)			
        mana = ' '.join(mana)
        
        card.mana_cost = mana
        print card.mana_cost.encode('ascii', 'replace')
        
        version = c.find('td', 'setVersions').find('img')
        card.rarity = version['title'].split('(')[1].strip(')')
        
        pt = type_line.string.split('(')
        if len(pt) > 1:
            if "Planeswalker" in card.type:
        	card.loyalty = type_line.string.split('(')[1].strip(')')
            else:
        	card.power = type_line.string.split('(')[1].split('/')[0].strip(')')
        	
        	card.toughness = type_line.string.split('(')[1].split('/')[1].strip(')')
        
        card.save()
        card.sets.add(set)
        
        link = Link()
        link.url = "http://gatherer.wizards.com/Pages" + c.find('td', 'leftCol').find('a')['href'].strip('.')
        link.link_text = "Gatherer"
        link.card = card
        link.save()
                
    return redirect('/set/' + set_id)
    
