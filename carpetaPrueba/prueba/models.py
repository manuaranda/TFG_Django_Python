#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
import hashlib

 
class Cuenta(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    destinatario = models.CharField(max_length=140)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
	
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserCreate(models.Model):
    
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=200,verbose_name='LinkedIn')
    username = models.CharField(max_length=200,verbose_name='Twitter')
    password1 = models.CharField(max_length=200,verbose_name='Password')
    password2 = models.CharField(max_length=200,verbose_name='Password Confirmation')
    

   
class Authenti(models.Model) :
	
    username = models.CharField(max_length=200,verbose_name='Username')
    password = models.CharField(max_length=200,verbose_name='Password')
		
    def is_valid(self):
	form=super(AuthenticateForm,self).is_valid()
	for f,error in self.errors.iteritems():
		if f!= '_all_':
			self.fields[f].widget.attrs.update({'class':'error','value':strip_tags(error)})
	return form
    
class App(models.Model) :
	
    destinatario = models.CharField(max_length=200,verbose_name='Contenido')
 
    def is_valid(self):
	    form = super(AppForm, self).is_valid()
	    for f in self.errors.iterkeys():
		    if f != '__all__':
			    self.fields[f].widget.attrs.update({'class': 'error ribbitText'})
	    return form
	
class Coment(models.Model) :
	
    contenido = models.CharField(max_length=400,verbose_name='Comentario')
    
 
    def is_valid(self):
	    form = super(AppForm, self).is_valid()
	    for f in self.errors.iterkeys():
		    if f != '__all__':
			    self.fields[f].widget.attrs.update({'class': 'error ribbitText'})
	    return form
 
 
   
