from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from prueba.models import Cuenta, UserCreate, Authenti, App
from django.shortcuts import render_to_response, redirect , render
from django.contrib.auth import login, authenticate, logout
from prueba.forms import UserCreateForm, AuthenticateForm, AppForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404



def index(request, auth_form=None,formulario=None):
    
    # usuario logueado
    if request.user.is_authenticated():
        user = request.user
	usuario = UserCreate.objects.all()
	
        return render(request,'inicio.html',{'user': user,'next_url': '/', 'datos': getBiografia(request,None),'tweets':getTweets(request)})
    else:
        # usuario aun sin logear
        auth_form = auth_form or AuthenticateForm()
        formulario =UserCreateForm()
	
 
        return render(request,'home.html',{'auth_form': auth_form, 'formulario': formulario, })

    
    
def login_view(request):
     
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
	    user=request.user
	    usuario = form.cleaned_data['username']
	    password = form.cleaned_data['password']	    
	    linkedin = UserCreate.objects.values_list('first_name', flat=True).filter(username=usuario)
	    linkedin = linkedin[0]
	    acceso = authenticate(username=usuario, password=password)
            login(request, acceso)
             #Success
            return render_to_response('inicio.html',{'datos':getBiografia(request,linkedin),'tweets':getTweets(request,usuario),'linkedin': linkedin},context_instance=RequestContext(request),)
        else:
            # Failure
            return nuevo_usuario(request, log=form)
    return redirect('/')


 
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def usuarios(request, username="", tweet_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        ribbits = Cuenta.objects.filter(user=user.id)
	
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile
            return render(request, 'user.html', {'user': user, 'ribbits': ribbits, })
	
        return render(request, 'user.html', {'user': user, 'ribbits': ribbits, 'follow': True, })
    
    users = User.objects.all().annotate(ribbit_count=Count('ribbit'))
    ribbits = map(get_latest, users)
    obj = zip(users, ribbits)
    ribbit_form = tweet_form or AppForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/usuarios/',
                   'tweet_form': tweet_form,
                   'username': request.user.username, })


@login_required
def submit(request):
    formulario = AppForm(data=request.POST)
    if request.method == "POST":
        next_url = request.POST.get("next_url", "/")
        if formulario.is_valid():
	    import twitter
	    api = twitter.Api(
	        consumer_key='HSAJYkJso2lx7nV9pHGITg',
	        consumer_secret='okILf2DfyyMrNq0JRvlEckNKFC3hFxei21X4NEcURHQ',
	        access_token_key='310810114-eIP0VTRmwJ6uMsBHWb6qzVgp77quUloV3KfGT2MY',
	        access_token_secret='w2U7z2XcrJHjRDpxMoD0b8lVdSCIMWkZyKckf7oiaHG11'
	    )
            tweet = formulario.save(commit=False)
            tweet.user = request.user
            tweet.save()
	   
	    nuevo_tweet = api.PostUpdate(tweet.content)
            return redirect(next_url)
        else:
            return public(request, formulario)
    return redirect('/')


	
def nuevo_usuario(request):
    
    if request.method == 'POST':
	formulario = UserCreateForm(data=request.POST)
	log = AuthenticateForm(data=request.POST)
	if formulario.is_valid():	
	    username = formulario.cleaned_data['username']
	    password = formulario.cleaned_data['password2']
	    linkedin = formulario.cleaned_data['first_name']
	    user = User.objects.create_user(username, linkedin, password)
	    user.set_password(password)   
	    formulario.save()
	    user = authenticate(username=username, password=password)
	    return HttpResponseRedirect('/')
    else:
	formulario = UserCreateForm()
	log = AuthenticateForm()
	    
    return render_to_response('home.html',{'formulario':formulario,'log':log,},context_instance=RequestContext(request))


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
    
	
	for tweet in latest:
	    status = tweet.text
	    tweet_date = tweet.relative_created_at
	    tweets.append({'status': status, 'date': tweet_date})
	    
	
	    
    except:
	    tweets.append({'status': 'Follow us @ManuAranda9', 'date': 'about 10 minutes ago'})
	    
    return{'tweets':tweets}
	    
    #return render_to_response('inicio.html',{'tweet_form': tweet_form, 'user': user,'tweets': tweets})
		

def getBiografia(request,usuario):
    
    
    from linkedin import linkedin
    user = request.user
    
    cons_key='78hcghcxdf03ko'
    cons_secret='PCJJm3KI2Ta7tqja'
    user_token='25c7aef5-49bd-4e29-a7cb-e7d4f8dc2a2a' 
    user_secret='7ed2cba8-9e66-4a0e-aeab-16ca8443bd2b' 
    return_url='http://127.0.0.1:8000/'
	
    auth = linkedin.LinkedInDeveloperAuthentication(cons_key, cons_secret, 
                                                          user_token, user_secret, 
                                                          return_url, permissions=linkedin.PERMISSIONS.enums.values())


    app = linkedin.LinkedInApplication(auth)
    
    url = usuario
    
    
    nombre = app.get_profile(member_url=url,selectors=['first-name']).values()
    
    apellido = app.get_profile(member_url=url,selectors=['last-name']).values()   
   
    location = app.get_profile(member_url=url, selectors=['location']).values()
   
    headline = app.get_profile(member_url=url, selectors=['headline']).values()
	  
    picture = app.get_profile(member_url=url, selectors=['picture_url']).values()
    
    positions = app.get_profile(member_url=url, selectors=['positions:(company:(name))']).values()
    
    for item in positions:
	value = item.values()
    
  
    return ({'nombre': nombre[0], 'location':location[0], 'headline' : headline[0], 'picture' : picture[0],'apellido' : apellido[0], 'positions':value} )

def getPerfilProfesional(request):
    
    tweets=[]    
    
    try:
	import twitter
	tweet_form = AppForm()
        user = request.user
	api = twitter.Api(
	    consumer_key='HSAJYkJso2lx7nV9pHGITg',
	    consumer_secret='okILf2DfyyMrNq0JRvlEckNKFC3hFxei21X4NEcURHQ',
	    access_token_key='310810114-eIP0VTRmwJ6uMsBHWb6qzVgp77quUloV3KfGT2MY',
	    access_token_secret='w2U7z2XcrJHjRDpxMoD0b8lVdSCIMWkZyKckf7oiaHG11'
	)
	latest = api.GetUserTimeline(' ')
	
	
	
	
	for tweet in latest:
	    status = tweet.text
	    tweet_date = tweet.relative_created_at    
	    tweets.append({'status': status, 'date': tweet_date})
	    
	
	    
    except:
	    tweets.append({'status': 'Follow us @ManuAranda9', 'date': 'about 10 minutes ago'})
	    
    return render(request, 'profesional.html',{'tweet_form': tweet_form, 'user': user,'tweets': tweets,'next_url': '/',})
		
