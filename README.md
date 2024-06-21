# Dev Demo Website (Django)

•	It has features including: likes, comments, ratings comparison, admin panel, user panel, upload and download functionality and multi-factor authentication (MFA). <br/>
•	It has e-commerce components including: shopping cart, quick view, checkout page, coupons and discounts.
•	It implemented on AWS server and Utilized EC2 instances, Load Balancer, S3, SNS, RDS for MySQL.
•	Integrated with third-party APIs in JSON format. Utilized Ajax requests to send and receive data from third-party APIs.

        Django – JS – Ajax – Html – CSS – Bootstrap – JSON (JWT)– MySQL – AWS S3 – AWS RDS (MySQL) – AWS EC2 

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- User authentication and authorization
- Custom permissions
- Product management
- Static and template files for the frontend
- Docker support for easy deployment

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Behzad-Rajabalipour/Dev-Demo-Website-Django.git
    cd Dev-Demo-Website-Django
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage
- Access the website at `http://127.0.0.1:8000/`
- Log in with your credentials or create a new account.

## Docker Support

To run the application using Docker:

1. **Build the Docker image:**
    ```bash
    docker-compose build
    ```

2. **Run the Docker containers:**
    ```bash
    docker-compose up
    ```

3. The application will be available at `http://localhost:8000/`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

 
