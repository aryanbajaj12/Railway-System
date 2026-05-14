# 🚂 Antigravity Railway Reservation System

A professional Railway Reservation System built with Django, featuring a modern Indian Railways theme. This project provides a seamless booking experience with automated data population and real-time schedule integration.

## 🚀 Key Features

- **Professional Theming**: A clean, high-contrast "About" section and responsive navigation themed after standard rail utility portals.
- **Automated Indian Rail Data**: Automatically populates the database with 15 standard Indian trains (Rajdhani, Shatabdi, Vande Bharat, etc.) and major routes on first run.
- **Smart Booking Flow**: Integrated search, passenger management, and instant ticket generation.
- **Timing & Fare Integration**: Prominent display of departure/arrival times and distance-based fare calculations.
- **Resilient UI**: Fallback logic for missing train images to ensure a consistent visual experience across the project.
- **Admin Tools**: Full suite of management tools for trains, routes, and user registrations.

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Package Manager**: [uv](https://github.com/astral-sh/uv)

## 📦 Setup & Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd AB
   ```

2. **Install dependencies using `uv`**:

   ```bash
   uv sync
   ```

3. **Apply migrations**:

   ```bash
   uv run python manage.py migrate
   ```

4. **Run the development server**:

   ```bash
   uv run python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## 🚄 Warm-up Data

The system automatically populates 15 standard Indian trains if the database is empty. Visit the Dashboard or Search page to trigger the population.

## 🔧 Maintenance

- **Resetting Data**: If you need to refresh the train list, you can clear the `Add_Train` table through the Django admin or shell, and the system will re-populate it with the latest Indian Rail dataset.

## 📝 License

This project is for educational purposes.
