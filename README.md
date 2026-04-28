# ReSource – Local P2P Rental Platform

A beginner-friendly Django web application for community-based peer-to-peer rentals. Built for college students and local communities to list, borrow, and share items.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Architecture & Design Decisions](#architecture--design-decisions)
6. [Database Schema](#database-schema)
7. [URL Structure](#url-structure)
8. [Setup & Installation](#setup--installation)
9. [How to Use the App](#how-to-use-the-app)
10. [App-by-App Breakdown](#app-by-app-breakdown)
11. [Rental Workflow Explained](#rental-workflow-explained)
12. [Security Measures](#security-measures)
13. [How to Extend This Project](#how-to-extend-this-project)
14. [Common Errors & Fixes](#common-errors--fixes)
15. [Learning Takeaways](#learning-takeaways)

---

## Project Overview

**ReSource** is a Local Peer-to-Peer (P2P) Rental Platform. The goal is simple:

> Allow community members to list their items (tools, electronics, books, clothing) and let others borrow them for a daily fee — without any payment gateway, chat system, or complex infrastructure.

This project is built to be **read and understood by a 2nd-semester student**. Every design decision prioritizes **clarity over cleverness**.

---

## Features

### User Authentication
- Register with username, email, password, and community name
- Login / Logout using Django's built-in auth system
- Each user automatically gets a **Profile** with a trust score (default 5.0)

### Item Listings (Full CRUD)
- List an item with title, description, category, daily rate, and an optional image
- Edit or delete your own listings
- Browse all available items with **search** (by title) and **category filter**

### Rental Workflow
- Any logged-in user can request to rent an available item
- The item owner receives the request and can **Approve** or **Reject** it
- Once approved, the owner can mark the rental as **Completed** when the item is returned
- Completing a rental increments the item's `usage_count` (popularity tracker)

### Dashboard
- **My Listings tab**: See your listed items + all incoming rental requests with action buttons
- **My Rentals tab**: See all rental requests you've made and their current status

### Homepage
- Search bar
- Category filter buttons
- Card-based grid of available items

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x (Python) |
| Database | SQLite (via Django ORM) |
| Frontend | Django Templates + Bootstrap 5 |
| Auth | Django's built-in `django.contrib.auth` |
| File Uploads | Django's media system + Pillow |
| Styling | Bootstrap 5 CDN + Bootstrap Icons |

**Why these choices?**
- **Django**: Batteries-included. ORM, auth, admin, CSRF — all built in.
- **SQLite**: Zero config. Perfect for development. One file database.
- **Bootstrap 5**: No custom CSS needed. Responsive out of the box.
- **No JavaScript frameworks**: Keeps the project simple and server-rendered.

---

## Project Structure

```
resource_project/          ← Django project root
│
├── manage.py              ← Django CLI tool (run commands here)
│
├── resource_project/      ← Project configuration package
│   ├── settings.py        ← All settings: DB, installed apps, media, etc.
│   ├── urls.py            ← Root URL router (delegates to each app)
│   └── wsgi.py            ← WSGI server entry point
│
├── core/                  ← Homepage + Dashboard
│   ├── views.py           ← home_view, dashboard_view
│   └── urls.py            ← / and /dashboard/
│
├── users/                 ← Auth + Profile
│   ├── models.py          ← Profile model (extends User)
│   ├── forms.py           ← RegisterForm
│   ├── views.py           ← register_view
│   └── urls.py            ← /register/, /login/, /logout/
│
├── items/                 ← Item CRUD
│   ├── models.py          ← Item model
│   ├── forms.py           ← ItemForm
│   ├── views.py           ← list, detail, create, edit, delete
│   └── urls.py            ← /items/... routes
│
├── rentals/               ← Rental workflow
│   ├── models.py          ← Rental model
│   ├── forms.py           ← RentalRequestForm
│   ├── views.py           ← request, approve, reject, complete
│   └── urls.py            ← /rent/..., /rental/.../...
│
├── templates/             ← All HTML templates
│   ├── base.html          ← Master layout (navbar, messages, footer)
│   ├── core/
│   │   ├── home.html
│   │   └── dashboard.html
│   ├── users/
│   │   ├── login.html
│   │   └── register.html
│   ├── items/
│   │   ├── item_list.html
│   │   ├── item_detail.html
│   │   ├── item_form.html         ← Used for both Create and Edit
│   │   └── item_confirm_delete.html
│   └── rentals/
│       └── rental_request.html
│
├── static/                ← CSS, JS (currently empty — Bootstrap via CDN)
├── media/                 ← User-uploaded item images (auto-created)
├── db.sqlite3             ← SQLite database (auto-created on migrate)
├── requirements.txt       ← Python dependencies
└── .gitignore
```

---

## Architecture & Design Decisions

### Why 4 separate Django apps?

Django encourages splitting your project into "apps" — self-contained modules with their own models, views, and URLs. Each app has a **single responsibility**:

| App | Responsibility |
|---|---|
| `core` | Homepage and Dashboard (no models needed) |
| `users` | Auth + Profile (who is using the platform) |
| `items` | Item listings (what can be rented) |
| `rentals` | Rental transactions (rental requests and their lifecycle) |

This makes the code easier to navigate, debug, and extend.

### Why Function-Based Views (FBVs)?

Django supports both Function-Based Views (FBVs) and Class-Based Views (CBVs). This project uses **FBVs everywhere** because:
- They are explicit — you can read the function top-to-bottom and understand exactly what happens
- No magic inheritance to trace
- Easier to add custom logic (permission checks, flash messages)
- Better for beginners

### Why no REST API or React?

This is a **server-rendered** Django app. The browser requests a URL → Django processes it → Django sends back a complete HTML page. This is simpler, requires less code, and is the standard way to build Django apps for beginners.

### OneToOneField for Profile

Django's `User` model handles the auth-critical fields (username, password, email). Rather than replacing it, we **extend** it using a `Profile` model with a `OneToOneField`:

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trust_score = models.FloatField(default=5.0)
    community_name = models.CharField(max_length=100, blank=True)
```

This means every user has exactly one profile. When the user is deleted, the profile is deleted too (`CASCADE`).

---

## Database Schema

### Profile
| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `user` | OneToOneField → User | Django's built-in User |
| `trust_score` | FloatField | Default 5.0 |
| `community_name` | CharField(100) | Optional |

### Item
| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `owner` | ForeignKey → User | Who listed this item |
| `title` | CharField(200) | |
| `description` | TextField | |
| `category` | CharField(50) | Choices: Tools, Electronics, Books, Clothing, Other |
| `daily_rate` | PositiveIntegerField | Price in ₹ per day |
| `image` | ImageField | Optional, stored in `/media/item_images/` |
| `available` | BooleanField | Default True |
| `usage_count` | PositiveIntegerField | Increments on completion |
| `created_at` | DateTimeField | Auto-set on creation |

### Rental
| Field | Type | Notes |
|---|---|---|
| `id` | AutoField (PK) | |
| `item` | ForeignKey → Item | What is being rented |
| `renter` | ForeignKey → User | Who is renting it |
| `start_date` | DateField | |
| `end_date` | DateField | |
| `status` | CharField(20) | Pending → Approved/Rejected → Completed |
| `created_at` | DateTimeField | Auto-set on creation |

---

## URL Structure

| URL | View | Description |
|---|---|---|
| `/` | `home_view` | Homepage with item grid + search |
| `/login/` | Django built-in | Login page |
| `/register/` | `register_view` | Registration page |
| `/logout/` | Django built-in | Logs out + redirects |
| `/dashboard/` | `dashboard_view` | My listings + my rentals |
| `/items/` | `item_list_view` | Browse all items |
| `/items/create/` | `item_create_view` | Create new listing |
| `/items/<id>/` | `item_detail_view` | Item detail page |
| `/items/<id>/edit/` | `item_edit_view` | Edit your listing |
| `/items/<id>/delete/` | `item_delete_view` | Delete your listing |
| `/rent/<item_id>/` | `rental_request_view` | Request to rent an item |
| `/rental/<id>/approve/` | `rental_approve_view` | Owner approves request |
| `/rental/<id>/reject/` | `rental_reject_view` | Owner rejects request |
| `/rental/<id>/complete/` | `rental_complete_view` | Owner marks as completed |

---

## Setup & Installation

### Prerequisites

Make sure you have:
- Python 3.10+ installed (`python --version`)
- pip installed (`pip --version`)

### Step 1 — Clone or extract the project

```bash
# If you have the zip file:
unzip resource_project.zip
cd resource_project
```

### Step 2 — Create a virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Django` — the web framework
- `Pillow` — required for handling image uploads

### Step 4 — Apply database migrations

```bash
python manage.py migrate
```

This creates `db.sqlite3` and sets up all the tables.

### Step 5 — Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username and password. This gives you access to `/admin/`.

### Step 6 — Run the development server

```bash
python manage.py runserver
```

Now open your browser and go to: **http://127.0.0.1:8000/**

---

## How to Use the App

### As a new user:
1. Go to `/register/` → Create an account
2. Go to `/items/create/` → List an item (e.g., "Drill Machine", ₹50/day)
3. Browse other items at `/` or `/items/`
4. Click an item → "Request to Rent" → Pick dates → Submit
5. Check `/dashboard/` to see status of your requests

### As an item owner:
1. Go to `/dashboard/` → "My Listings" tab
2. Scroll down to "Incoming Rental Requests"
3. Click **Approve** or **Reject**
4. Once the renter returns the item, click **Mark Complete**

### As an admin:
1. Go to `/admin/` and log in with your superuser credentials
2. You can view/edit all Users, Profiles, Items, and Rentals from here

---

## App-by-App Breakdown

### `users` app

**models.py** — `Profile` model
- Uses `OneToOneField` to link to Django's `User`
- Created automatically when a user registers (in `RegisterForm.save()`)

**forms.py** — `RegisterForm`
- Inherits from `UserCreationForm` (handles username + password validation)
- Adds `email` and `community_name`
- Overrides `save()` to also create the Profile

**views.py** — `register_view`
- GET: Renders the empty form
- POST: Validates, saves user, logs them in, redirects to dashboard

### `items` app

**models.py** — `Item` model
- `CATEGORY_CHOICES` is a list of tuples used in the dropdown
- `ImageField` stores files in `media/item_images/`
- `usage_count` is incremented by the rental app (not directly here)

**views.py** — 5 views
- `item_list_view`: Filters queryset by `q` (search) and `category` GET params
- `item_create_view`: Sets `item.owner = request.user` before saving
- `item_edit_view`: Checks `item.owner == request.user` before allowing edits
- `item_delete_view`: Shows a confirmation page on GET, deletes on POST
- `item_detail_view`: Shows single item; shows Rent button only if user is not the owner

### `rentals` app

**models.py** — `Rental` model
- `STATUS_CHOICES` drives the entire workflow
- `total_days()` and `total_cost()` are helper methods (not stored in DB)

**views.py** — 4 views
- `rental_request_view`: Validates item is available + user is not the owner
- `rental_approve_view`: Checks `rental.item.owner == request.user`
- `rental_reject_view`: Same ownership check
- `rental_complete_view`: Increments `item.usage_count` after saving

### `core` app

**views.py** — 2 views
- `home_view`: Identical search/filter logic to `item_list_view`; renders home template
- `dashboard_view`: Queries three separate querysets and passes all to template

---

## Rental Workflow Explained

```
Renter visits item page
        │
        ▼
"Request to Rent" → POST /rent/<item_id>/
        │
        ▼
  Rental created (status = "Pending")
        │
        ▼
Owner sees it on Dashboard → Incoming Requests
        │
   ┌────┴────┐
   ▼         ▼
Approve    Reject
   │         │
status=    status=
"Approved" "Rejected"
   │
   ▼
Item is used and returned
   │
   ▼
Owner clicks "Mark Complete"
   │
   ▼
status = "Completed"
item.usage_count += 1
```

**Key rules enforced in views:**
- You cannot rent your own item
- You cannot rent an unavailable item
- Only the item owner can approve/reject/complete
- Only Pending rentals can be approved or rejected
- Only Approved rentals can be completed

---

## Security Measures

### `@login_required` decorator
Applied to all views that modify data:
```python
@login_required
def item_create_view(request):
    ...
```
If not logged in, user is redirected to `/login/`.

### Ownership checks in views
```python
if item.owner != request.user:
    messages.error(request, "You don't have permission.")
    return redirect('item_detail', pk=pk)
```

### `get_object_or_404()`
Instead of letting Django throw a 500 error for missing objects:
```python
item = get_object_or_404(Item, pk=pk)
```
Returns a clean 404 page if the item doesn't exist.

### CSRF Protection
Django's `{% csrf_token %}` tag is in every form. This prevents Cross-Site Request Forgery attacks where malicious sites could submit forms on behalf of logged-in users.

---

## How to Extend This Project

Here are beginner-friendly next steps:

### 1. Add a Rating System
```python
# In rentals/models.py
class Review(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
```
Only allow reviews after status = 'Completed'.

### 2. User Profile Page
Add a `/profile/<username>/` page that shows their listed items and trust score.

### 3. Availability Toggle
Let owners mark items as unavailable temporarily from the dashboard with one click.

### 4. Pagination
```python
from django.core.paginator import Paginator
paginator = Paginator(items, 12)  # 12 per page
page = paginator.get_page(request.GET.get('page'))
```

### 5. Item Image Thumbnail
Use `Pillow` to resize images on upload to save storage space.

### 6. Email Notifications
Use Django's `send_mail()` to notify owners when a rental request arrives.

### 7. Rental Conflict Detection
Check that no overlapping approved rentals exist for the same item on requested dates:
```python
overlapping = Rental.objects.filter(
    item=item,
    status='Approved',
    start_date__lt=end_date,
    end_date__gt=start_date
)
```

---

## Common Errors & Fixes

### `No module named 'PIL'`
```bash
pip install Pillow
```
Pillow is required for `ImageField` in Item model.

### `TemplateDoesNotExist`
Make sure `DIRS` in `settings.py` includes:
```python
'DIRS': [BASE_DIR / 'templates'],
```

### `Media files not loading`
In `resource_project/urls.py`, ensure this is present:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### `No reverse match for 'dashboard'`
Make sure `core/urls.py` is included in the main `urls.py`:
```python
path('', include('core.urls')),
```

### `Profile.DoesNotExist`
If you created users directly via `createsuperuser` or the admin, they won't have a Profile. Fix by creating one manually in the shell:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from users.models import Profile
>>> for u in User.objects.all():
...     Profile.objects.get_or_create(user=u)
```

### Image not showing after upload
Check that:
1. `MEDIA_URL = '/media/'` and `MEDIA_ROOT = BASE_DIR / 'media'` are set
2. The `media/` directory exists (it's created automatically on first upload)
3. `urls.py` serves media in DEBUG mode (see above)

---

## Learning Takeaways

By studying this project, you will understand:

| Concept | Where to find it |
|---|---|
| Django project vs app structure | Top-level folder layout |
| Model definition + field types | `items/models.py`, `users/models.py` |
| OneToOneField vs ForeignKey | `users/models.py` vs `items/models.py` |
| Django ORM queries | `core/views.py` — dashboard queries |
| Form creation and validation | `users/forms.py`, `items/forms.py`, `rentals/forms.py` |
| Function-based views (GET/POST) | All views files |
| Template inheritance | `base.html` + `{% extends %}` |
| Template tags: if, for, url, csrf_token | All templates |
| Flash messages | `messages.success/error()` in views |
| `@login_required` decorator | `items/views.py`, `rentals/views.py` |
| File upload handling | `ItemForm` + `enctype="multipart/form-data"` |
| Static vs Media files | `settings.py` + `urls.py` |
| Django Admin registration | All `admin.py` files |
| URL routing with `include()` | `resource_project/urls.py` |

---

## Project Info

- **Project name**: ReSource – Local P2P Rental Platform  
- **Framework**: Django 5.x  
- **Database**: SQLite  
- **Frontend**: Bootstrap 5  
- **Difficulty**: Beginner-friendly  
- **Recommended for**: 2nd–3rd semester CS/IT students  

Happy coding! 🚀
