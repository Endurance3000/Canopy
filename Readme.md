# Canopy 🌲

An elegant, web platform for discovering, sharing, and exploring nature photography. Built with Django and designed around a dark forest aesthetic, Canopy highlights EXIF camera specifications, photographer attributions, and real-time community engagement.

---

## Key Features

* **Earthy, Cohesive UI**: Custom forest aesthetic using warm cream (`#FEFAE0`) and deep pine tones (`#2D3A2B`) with Bootstrap Icons.
* **Interactive Spotlight Hero Carousel**: Smooth horizontal spotlight banner with scroll progress bar and glassmorphism badges.
* **Masonry Discovery Grid**: Clean card layout displaying photography thumbnails, view counters, EXIF availability badges, and direct action triggers.
* **Interactive Lightbox Modal**: High-resolution lightbox modal displaying complete camera metadata without navigating away from the page.
* **Asynchronous Like Engine**: Dynamic AJAX-powered toggling for likes across grid cards, detail pages, and lightboxes without page reloads or layout jumps.
* **EXIF Metadata Engine**: Dedicated view support for camera hardware specs including Aperture, Shutter Speed, ISO, Focal Length, and Location.

---

## Tech Stack

* **Backend**: Python 3.14, Django 6.1
* **Frontend**: HTML5, CSS3, JavaScript (ES6+ AJAX Fetch API)
* **UI Framework**: Bootstrap 5, Bootstrap Icons
* **Database**: Postgres (Under Development)

---

## Project Structure

```text
Canopy/
├── App/                    # Core Django application
│   ├── models.py           # Photo model (Image, Likes, Views, EXIF data)
│   ├── views.py            # View logic & JSON response handling for AJAX
│   ├── urls.py             # Route mapping
│   └── templates/          # Application templates
│       ├── base.html       # Global navigation & asset dependencies
│       ├── index.html      # Masonry grid, hero carousel & lightbox modal
│       └── photo_detail.html # Extended EXIF specs & dedicated photo view
├── manage.py
└── requirements.txt

```

---

## Quick Start

### 1. Prerequisites

Ensure you have Python 3.10+ installed on your machine.

### 2. Installation & Setup

Clone the repository:

```bash
git clone https://github.com/your-username/canopy.git
cd canopy

```

Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

Install dependencies:

```bash
pip install django pillow

```

Apply migrations:

```bash
python manage.py migrate

```

Create a superuser to manage uploads:

```bash
python manage.py createsuperuser

```

Run the development server:

```bash
python manage.py runserver

```

Open `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)` in your browser to explore Canopy.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
