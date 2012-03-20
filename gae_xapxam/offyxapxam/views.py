from django.template import RequestContext, loader
from google.appengine.ext.webapp import template
from django.http import HttpResponse
from gae_xapxam.offyxapxam.ext.response import JSONResponse
from django.http import HttpRequest
from gae_xapxam.offyxapxam import models

# Create your views here.

def json(request, data):
    t = loader.get_template('json.html')
    c = RequestContext(request, {
        'message': data,
    })
    return HttpResponse(t.render(c))

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, {
        'message': 'Welcome to ANCHOI service of ITDev..',
    })
    return HttpResponse(t.render(c))

def shuffleDeck(request):
    from random import shuffle

    cards = range(1, 53)
    shuffle(cards)

    deck = models.Deck(cards=cards)
    deck.put()

    response_data = {
        'deckID': deck.key(),
        #'deck': deck.cards
    }
    return JSONResponse(response_data)

def getRandomSet(request):
    from random import shuffle

    cards = range(1, 53)
    shuffle(cards)

    response_data = {
        'deckID': 'random',
        'cards': cards[:13]
    }
    return json(request, response_data)#JSONResponse(response_data)

def getDeck(request, deckKey=None):
    if deckKey:
        deck = models.Deck.get(deckKey)
    else:
        deck = models.Deck.all().order('-created_on')[0]
    response_data = []

    if deck:
        response_data = {
            'deckID': deck.key(),
            'deck': deck.cards
        }

    return JSONResponse(response_data)

def getStatus(request):
    deck = models.Deck.all().order('-created_on')[0] #Get last Deck
    response_data = []

    if deck:
        response_data = {
            'deckID': deck.key(),
            #'deck': deck.cards
        }

    return JSONResponse(response_data)

def getSet(request, setKey=None):
    set = models.Set.get(setKey)
    response_data = []

    if set:
        response_data = {
            'clientIP': getClientIP(request),
            'deckID': set.deck,
            'cards': set.cards
        }

    return JSONResponse(response_data)

def getSetFromDeck(request, deckKey=None):
    deck = models.Deck.get(deckKey)
    set = models.Set(position=0)

    if deck:
        qSet = models.Set.all()
        qSet.filter("deck =", deck)
        qSet.filter("clientIP =", getClientIP(request))

        # if client has gotten the set
        if qSet.count() > 0:
            set = qSet[0]
        else:
            count = deck.set_set.count()
            # if client still can get a set
            if count < 4:
                set = models.Set(deck=deck, clientIP=getClientIP(request), cards=deck.cards[count*13:(count+1)*13], position=count+1)
                set.put()

        response_data = {
            'position': set.position,
            'clientIP': set.clientIP,
            'deckID': deck.key(),
            'cards': set.cards
        }

    return JSONResponse(response_data)

def getClientIP(request):
    try:
        client_address = request.META['HTTP_X_FORWARDED_FOR']
    except:
        # case localhost ou 127.0.0.1
        client_address = request.META['REMOTE_ADDR']

    return client_address