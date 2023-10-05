# CRM Viajemos Travel


![CRM Web site](static/images/general/logo.jpg)

## Overview

- **Customer Management**: Easily add and manage customer profiles, including contact information and travel details.

- **Service Tracking**: Keep track of all the services provided to each client, including service history.

- **User Authentication**: Secure user authentication system for admin and staff members.

## Installation

Clone the repository:

```bash
git clone https://github.com/ronaldmh/python_django-travel.git
```
Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Migrate the database:
```
python manage.py migrate
```
Create a superuser account:
```
python manage.py createsuperuser
```
Create a superuser account:
```
python manage.py runserver
```

## Usage
- Log in using the superuser account created during installation.

- Begin by adding customers and generating quotes to the system.

- Generate services.


## Contribution

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.

Create a new branch for your feature or bug fix: git checkout -b feature/your-feature-name.

Make your changes and commit them: git commit -m 'Add some feature'.

Push to the branch: git push origin feature/your-feature-name.

Create a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, please feel free to contact me at ronaldmh20@gmail.com


# End
