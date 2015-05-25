from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from prueba.models import Cuenta, UserCreate, Authenti, App, Coment
from django.shortcuts import render_to_response, redirect , render
from django.contrib.auth import login, authenticate, logout
from prueba.forms import UserCreateForm, AuthenticateForm, AppForm, ComentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404



def index(request, auth_form=None,formulario=None):
    
    # usuario logueado
    if request.user.is_authenticated():
        user = request.user
	usuario = UserCreate.objects.all()
	buscar =AppForm()
	
        return render(request,'inicio.html',{'buscar':buscar,'user': user,'next_url': '/', 'datos': getBiografia(request,None),'tweets':getTweets(request)})
    else:
        # usuario aun sin logear
        auth_form = auth_form or AuthenticateForm()
        formulario =UserCreateForm()
	buscar =AppForm()
	
        return render(request,'home.html',{'auth_form': auth_form, 'formulario': formulario, 'buscar':buscar})

    
    
def login_view(request,user):
     
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
	    user=request.user
	    usuario = form.cleaned_data['username']
	    password = form.cleaned_data['password']	
	    try:
		linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=usuario)
		linkedin = linkedin[0]
		acceso = authenticate(username=usuario, password=password)	
		todos = Cuenta.objects.all().filter(destinatario=usuario)
	    except:
		fallo='Por favor introduzca un usuario y contraseña correctos.'
		acceso= None
	    if acceso is not None and acceso.is_active:	   
		login(request, acceso)
	    else:
		fallo='Por favor introduzca un usuario y contraseña correctos.'		
		log = AuthenticateForm()
		formulario = UserCreateForm()
		return render_to_response('home.html',{'fallo':fallo,'log': log, 'formulario': formulario,},context_instance=RequestContext(request),)
	    buscar =AppForm()
             #Success
            return render_to_response('inicio.html',{'buscar':buscar,'datos':getBiografia(request,linkedin),'tweets':getTweets(request,usuario),'linkedin': linkedin,'todos':todos},context_instance=RequestContext(request),)
        else:
            # Failure
	    fallo='Por favor introduzca un usuario y contraseña correctos. '
	    
	    log = AuthenticateForm()
	    formulario = UserCreateForm()
	 
            return render_to_response('home.html',{'fallo':fallo,'log': log, 'formulario': formulario,},context_instance=RequestContext(request),)


 
def logout_view(request):
    logout(request)
    return redirect('/')



@login_required
def submit(request,usuario):
    
    if request.method == "POST":
	formulario = ComentForm(data=request.POST)

        if formulario.is_valid() :	
	    user=request.user
	    buscar =AppForm()
	    linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=usuario)
	    linkedin = linkedin[0]	
            tweet = formulario.save(commit=False)
	    #usuario = formulario2.cleaned_data['destinatario']  
            tweet.user = request.user	    
	    tweet.destinatario = usuario
	    tweet.save()
	    comentario= ComentForm()
	    todos = Cuenta.objects.all().filter(destinatario=usuario)
    
            return render(request,'inicio.html',{'buscar':buscar,'user': user,'next_url': '/', 'datos': getBiografia(request,linkedin),'tweets':getTweets(request,usuario),'tweet':tweet,'todos':todos,'comentario':comentario})
        else:
            return redirect('/')
    return redirect('/')


	
def nuevo_usuario(request):
    
    if request.method == 'POST':
    
	formulario = UserCreateForm(data=request.POST)
	log = AuthenticateForm(data=request.POST)
	if formulario.is_valid():
	    try:
		username = formulario.cleaned_data['username']	
		password = formulario.cleaned_data['password2']
		email = formulario.cleaned_data['email']
		user = User.objects.create_user(username, email, password)		
		user.set_password(password)   
		formulario.save()
		user = authenticate(username=username, password=password)
		mensaje='Usuario registrado con exito.'
	    except:
		mensaje = 'El usuario ya existe.'
	    
	    return render_to_response('home.html',{'formulario':formulario,'log':log,'mensaje':mensaje},context_instance=RequestContext(request))
	    
	else:
	    formulario = UserCreateForm()
	    log = AuthenticateForm()	    
	    fallo2='Fallo en el registro, por favor compruebe que todos los campos sean correctos.'
	    
	    return render_to_response('home.html',{'formulario':formulario,'log':log,'fallo2':fallo2},context_instance=RequestContext(request))
	
    formulario = UserCreateForm()
    log = AuthenticateForm()
    return render_to_response('home.html',{'formulario':formulario,'log':log},context_instance=RequestContext(request))
	


