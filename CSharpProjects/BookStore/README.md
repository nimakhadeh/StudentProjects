# BookStore

An educational book catalog built with **ASP.NET Core MVC**, **Entity Framework Core** and **SQLite**.

پروژه آموزشی فروشگاه کتاب با سی‌شارپ، معماری MVC و پایگاه داده SQLite.

## Features

- Browse books with category details
- Search by title or author
- Paginate the catalog
- Create, edit and delete books after signing in
- Register, sign in and sign out using session-based application logic
- Initialize SQLite with sample categories, books and a demo account

## Stack

C# · .NET 8 · ASP.NET Core MVC · Entity Framework Core 8 · SQLite · Razor views · Bootstrap

## Run locally

Install the **.NET 8 SDK**, then run from the repository root:

```bash
cd CSharpProjects/BookStore
dotnet restore
dotnet run --launch-profile http
```

Open **http://localhost:5099**. The application creates its SQLite database on startup using `EnsureCreated()`; the connection is configured in `appsettings.json`.

## Project structure

```text
BookStore/
├── Controllers/     # Home, account actions and book CRUD
├── Models/          # Books, categories, users and database context
├── Views/           # Razor views and shared layout
├── wwwroot/         # Styles, scripts and static assets
└── Program.cs       # Services, database initialization and routing
```

## Educational scope

The current login flow stores passwords directly and uses a seeded demo account. Use this project locally with sample data; a deployed application needs password hashing, a complete authentication system and a review of write actions.

## فارسی

پس از نصب .NET 8، دستورهای بالا را اجرا کنید و آدرس محلی را باز کنید. امکانات پروژه شامل جست‌وجو، صفحه‌بندی، دسته‌بندی و افزودن، ویرایش و حذف کتاب است. ورود کاربران در این نسخه آموزشی ساده‌سازی شده است.

[Back to Student Projects](../../README.md) · [Nima Khadeh](https://github.com/nimakhadeh)
