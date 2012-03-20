from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^random', 'gae_xapxam.offyxapxam.views.getRandomSet'),
    (r'^shuffle', 'gae_xapxam.offyxapxam.views.shuffleDeck'),
    (r'^status', 'gae_xapxam.offyxapxam.views.getStatus'),
    (r'^deck/(?P<deckKey>[^\.^/]+)/$', 'gae_xapxam.offyxapxam.views.getDeck'),
    (r'^cards/(?P<deckKey>[^\.^/]+)/$', 'gae_xapxam.offyxapxam.views.getSetFromDeck'),
    #(r'^set/(?P<setKey>[^\.^/]+)/$', 'gae_xapxam.offyxapxam.views.getSet'),
    (r'^$', 'gae_xapxam.offyxapxam.views.index'),
    #(r'^ajax/qualify','officience_xmltool.xmltool.views.qualify_service'),
    # url(r'^gae_xapxam/', include('gae_xapxam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
