# E-commerce Platform with Virtual Try-On and Sentiment Analysis

## Overview

This project is an E-commerce platform that includes both a web application and a mobile app, built to enhance the shopping experience by integrating a virtual try-on feature using Augmented Reality (AR) and sentiment analysis for product reviews.

## Features

- **Virtual Try-On**: Users can try on products virtually using AR technology.
- **Sentiment Analysis**: Automated analysis of user comments to determine sentiment (positive, negative, neutral).
- **Product Management**: CRUD operations for products, categories, and brands.
- **User Authentication**: JWT-based authentication for secure login and registration and logout .
- **Cart Management**: Add, Update, Remove items
- **Order Processing**: Checkout status
- **Image Uploads**: Access product images via URLs
- **Responsive Design**: Tailwind CSS and React for a mobile-friendly web application.
- **Mobile App**: Built with Flutter for a seamless cross-platform experience.

## Installation

### Backend Setup (Django)

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt

4. **Apply migrations:**

    ```sh
    python manage.py migrate

4. **Create a superuser:**

    ```sh
    python manage.py createsuperuser

5. **Run the development server:**

    ```sh
    python manage.py runserver

**Deployment**

API URL:
[https://o5l-astute-lyell.circumeo-apps.net/]
(https://o5l-astute-lyell.circumeo-apps.net/)
