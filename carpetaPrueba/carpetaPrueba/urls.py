from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', "prueba.views.nuevo_usuario"), #Esta es la ventana principal, desde la que se ejecutara la web
	url(r'^login', "prueba.views.login_view"),	
	url(r'^nuevo_usuario$', 'prueba.views.nuevo_usuario'),
        url(r'^logout$', 'prueba.views.logout_view'),
        url(r'^submit$', 'prueba.views.submit'), #publicar nuevo tweet
        url(r'^profesional/$', 'prueba.views.getPerfilProfesional'),
        url(r'^cargarInicio/$', 'prueba.views.index'),
        url(r'^buddies/$', 'prueba.views.getTweets'),
        url(r'^admin/', include(admin.site.urls))
        
    
)
 