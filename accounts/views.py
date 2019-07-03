from django.shortcuts import render, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact
def register(request):
    if request.method=='POST':
        #get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #chekcing if pw martches
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,"User name already taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"email is already registered")
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,password=password,email=email,last_name=last_name)
                    #auto login after register
                    '''
                    auth.login(request,user)
                    messages.success(request,"YOU ARE NOW LOGGED IN")
                    return redirect('index')
                    '''
                    user.save()
                    messages.success(request,"You have now registered , you can login")
                    return redirect('login')
        else:
            messages.error(request,"passwords do not match")
            return redirect('register')    


    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method=='POST':
        #registeruser
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username, password=password)


        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are logged in")
            return redirect('dashboard')
            
        else:
            messages.error(request,"invalid credentials")
            return redirect('login')


    else:
       return render(request,'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,"You are now logged out")
        return redirect('index')

def dashboard(request):
    user_contacts=Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context={
        'contacts':user_contacts
    }
    return render(request,'accounts/dashboard.html', context)