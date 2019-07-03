from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def contact(request):   
    if request.method =='POST':
        listing=request.POST['listing']
        listing_id=request.POST['listing_id']
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']

        #checking if req already sent
        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted=Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request,"You have already made an inquiry for this listing")
                return redirect('/listings/'+listing_id)


        contact=Contact(listing=listing, name=name, listing_id=listing_id, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        send_mail(
            'property listing inquiry',
            'There has been an inquiry for '+listing+'.Sign in to  admin panel for more info',
            'akshayparseja@gmail.com',
            ['bharatparseja@gmail.com','akshay@treeni.com'],
            fail_silently=False
            
        )

        
        
        
        messages.success(request,"your req has been submitted ")
        return redirect('/listings/'+listing_id)
       


        