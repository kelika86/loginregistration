from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pizza
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

def index(request):
    context={'all_pizzas': Pizza.objects.all()}
    return render(request, 'form_app/index.html', context)

def create(request):
    if request.method=="POST":
    #Original validation logic applies
    #Name must be present and at least 2 characters long
    #Description must be at least 8 characters long
    #Price must be present
        print(request.POST)
    #1. create errors dictionary   
        errors={}
    #2. validate post information
        if len(request.POST['name'])==0:
            
            errors['name']="Name must be present"
        elif len(request.POST['name'])<2:
            
            errors['name']="Name must be at least 2 characters long"
        
        if len(request.POST['price'])==0:
            
            errors['price']="Price must be present"
        
        if len(request.POST['description'])==0:
            
            errors['description']="Description is required"
        elif len(request.POST['description'])<8:
            
            errors['description']="Description must be at least 8 characters long"
        
        #This is new for registering
        if not EMAIL_REGEX.match(request.POST['email']):
            errors['email']="Email must be in proper format"
        else:
            users_with_same_email=Pizza.objects.filter(email=request.POST['email'])
            if len(users_with_same_email)>0:
                errors['email']='Email is already taken'
        
        if request.POST['password'] != request.POST['password_confirm']:
                errors['password'] = 'Password fields must match'
        if len(request.POST['password'])<8:
            errors['password']='Password must be at least 8 characters long'
        
        print(errors)
        #3. Check if errrors exist; uf they do, add them to messages
        if len(errors):
            for key,value in errors.items():
                messages.error(request, value)
        else: 
            #We need Bcrypt to hash the password
            hashed_pw= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            Pizza.objects.create(name=request.POST['name'], price= request.POST['price'], description=request.POST['description'], email=request.POST['email'], password=hashed_pw)
            messages.success(request, 'successfully created a pizza!')
        return redirect ('/')
    
def login(request):
    if request.method=="POST":
        users_with_same_email=Pizza.objects.filter(email=request.POST['email'])
        if len(users_with_same_email)>0:
            print('user with the email exists! checking password now....')
            the_user=users_with_same_email.first()
            if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
                print('the passwords match! adding to session')
                request.session['user_id']=the_user.id
                request.session['user_name']=the_user.name
                messages.success(request, 'you have logged in {}!'.format(request.session['user_name']))
                return redirect ('/')
            else:
                print('passwords do not match')
                messages.error(request, "invalid info")
                return redirect ('/')
        else:
            messages.error(request, "invalid info, no users with that email")
            return redirect ('/')
# Create your views here.
