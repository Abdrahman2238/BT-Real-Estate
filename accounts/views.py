from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact

def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
      if User.objects.filter(username=username).exists():
        return redirect('index') 
      else:
        if User.objects.filter(email=email).exists():
          return redirect('index') 
        else:
         user = User.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name)
         user.save
         return redirect('login')
    else:
      return redirect("register")
  else:
    return render(request, 'accounts/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('dashboard')

    else:
      return redirect('index')

  else:
    return render(request, 'accounts/login.html')

def logout(request):
   if request.method == 'POST':
     auth.logout(request)
     return redirect('index')

def dashboard(request):

  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts' : user_contacts
  }

  return render(request, 'accounts/dashboard.html', context)