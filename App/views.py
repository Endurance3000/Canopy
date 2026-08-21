from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Photo, Category

def testfun(request):
    photos = Photo.objects.all().order_by('-uploaded_at')
    return render(request, 'index.html', {'photos': photos})

# SIGN UP VIEW
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# LOGOUT VIEW
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        photo_title = request.POST.get('title', 'Untitled Shot')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        location = request.POST.get('location', '')
        camera_model = request.POST.get('camera_model', '')
        aperture = request.POST.get('aperture', '')
        shutter_speed = request.POST.get('shutter_speed', '')
        iso = request.POST.get('iso')
        focal_length = request.POST.get('focal_length', '')

        category_obj = Category.objects.filter(id=category_id).first() if category_id else None

        if uploaded_file:
            Photo.objects.create(
                user=request.user,
                image=uploaded_file,
                title=photo_title,
                description=description,
                category=category_obj,
                location=location,
                camera_model=camera_model,
                aperture=aperture,
                shutter_speed=shutter_speed,
                iso=int(iso) if iso and iso.isdigit() else None,
                focal_length=focal_length
            )
            return redirect('home')
            
    categories = Category.objects.all()
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'upload.html', {'photos': photos, 'categories': categories})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    # Increment view count
    photo.views += 1
    photo.save(update_fields=['views'])
    
    is_liked = photo.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    return render(request, 'photo_detail.html', {
        'photo': photo,
        'is_liked': is_liked,
    })

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
        is_liked = False
    else:
        photo.likes.add(request.user)
        is_liked = True
    
    # Return JSON for AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'liked': is_liked,
            'likes_count': photo.likes.count()
        })
    
    # Fallback redirect for standard HTTP requests
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('photo_detail', pk=pk)