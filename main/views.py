from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout  
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from .ml_model import util 
from .models import Car , Post, User, Conversation, Message
from .forms import PostForm, SignUpForm, CarForm
from django.core.files.storage import FileSystemStorage 

from pathlib import Path 
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



BASE_DIR = Path(__file__).resolve().parent.parent



def loginPage(response):
    page = 'login'
    if response.user.is_authenticated:
        return redirect('home')

    if response.method == 'POST':
        email = response.POST.get('email')
        password = response.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except:     
            messages.error(response, 'User does not exist')

        user = authenticate(response, email= email , password = password)
        if user is not None:
            login(response, user)
            return redirect('home')
        else: 
            messages.error(response, 'Username or password does not exist')  

    context = {'page': page}
    return render(response, 'main/login_register.html', context)


def logoutPage(response):
    logout(response)
    return redirect('home') 

def registerPage(response):
    
    if response.method == 'POST':
        print(response.POST)
        name = response.POST.get('name')
        email = response.POST.get('email')
        phoneNum = response.POST.get('phoneNum')
        rad = response.POST.get('type')
        password1 = response.POST.get('password1')
        password2 = response.POST.get('password2')
        username = name + str(random_with_N_digits(4))
        
        if rad == '1':
            buyer = True
            seller = False
        if rad == '0'   : 
            buyer = False
            seller = True
        if password1 == password2:
            user = User.objects.create(
                    name = name,
                    email = email,
                    phoneNum = phoneNum,
                    buyer = buyer,
                    seller = seller,
                    password = password1,
                    username= username )
            login(response, user) 
            return redirect('home')
        else: 
            messages.error(response, 'An error occurred during registration!')    
    context = {}
    return render(response, 'main/login_register.html', context)    

def home(response):
    # context = {'BASE_DIR': BASE_DIR}
    return render(response, "main/home.html", {} )

# Gallery and Posts #############################################

def gallery(response):
    if response.GET.get('q') != None:
        q = response.GET.get('q')
    else:
        q=''    

    posts = Post.objects.filter(
        Q(carId__model__icontains=q) |
        Q(carId__year__icontains=q)
    )
    posts_count = posts.count()
    context = {'posts': posts , 'posts_count' : posts_count}
    return render(response, "main/gallery.html", context)

def post(response, pk):
    post = Post.objects.get(id=pk)
    if response.method == 'POST':
       if response.POST.get("start"):
        seller = post.sellerId
        car = post.carId
        context = {'seller': seller, 'car': car}
        return render(response, 'main/start-convo.html', context)
       if response.POST.get("send"): 
           convo = Conversation.objects.create(
               name =  response.POST.get('name'),
               carId=  Car.objects.get(model= response.POST.get('car')),
               buyerId= response.user,
               sellerId= User.objects.get(email= response.POST.get('seller'))
           )
           Message.objects.create(
               user = response.user,
               text = response.POST.get('message'),
               conversationId= convo,
                
           )
           return redirect('mailbox')

    return render(response, "main/post.html", {'post': post})


@login_required(login_url='login')
def createPost(response):
    form = PostForm(response.POST or None, response.FILES or None)
    cars = Car.objects.filter(sellerId= response.user)
    length = len(cars)
    if response.method == 'POST' and response.FILES['avatar']:
        upload = response.FILES['avatar']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        car = Car.objects.get(model = response.POST.get('carId'))
        Post.objects.create(
                     name = response.POST.get('name'),
                     description = response.POST.get('description'),
                     carId = car,
                     avatar = file,
                     sellerId= response.user
                 ) 
        return redirect('gallery') 

    context = {'form': form , 'cars': cars, 'length': length}
    return render(response, "main/post-form.html", context) 



def updatePost(response, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    context = {'form': form}

    if response.method == 'POST':
        form = PostForm(response.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    return render(response, 'main/post-form.html', context)  



def deletePost(response, pk):
    post = Post.objects.get(id=pk)

    if response.method == 'POST':
        post.delete()
        return redirect('gallery')
    return render(response, 'main/delete.html', {'obj': post})


### End of Gallery and Posts #############################################


### Chat Room ############################
def mailbox(response):
    convoB = Conversation.objects.filter(buyerId= response.user)
    convoS = Conversation.objects.filter(sellerId= response.user)
    context = {'convoS' : convoS, 'convoB': convoB}
    return render(response, 'main/mailbox.html',context )


def convo(response, pk):
    convo = Conversation.objects.get(id=pk)
    convo_messages = convo.message_set.all()
    context = {'convo': convo , 'convo_messages': convo_messages}
    if response.method == 'POST':
        message = Message.objects.create(
            user = response.user,
            text = response.POST.get('message'),
            conversationId= convo,
             )
        return render(response, "main/convo.html", context)     


    return render(response, "main/convo.html", context)


def deleteMessage(response, pk):
    message = Message.objects.get(id=pk)
    if response.method == 'POST':
        message.delete()    
        return redirect('mailbox')
    return render(response, 'main/delete.html', {'obj': post})


### estimator ###### 
def service(response):
    util.load_saved_artifacts()
    carModels = []
    carModels = util.get_carModel_names()

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("estimate"):
            odo   = response.POST.get("odometer")
            year  = response.POST.get("year")
            cond  = response.POST.get("condition")
            trans = response.POST.get("trans")
            model = response.POST.get("CarModel")
            price = util.get_estimated_price(model, year, trans, cond, odo)
            car = [odo, year, cond, trans, model, price]

            if response.user.is_authenticated:
                if response.user.seller:
                    form = CarForm({'year': year,
                    'odometer': odo, 'condition': cond, 'transmission': trans,
                    'model': model, 
                    'price': price, 'sellerId': response.user})
                    return render(response, "main/carForm.html", {'form': form })
                else:
                    return render(response, "main/service.html", {"price" : price})
            else: 
               return render(response, "main/service.html", {"price" : price})          
        if response.POST.get("saveCar"): 
                 print(response.POST)
                 Car.objects.create(
                     year = response.POST.get('year'),
                     odometer = response.POST.get('odometer'),
                     condition = response.POST.get('condition'),
                     transmission = response.POST.get('transmission'),
                     model = response.POST.get('model'),
                     price = response.POST.get('price'),
                     sellerId= response.user
                 )
                 return redirect('create-post')   
    return render(response, "main/service.html", {"carModels" : carModels})

        





   





