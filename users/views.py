from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils.text import slugify
from cart.models import Order

from .forms import SingupForm, EditProfileForm, CustomAuthenticationForm, BookForm
from shop.models import Book

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('about_us')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login_or_signup.html', {'title':'Login','form':form})

def singup_view(request):
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('about_us')
    else:
        form = SingupForm()
    
    return render(request, 'users/login_or_signup.html', {'title':'Signup','form':form})

@login_required()
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'title':'Profile', 'orders': orders})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'users/login_or_signup.html', {'title':'Edit Profile','form':form})

@login_required()
def logout_view(request):
    logout(request)
    return redirect('about_us')

@login_required()
def create_product(request):
    print(request.method)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            book = form.save(user=request.user)
            print('____________________________OK____________________________________')
            return redirect('book', slug=book.slug)
    else:
        ('____________________________NOT____________________________________')
        form = BookForm()
    print('____________________________:(____________________________________')
    return render(request, 'users/create.html', {'form': form})

@login_required()
def edit_product(request, slug):
    print(request.method)
    book = get_object_or_404(Book, slug=slug, owner=request.user)
    print(book)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        print(form)
        if form.is_valid():
            book = form.save(user=request.user)
            print('____________________________OK____________________________________')
            return redirect('book', slug=book.slug)
    else:
        print('____________________________NOT____________________________________')
        form = BookForm(instance=book)
    print('____________________________:(____________________________________')
    return render(request, 'users/edit.html', {'form': form})
