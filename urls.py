from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inventory.views.get_set_list'),
    
    url(r'^set/(?P<id>\d+)/$', 'inventory.views.get_set'),
    url(r'^set/(?P<id>\d+)/buylist/$', 'inventory.views.get_set_buylist'),
    url(r'^set/(?P<set_id>\d+)/import/$', 'inventory.views.import_card_list'),
    url(r'^set/add/$', 'inventory.views.add_set'),
    
    url(r'^card/change_count/$', 'inventory.views.change_card_count'),           
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
