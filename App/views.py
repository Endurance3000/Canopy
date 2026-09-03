from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Photo, Category
from PIL import Image, ExifTags
# Add User to this import at the top of views.py
from django.contrib.auth.models import User

def extract_exif_data(image_file):
    """Helper function to extract EXIF metadata using Pillow."""
    exif_data = {
        'camera_model': None,
        'aperture': None,
        'shutter_speed': None,
        'iso': None,
        'focal_length': None
    }
    try:
        image = Image.open(image_file)
        raw_exif = image._getexif()
        if not raw_exif:
            return exif_data

        exif = {ExifTags.TAGS.get(k, k): v for k, v in raw_exif.items() if k in ExifTags.TAGS}

        # Camera Model
        make = exif.get('Make', '').strip()
        model = exif.get('Model', '').strip()
        if model:
            exif_data['camera_model'] = f"{make} {model}".strip() if make and make not in model else model

        # ISO
        iso_val = exif.get('ISOSpeedRatings')
        if iso_val:
            exif_data['iso'] = int(iso_val)

        # Aperture (FNumber)
        f_number = exif.get('FNumber')
        if f_number:
            exif_data['aperture'] = f"f/{float(f_number):.1f}"

        # Shutter Speed (ExposureTime)
        exposure_time = exif.get('ExposureTime')
        if exposure_time:
            if exposure_time < 1:
                exif_data['shutter_speed'] = f"1/{int(1/float(exposure_time))}s"
            else:
                exif_data['shutter_speed'] = f"{float(exposure_time)}s"

        # Focal Length
        focal_length = exif.get('FocalLength')
        if focal_length:
            exif_data['focal_length'] = f"{int(float(focal_length))}mm"

    except Exception:
        pass  # Fall back cleanly if EXIF extraction fails
    
    return exif_data


def testfun(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    photos = Photo.objects.all().order_by('-uploaded_at')
    
    if category_id:
        photos = photos.filter(category_id=category_id)
        
    if search_query:
        photos = photos.filter(
            title__icontains=search_query
        ) | photos.filter(
            location__icontains=search_query
        ) | photos.filter(
            camera_model__icontains=search_query
        )
        
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'photos': photos,
        'categories': categories,
        'selected_category': category_id
    })


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


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def upload(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')  # Retrieves all selected files
        photo_title = request.POST.get('title', 'Untitled Shot')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        location = request.POST.get('location', '')

        category_obj = Category.objects.filter(id=category_id).first() if category_id else None

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Auto-extract EXIF details for each individual file
                exif_info = extract_exif_data(uploaded_file)

                # Prioritize manual input, fallback to extracted EXIF per image
                camera_model = request.POST.get('camera_model') or exif_info['camera_model']
                aperture = request.POST.get('aperture') or exif_info['aperture']
                shutter_speed = request.POST.get('shutter_speed') or exif_info['shutter_speed']
                focal_length = request.POST.get('focal_length') or exif_info['focal_length']
                
                iso_input = request.POST.get('iso')
                iso = int(iso_input) if iso_input and iso_input.isdigit() else exif_info['iso']

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
                    iso=iso,
                    focal_length=focal_length
                )
            return redirect('home')

    categories = Category.objects.all()
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'upload.html', {'photos': photos, 'categories': categories})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
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
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'liked': is_liked,
            'likes_count': photo.likes.count()
        })
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('photo_detail', pk=pk)

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_photos = Photo.objects.filter(user=profile_user).order_by('-uploaded_at')
    liked_photos = profile_user.liked_photos.all().order_by('-uploaded_at')
    
    # Calculate total likes received across all uploaded photos
    total_likes_received = sum(photo.likes.count() for photo in user_photos)

    if request.method == 'POST' and request.user == profile_user:
        # Handle Profile Updates (Avatar, Bio, Location, Gear)
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        primary_gear = request.POST.get('primary_gear')
        avatar = request.FILES.get('avatar')

        profile = profile_user.profile
        profile.bio = bio
        profile.location = location
        profile.primary_gear = primary_gear
        if avatar:
            profile.avatar = avatar
        profile.save()
        return redirect('profile', username=username)

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'user_photos': user_photos,
        'liked_photos': liked_photos,
        'total_likes_received': total_likes_received,
    })