def getTweets(request,usuario):
    tweets = []
    try:
	import twitter
    
	tweet_form = AppForm()

	api = twitter.Api(
	    consumer_key='HSAJYkJso2lx7nV9pHGITg',
	    consumer_secret='okILf2DfyyMrNq0JRvlEckNKFC3hFxei21X4NEcURHQ',
	    access_token_key='310810114-eIP0VTRmwJ6uMsBHWb6qzVgp77quUloV3KfGT2MY',
	    access_token_secret='w2U7z2XcrJHjRDpxMoD0b8lVdSCIMWkZyKckf7oiaHG11'
	)
	
	latest = api.GetUserTimeline(screen_name=usuario)
	user= api.GetUser(screen_name=usuario)
	descripcion = user.GetDescription()
	name = user.GetName()
	avatar = user.GetProfileImageUrl()
	imagen = user.GetProfileBannerUrl()
	location = user.GetLocation()
	union = user.GetCreatedAt()
	total=user.GetStatusesCount()
	seguidores=user.GetFollowersCount()
	amigos=user.GetFriendsCount()
	fav= user.GetFavouritesCount()
	
	for tweet in latest:
	    status = tweet.text
	    tweet_date = tweet.relative_created_at
	    tweets.append({'status': status, 'date': tweet_date})
	    
	
	    
    except:
	    tweets.append({'status': 'Follow us @ManuAranda9', 'date': 'about 10 minutes ago'})
	    
    return({'tweets':tweets,'usuario':usuario,'descripcion':descripcion,'avatar':avatar,'location':location,'union':union,'total':total,'name':name,'seguidores':seguidores,'amigos':amigos,'imagen':imagen,'fav':fav})
	    
    #return render_to_response('inicio.html',{'tweet_form': tweet_form, 'user': user,'tweets': tweets})
		

def getBiografia(request,usuario):
    
    try:
	from linkedin import linkedin
	user = request.user
	
	cons_key='78hcghcxdf03ko'
	cons_secret='PCJJm3KI2Ta7tqja'
	user_token='25c7aef5-49bd-4e29-a7cb-e7d4f8dc2a2a' 
	user_secret='7ed2cba8-9e66-4a0e-aeab-16ca8443bd2b' 
	return_url='http://127.0.0.1:8000/'
	
	#cons_key='779vct8th3wnad'
	#cons_secret='LkCTAYQkarzVFCFJ'
	#user_token='d152649a-b42d-40c4-860d-5d7eabfca142' 
	#user_secret='41261b07-ba82-4d61-83b2-6cae6d1deaf6' 
	#return_url='http://127.0.0.1:8000/'
	    
	auth = linkedin.LinkedInDeveloperAuthentication(cons_key, cons_secret, 
	                                                      user_token, user_secret, 
	                                                      return_url, permissions=linkedin.PERMISSIONS.enums.values())
    
    
	app = linkedin.LinkedInApplication(auth)
	
	url = usuario
	
	array=[]
	
	nombre = app.get_profile(member_url=url,selectors=['first-name']).values()
	
	apellido = app.get_profile(member_url=url,selectors=['last-name']).values()   
       
	headline = app.get_profile(member_url=url, selectors=['headline']).values()
	      
	picture = app.get_profile(member_url=url, selectors=['picture_url']).values()
	
	positions = app.get_profile(member_url=url, selectors=['positions:(company:(name),startDate,title)']).values()
	
	contactos = app.get_profile(member_url=url, selectors=['num-connections']).values()
	
	
	
	#foto por defecto en caso de que no tenga avatar
	if picture == []:
	    picture =['http://www.rotulomivehiculo.com/images/loginUser.png']
	
	
	contador = positions[0]['_total']
	
	
	if contador == 1 and len(positions[0]['values'][0]) >= 3:
    
	    fechaAno= positions[0]['values'][0]['startDate']['year']
	    fechaMes= positions[0]['values'][0]['startDate']['month']
	    company= positions[0]['values'][0]['company']['name']
	    title= positions[0]['values'][0]['title']
	    
	    return ({'nombre': nombre[0],  'headline' : headline[0], 'picture' : picture[0],'apellido' : apellido[0], 'fechaAno':fechaAno,'fechaMes':fechaMes,'company':company,'title':title,'contactos':contactos[0]} )
    
	elif contador == 1 and len(positions[0]['values'][0])<3:
	    
	    mensaje = 'Este usuario no tiene EXP publica en LinkedIn'
       
	    return ({'nombre': nombre[0],  'headline' : headline[0], 'picture' : picture[0],'apellido' : apellido[0], 'mensaje':mensaje,'contactos':contactos[0]} )
		    
    
	elif contador > 1:
    
	    fechaAno= positions[0]['values'][0]['startDate']['year']
	    fechaMes= positions[0]['values'][0]['startDate']['month']
	    company= positions[0]['values'][0]['company']['name']
	    title= positions[0]['values'][0]['title']
       
	    fechaAno2= positions[0]['values'][1]['startDate']['year']
	    fechaMes2= positions[0]['values'][1]['startDate']['month']
	    company2= positions[0]['values'][1]['company']['name']
	    title2= positions[0]['values'][1]['title']
	    
	    return ({'nombre': nombre[0],  'headline' : headline[0], 'picture' : picture[0],'apellido' : apellido[0], 'fechaAno':fechaAno,'fechaMes':fechaMes,'company':company,'title':title,'fechaAno2':fechaAno2,'fechaMes2':fechaMes2,'company2':company2,'title2':title2,'contactos':contactos[0]} )
	
	elif len(positions[0])>2 or contador<2:
	    mensaje = 'Este usuario no tiene EXP publica en LinkedIn'
       
	    return ({'nombre': nombre[0],  'headline' : headline[0], 'picture' : picture[0],'apellido' : apellido[0], 'mensaje':mensaje,'contactos':contactos[0]} )
	
	else:
	    
	    fallo='No hay suficientes datos.'
	    
	return ({'fallo3':fallo})
    except:
	errorAcceso="Error al acceder a la API de LinkeIn"
    


		

