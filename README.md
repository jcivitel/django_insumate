[![](https://img.shields.io/maintenance/yes/2024)](https://github.com/jcivitel/)
[![Static Badge](https://img.shields.io/badge/GitHub-jcivitell-green?logo=github)](https://github.com/jcivitel/django_insumate)
[![GitHub Repo stars](https://img.shields.io/github/stars/jcivitel/django_insumate)](https://github.com/jcivitel/django_insumate)
[![Docker Pulls](https://img.shields.io/docker/pulls/jcivitell/insumate?logo=docker)](https://hub.docker.com/r/jcivitell/insumate)
[![Docker Stars](https://img.shields.io/docker/stars/jcivitell/insumate?logo=docker)](https://hub.docker.com/r/jcivitell/insumate)
[![Docker Image Size](https://img.shields.io/docker/image-size/jcivitell/insumate/latest?logo=docker)](https://hub.docker.com/r/jcivitell/insumate)


# InsuMate

## Project Purpose

This Django-based web application is designed to assist people with diabetes in managing their carbohydrate intake and insulin dosages. The primary goals of the project are:

1. **Carbohydrate Tracking**:
   - Allow users to quickly search for food items using barcodes
   - Record meals and their corresponding carbohydrate content (CU - Carbohydrate Units)

2. **Insulin Dose Calculation**:
   - Utilize user-specific profile data (likely including factors such as insulin sensitivity)
   - Consider time of day to apply appropriate insulin-to-carb ratios
   - Suggest insulin doses based on recorded meals

3. **Meal History**:
   - Provide a dashboard showing recent meal entries
   - Display total carbohydrate intake for the past 30 minutes

4. **User Convenience**:
   - Store recent food searches for quick access
   - Allow easy addition and deletion of meal entries

5. **Personalization**:
   - Enable users to maintain personal profiles with diabetes-specific data
   - Use this data to tailor calculations to individual needs

## Key Components

- **User Authentication**: Secure login system to protect personal health data
- **Product Database**: Quick retrieval of nutritional information via barcode
- **Calculation Engine**: Algorithms to determine appropriate insulin dosages
- **User-friendly Interface**: Intuitive design with supportive feedback messages

This application aims to simplify the daily task of managing diabetes by providing quick, personalized carbohydrate and insulin calculations, potentially improving glycemic control and quality of life for users.

## Technologies

- Python 3.x
- Django 3.x
- Bootstrap 5.x
- Redis 7.2.x
- MariaDB 11.4.x

## Installation
>[!TIP]
> You can use the predefined [docker compose](docs/quickstart)

1. Clone the repository:

```
    git clone https://github.com/jcivitel/django_insumate.git
    cd django_insumate
```

2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Run database migration:

```
    python manage.py migrate
```

## Contributing

Contributions are welcome! Please create an issue or pull request for suggestions or improvements.

## License

[BSD 3-Clause License](LICENSE)

# Contributors
[![Contributors Display](https://badges.pufler.dev/contributors/jcivitel/django_insumate?size=50&padding=5&bots=false)](https://github.com/jcivitel/django_insumate/graphs/contributors)
