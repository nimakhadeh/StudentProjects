using Microsoft.EntityFrameworkCore;

namespace BookStore.Models;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    
    public DbSet<Book> Books { get; set; }
    public DbSet<User> Users { get; set; }
    public DbSet<Category> Categories { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Seed دسته‌بندی‌ها
        modelBuilder.Entity<Category>().HasData(
            new Category { Id = 1, Name = "رمان" },
            new Category { Id = 2, Name = "تاریخی" },
            new Category { Id = 3, Name = "علمی" },
            new Category { Id = 4, Name = "برنامه‌نویسی" },
            new Category { Id = 5, Name = "فلسفی" }
        );
        
        // کاربر پیش‌فرض
        modelBuilder.Entity<User>().HasData(
            new User { Id = 1, Username = "admin", Password = "123" }
        );
        
        // کتاب‌های نمونه با CategoryId
        modelBuilder.Entity<Book>().HasData(
            new Book { Id = 1, Title = "هابیت", Author = "جی.آر.آر. تالکین", Price = 15.99m, Genre = "فانتزی", CategoryId = 1 },
            new Book { Id = 2, Title = "۱۹۸۴", Author = "جورج اورول", Price = 12.50m, Genre = "دیستوپیا", CategoryId = 5 },
            new Book { Id = 3, Title = "کد تمیز", Author = "رابرت سی. مارتین", Price = 45.00m, Genre = "برنامه‌نویسی", CategoryId = 4 }
        );
    }
}