def cargarPantalla(request):
    
    
    user=request.user
    buscar =AppForm()
    comentario = ComentForm()
    linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=user)
    linkedin = linkedin[0]	
    todos = Cuenta.objects.all().filter(destinatario=user)
    return render(request,'inicio.html',{'buscar':buscar,'user': user,'next_url': '/', 'datos': getBiografia(request,linkedin),'tweets':getTweets(request,user),'todos':todos})
    
def buscar(request,usuario):

    if request.method == 'POST':
        form = AppForm(data=request.POST)
	
        if form.is_valid():
	    user=request.user
	    usuario = form.cleaned_data['destinatario']  
	    comentario = ComentForm()
	    todos = Cuenta.objects.all().filter(destinatario=usuario)
	    linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=usuario)
	    if linkedin != 'None' and linkedin and usuario!= 'None':
		linkedin = linkedin[0]	
		buscar =AppForm()
             #Success
		return render_to_response('inicio.html',{'buscar':buscar,'tweets':getTweets(request,usuario),'datos':getBiografia(request,linkedin),'linkedin': linkedin,'comentario':comentario,'todos':todos,'usuario':usuario,},context_instance=RequestContext(request),)
	    else:
		user=request.user
		buscar =AppForm()

		comentario = ComentForm()
		linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=user)
		linkedin = linkedin[0]	
		
		todos = Cuenta.objects.all().filter(destinatario=user)
		falloBusca="No se han encontrado coincidencias con ese nombre de usuario."
		return render(request,'inicio.html',{'buscar':buscar,'user': user,'next_url': '/', 'datos': getBiografia(request,linkedin),'tweets':getTweets(request,usuario),'fallo':falloBusca,'todos':todos,})
		#return HttpResponseRedirect('/login')
	else:
            
	    user=request.user
	    buscar =AppForm()

	    comentario = ComentForm()
	    linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=usuario)
	    linkedin = linkedin[0]	
	    todos = Cuenta.objects.all().filter(destinatario=usuario)
	    falloBusca="No se han encontrado coincidencias con ese nombre de usuario."
	    return render(request,'inicio.html',{'buscar':buscar,'user': user,'next_url': '/', 'datos': getBiografia(request,linkedin),'tweets':getTweets(request,usuario),'fallo':falloBusca,'todos':todos,})