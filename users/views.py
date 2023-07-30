from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
    return render(request, 'users/profile.html', {'title':'Profile'})

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
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book', slug=book.slug)
    else:
        form = BookForm()
    return render(request, 'users/create.html', {'form': form})

@login_required()
def edit_product(request, slug):
    book = get_object_or_404(Book, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            book = form.save()
            return redirect('book', slug=book.slug)
    else:
        form = BookForm(instance=book)
    return render(request, 'users/edit.html', {'form': form})
