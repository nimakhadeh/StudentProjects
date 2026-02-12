using System.ComponentModel.DataAnnotations;

namespace BookStore.Models;

public class Book
{
    public int Id { get; set; }
    
    [Required, StringLength(100)]
    public string Title { get; set; } = "";
    
    [Required, StringLength(100)]
    public string Author { get; set; } = "";
    
    [Required]
    public decimal Price { get; set; }
    
    [StringLength(50)]
    public string? Genre { get; set; }
    
    // ارتباط با دسته‌بندی
    public int CategoryId { get; set; }
    public Category? Category { get; set; }
}
