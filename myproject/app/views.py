from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Item, UserProfile

def home(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'items': items})

def browse_items(request):
    query = request.GET.get('q', '').strip()
    items = Item.objects.filter(
        Q(removed_at__isnull=True) |
        Q(removed_at__gte=timezone.now() - timedelta(days=30))
    ).order_by('-created_at')

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'browse.html', {
        'items': items,
        'query': query,
    })

@login_required(login_url='login')
def my_reports(request):
    user_contact = None
    if hasattr(request.user, 'userprofile'):
        user_contact = request.user.userprofile.contact_number

    history_filter = Q(owner=request.user)
    if user_contact:
        history_filter |= Q(owner__isnull=True, contact=user_contact)
    if request.user.email:
        history_filter |= Q(owner__isnull=True, contact=request.user.email)

    items = Item.objects.filter(
        history_filter & (
            Q(removed_at__isnull=True) |
            Q(removed_at__gte=timezone.now() - timedelta(days=30))
        )
    ).order_by('-created_at')

    return render(request, 'my_reports.html', {'items': items})

def how_it_works(request):
    return render(request, 'how_it_works.html')

def contact(request):
    return render(request, 'contact.html')

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = request.POST.get('category', 'Other')
        contact = request.POST.get('contact')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        Item.objects.create(
            name=name,
            description=description,
            owner=request.user if request.user.is_authenticated else None,
            status=status,
            category=category,
            contact=contact,
            location=location,
            image=image
        )
        messages.success(request, f"Item '{name}' reported successfully!")
        return redirect('/')
    return render(request, 'add_item.html')

def delete_item(request, id):
    try:
        item = Item.objects.get(id=id)
        if not request.user.is_authenticated:
            messages.error(request, "Please login before removing an item.")
            return redirect('login')

        user_contact = None
        if hasattr(request.user, 'userprofile'):
            user_contact = request.user.userprofile.contact_number

        can_remove = (
            item.owner == request.user or
            (item.owner is None and user_contact and item.contact == user_contact) or
            request.user.is_staff
        )

        if not can_remove:
            messages.error(request, "You are not allowed to remove this item.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if request.user.is_staff:
            name = item.name
            item.delete()
            messages.warning(request, f"Item '{name}' has been permanently deleted.")
        else:
            item.removed_at = timezone.now()
            item.save()
            messages.warning(request, f"Item '{item.name}' has been removed from your history and will remain saved for 30 days.")
    except Item.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- AUTHENTICATION & PROFILE VIEWS ---

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        UserProfile.objects.create(user=user, contact_number=contact)

        login(request, user)
        messages.success(request, f"Welcome, {name}! Your account has been created.")
        return redirect('/')

    return render(request, 'register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.warning(request, "You have been logged out.")
    return redirect('/')

def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your profile.")
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        image = request.FILES.get('profile_image')

        request.user.first_name = name
        request.user.save()

        profile = request.user.userprofile
        profile.contact_number = contact
        if image:
            profile.profile_image = image
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('/')

    return render(request, 'profile.html')
