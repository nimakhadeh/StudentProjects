using System.ComponentModel.DataAnnotations;

namespace BookStore.Models;

public class Category
{
    public int Id { get; set; }
    
    [Required, StringLength(50)]
    public string Name { get; set; } = "";
    
    public ICollection<Book> Books { get; set; } = new List<Book>();
}
