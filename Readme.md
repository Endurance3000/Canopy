<div align="center">

# 🌲 Canopy

### An editorial-grade nature photography showcase platform.

<p align="center">
  Discover, share, and explore nature photography presented with the craft of a print magazine.
</p>

<p align="center">
  <a href="https://github.com/Endurance3000/Canopy">
    <img src="https://img.shields.io/github/stars/Endurance3000/Canopy?style=flat-square&color=c48b71" alt="GitHub Stars" />
  </a>
  <a href="https://github.com/Endurance3000/Canopy/issues">
    <img src="https://img.shields.io/github/issues/Endurance3000/Canopy?style=flat-square&color=789461" alt="GitHub Issues" />
  </a>
  <a href="https://github.com/Endurance3000/Canopy/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-607274?style=flat-square" alt="License: MIT" />
  </a>
  <img src="https://img.shields.io/badge/Built%20With-Django%20%2B%20Bootstrap%205-8a6552?style=flat-square" alt="Built with Django and Bootstrap 5" />
</p>

<p align="center">
  <a href="#-overview"><strong>Overview</strong></a> ·
  <a href="#-key-features"><strong>Features</strong></a> ·
  <a href="#️-technology-stack"><strong>Tech Stack</strong></a> ·
  <a href="#-project-structure"><strong>Project Structure</strong></a> ·
  <a href="#️-quick-start"><strong>Quick Start</strong></a> ·
  <a href="#-contributing"><strong>Contributing</strong></a>
</p>

</div>

---

## 🌟 Overview

**Canopy** is an elegant web platform for discovering, sharing, and exploring nature photography. Built with **Django** and designed around a dark forest aesthetic, Canopy elevates each photo submission with EXIF camera specifications, photographer attribution, and real-time community engagement, all wrapped in a calm, nature-inspired interface built for crisp showcase previews.

Whether you're browsing a spotlighted collection, filtering by category, or inspecting the exact aperture and shutter speed behind a shot, Canopy is designed to feel like flipping through a curated nature magazine rather than scrolling a generic gallery.

---

## 🚀 Key Features

### 🎨 Earthy, Cohesive UI

- A custom forest-inspired color palette, warm cream (`#FEFAE0`) paired with deep pine tones (`#2D3A2B`), combined with Bootstrap Icons for a consistent, calming visual identity.

### 🖼️ Interactive Spotlight Hero Carousel

- A smooth, horizontally scrolling spotlight banner featuring a scroll progress bar and glassmorphism badges, designed to highlight standout photography front and center.

### 🧱 Masonry Discovery Grid

- A clean, responsive card layout displaying photography thumbnails, live view counters, EXIF-availability badges, and direct action triggers, built for effortless browsing.

### 🔍 Interactive Lightbox Modal

- A high-resolution lightbox modal that surfaces complete camera metadata without ever navigating away from the current page.

### ❤️ Asynchronous Like Engine

- Dynamic, AJAX-powered like toggling across grid cards, detail pages, and lightboxes, with instant feedback and zero page reloads or layout jumps.

### 📷 EXIF Metadata Engine

- Dedicated views expose full camera hardware specs for every photo, including **Aperture**, **Shutter Speed**, **ISO**, **Focal Length**, and **Location**.

### 🔎 Category Filters & Global Search

- Browse by category or search the entire collection to quickly surface the photography you're looking for.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | [Python 3.14](https://www.python.org/) + [Django 6.1](https://www.djangoproject.com/) | Core application logic, routing, and data models |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+ Fetch API) | Interactive UI behavior and AJAX-driven interactions |
| **UI Framework** | [Bootstrap 5](https://getbootstrap.com/) + Bootstrap Icons | Responsive layout system and iconography |
| **Database** | PostgreSQL *(under development)* | Persistent storage for photos, likes, views, and EXIF data |
| **Image Handling** | [Pillow](https://python-pillow.org/) | Image processing and EXIF metadata extraction |

---

## 📂 Project Structure

```
Canopy/
├── App/                        # Core Django application
│   ├── models.py               # Photo model (Image, Likes, Views, EXIF data)
│   ├── views.py                # View logic & JSON response handling for AJAX
│   ├── urls.py                 # Route mapping
│   └── templates/               # Application templates
│       ├── base.html            # Global navigation & asset dependencies
│       ├── index.html           # Masonry grid, hero carousel & lightbox modal
│       └── photo_detail.html    # Extended EXIF specs & dedicated photo view
├── Canopy/                     # Django project configuration (settings, WSGI/ASGI)
├── assets/                      # Design assets
├── images/                      # Uploaded/sample photography assets
├── static/                      # Static files (CSS, JS, icons)
├── manage.py                    # Django management entry point
└── requirements.txt              # Python dependencies
```

---

## ⚙️ Quick Start

### 1. Prerequisites

- [Python 3.10+](https://www.python.org/downloads/) installed on your machine

### 2. Clone the Repository

```bash
git clone https://github.com/Endurance3000/Canopy.git
cd Canopy
```

### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install django pillow
```

> Or, if `requirements.txt` is fully populated:
> ```bash
> pip install -r requirements.txt
> ```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Use this account to log into the Django admin panel and manage photo uploads.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/) in your browser to explore Canopy.

---

## 🤝 Contributing

Contributions are welcome — whether you're refining the UI, extending the EXIF engine, or fixing bugs.

1. **Fork** this repository.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add category-based trending section"
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** describing your change.

---

## 🐛 Issue Reporting & Support

If you encounter a bug or have a feature suggestion, please open an issue on the [GitHub Issues](https://github.com/Endurance3000/Canopy/issues) tracker, including:

- Steps to reproduce the issue
- Expected vs. observed behavior
- Browser/device details, if relevant

---

## 📜 License

This project is distributed under the [MIT License](https://github.com/Endurance3000/Canopy/blob/main/LICENSE). See the `LICENSE` file for full details.

---

<div align="center">
  <sub>Made for the quiet moments spent looking closer at the natural world.</sub><br>
  <strong>Canopy — Nature photography, presented with care.</strong>
</div>
