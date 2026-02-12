using Microsoft.AspNetCore.Mvc;
using BookStore.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Http;
using System.Linq;
using X.PagedList;

namespace BookStore.Controllers;

public class BooksController : Controller
{
    private readonly AppDbContext _context;
    private readonly IHttpContextAccessor _httpContextAccessor;
    
    public BooksController(AppDbContext context, IHttpContextAccessor httpContextAccessor)
    {
        _context = context;
        _httpContextAccessor = httpContextAccessor;
    }
    
    private bool IsLoggedIn()
    {
        return _httpContextAccessor.HttpContext?.Session?.GetString("UserId") != null;
    }
    
    public IActionResult Index(string searchString, int? page)
    {
        ViewBag.CurrentFilter = searchString;
        int pageSize = 6;
        int pageNumber = page ?? 1;
        
        var books = _context.Books
            .Include(b => b.Category)   // بارگذاری دسته‌بندی
            .AsQueryable();
            
        if (!string.IsNullOrEmpty(searchString))
        {
            books = books.Where(b => b.Title.Contains(searchString) || b.Author.Contains(searchString));
        }
        
        var pagedList = books.OrderBy(b => b.Title).ToPagedList(pageNumber, pageSize);
        return View(pagedList);
    }
    
    public IActionResult Details(int id)
    {
        var book = _context.Books
            .Include(b => b.Category)
            .FirstOrDefault(b => b.Id == id);
        if (book == null) return NotFound();
        return View(book);
    }
    
    public IActionResult Create()
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        ViewBag.Categories = _context.Categories.ToList();
        return View();
    }
    
    [HttpPost]
    public IActionResult Create(Book book)
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        if (ModelState.IsValid)
        {
            _context.Books.Add(book);
            _context.SaveChanges();
            return RedirectToAction("Index");
        }
        ViewBag.Categories = _context.Categories.ToList();
        return View(book);
    }
    
    public IActionResult Edit(int id)
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        var book = _context.Books.Find(id);
        if (book == null) return NotFound();
        ViewBag.Categories = _context.Categories.ToList();
        return View(book);
    }
    
    [HttpPost]
    public IActionResult Edit(int id, Book book)
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        if (id != book.Id) return NotFound();
        if (ModelState.IsValid)
        {
            _context.Update(book);
            _context.SaveChanges();
            return RedirectToAction("Index");
        }
        ViewBag.Categories = _context.Categories.ToList();
        return View(book);
    }
    
    public IActionResult Delete(int id)
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        var book = _context.Books
            .Include(b => b.Category)
            .FirstOrDefault(b => b.Id == id);
        if (book == null) return NotFound();
        return View(book);
    }
    
    [HttpPost, ActionName("Delete")]
    public IActionResult DeleteConfirmed(int id)
    {
        if (!IsLoggedIn()) return RedirectToAction("Login", "Home");
        var book = _context.Books.Find(id);
        if (book != null)
        {
            _context.Books.Remove(book);
            _context.SaveChanges();
        }
        return RedirectToAction("Index");
    }
}
