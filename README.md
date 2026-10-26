# Student Projects

Practical web development exercises by **Nima Khadeh**, exploring Python/Django and C#/ASP.NET Core through two application projects.

مجموعه پروژه‌های آموزشی برای تمرین توسعه وب با پایتون و سی‌شارپ.

## Projects

| Project | What it covers | Stack |
| --- | --- | --- |
| [BookStore](CSharpProjects/BookStore) | Book catalog, search, pagination, categories and CRUD operations | C# · ASP.NET Core MVC · .NET 8 · Entity Framework Core · SQLite |
| [Car Shop](PythonProjects/car_shop21) | Car listings, customer accounts, dealer profiles, cart, orders and a simulated payment flow | Python · Django 4.2 · SQLite · Django templates |

These are educational projects. Each directory contains its own application and configuration.

## Explore the code

```text
StudentProjects/
├── CSharpProjects/
│   └── BookStore/          # ASP.NET Core MVC application
└── PythonProjects/
    └── car_shop21/         # Django car marketplace exercise
```

### BookStore

The [BookStore guide](CSharpProjects/BookStore/README.md) describes the application and local setup using the .NET 8 SDK.

### Car Shop

Start with [manage.py](PythonProjects/car_shop21/manage.py), [settings](PythonProjects/car_shop21/car_shop/settings.py) and [URL routes](PythonProjects/car_shop21/car_shop/urls.py). The application includes separate Django apps for accounts, cars, dealers, articles, cart, orders, payments and notifications.

The current [dependency file](PythonProjects/car_shop21/requirements.txt) mixes package pins with `pip list` output and needs normalization before installation. The notification service also imports `requests`, which is absent from that file. Payment processing is simulated, and external notification settings use placeholders.

## Learning focus

- MVC and Django application structure
- Relational models and database persistence
- Forms, templates and CRUD workflows
- Search, pagination and user sessions
- Separating application features into modules

## فارسی

این مخزن شامل دو پروژه واقعی است: **فروشگاه کتاب با ASP.NET Core** و **نمایشگاه خودرو با Django**. برای شروع، راهنمای هر پروژه و تنظیمات همان پوشه را بررسی کنید. این نمونه‌ها برای یادگیری و توسعه محلی هستند؛ بخش پرداخت نمایشگاه خودرو شبیه‌سازی شده است.

## Author

[Nima Khadeh](https://github.com/nimakhadeh) · [Email](mailto:khadehnima@gmail.com)
