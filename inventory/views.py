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
    sets = Set.objects.all()
    return render_to_response('set-list.html', RequestContext(request,{'sets': sets}))

def get_set(request, id):
    set = Set.objects.get(pk=id)
    return render_to_response('card-list.html', RequestContext(request,{'set': set}))

def add_set(request):
    set_name = request.POST['name']
    set = Set(name=set_name)
    set.save()
    return render_to_json({'success': 'true'})

def get_card(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render_to_response('card.html', RequestContext(request,{'card': card}))

def add_card(request, set_id, card_id):
    card = Card.objects.get(pk=card_id)
    card.count = card.count + 1
    card.save()
    return redirect('/set/' + set_id)

def subtract_card(request, set_id, card_id):
    card = Card.objects.get(pk=card_id)
    card.count = card.count - 1
    card.save()
    return redirect('/set/' + set_id)

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
        	card.power = int(type_line.string.split('(')[1].split('/')[0])
        	print card.power
        	
        	card.toughness = int(type_line.string.split('(')[1].split('/')[1].strip(')'))
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
    

    

