from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inventory.views.get_set_list'),
    
    url(r'^set/(?P<id>\d+)/$', 'inventory.views.get_set'),
    url(r'^set/(?P<set_id>\d+)/import/$', 'inventory.views.import_card_list'),
    url(r'^set/add/$', 'inventory.views.add_set'),
    
    url(r'^card/(?P<card_id>\d+)/add/$', 'inventory.views.add_card'),
    url(r'^card/(?P<card_id>\d+)/add/(?P<count>\d+)/$', 'inventory.views.add_card'),
    url(r'^card/(?P<card_id>\d+)/subtract/$', 'inventory.views.subtract_card'),
    url(r'^card/(?P<card_id>\d+)/subtract/(?P<count>\d+)/$', 'inventory.views.subtract_card'),
    
    url(r'^card/(?P<card_id>\d+)/addfoil/$', 'inventory.views.add_foil'),
    url(r'^card/(?P<card_id>\d+)/addfoil/(?P<count>\d+)/$', 'inventory.views.add_foil'),
    url(r'^card/(?P<card_id>\d+)/subtractfoil/$', 'inventory.views.subtract_foil'),
    url(r'^card/(?P<card_id>\d+)/subtractfoil/(?P<count>\d+)/$', 'inventory.views.subtract_foil'),
           
    url(r'^card/(?P<card_id>\d+)/addalt/$', 'inventory.views.add_card_alt'),
    url(r'^card/(?P<card_id>\d+)/addalt/(?P<count>\d+)/$', 'inventory.views.add_card_alt'),
    url(r'^card/(?P<card_id>\d+)/subtractalt/$', 'inventory.views.subtract_card_alt'),
    url(r'^card/(?P<card_id>\d+)/subtractalt/(?P<count>\d+)/$', 'inventory.views.subtract_card_alt'),
    
    url(r'^card/(?P<card_id>\d+)/addaltfoil/$', 'inventory.views.add_foil_alt'),
    url(r'^card/(?P<card_id>\d+)/addaltfoil/(?P<count>\d+)/$', 'inventory.views.add_foil_alt'),
    url(r'^card/(?P<card_id>\d+)/subtractaltfoil/$', 'inventory.views.subtract_foil_alt'),
    url(r'^card/(?P<card_id>\d+)/subtractaltfoil/(?P<count>\d+)/$', 'inventory.views.subtract_foil_alt'),
   
    
    url(r'^card/(?P<card_id>\d+)/$', 'inventory.views.get_card'),
    url(r'^card/(?P<card_id>\d+)/create_alt/$', 'inventory.views.create_card_alt'),
    
    url(r'^alt/(?P<alt_id>\d+)/update_notes/$', 'inventory.views.update_alt_notes'),
    url(r'^alt/(?P<alt_id>\d+)/delete/$', 'inventory.views.delete_card_alt'),
     
    # url(r'^MagicInventory/', include('MagicInventory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
