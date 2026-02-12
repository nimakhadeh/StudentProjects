using Microsoft.AspNetCore.Mvc;
using BookStore.Models;
using Microsoft.AspNetCore.Http;
using System.Linq;

namespace BookStore.Controllers;

public class HomeController : Controller
{
    private readonly AppDbContext _context;
    private readonly IHttpContextAccessor _httpContextAccessor;
    
    public HomeController(AppDbContext context, IHttpContextAccessor httpContextAccessor)
    {
        _context = context;
        _httpContextAccessor = httpContextAccessor;
    }
    
    public IActionResult Index()
    {
        var books = _context.Books.Take(3).ToList();
        return View(books);
    }
    
    public IActionResult Login()
    {
        return View();
    }
    
    [HttpPost]
    public IActionResult Login(string username, string password)
    {
        var user = _context.Users.FirstOrDefault(u => u.Username == username && u.Password == password);
        if (user != null)
        {
            _httpContextAccessor.HttpContext?.Session?.SetString("UserId", user.Id.ToString());
            _httpContextAccessor.HttpContext?.Session?.SetString("Username", user.Username);
            return RedirectToAction("Index", "Books");
        }
        ViewBag.Error = "نام کاربری یا رمز عبور اشتباه است.";
        return View();
    }
    
    public IActionResult Logout()
    {
        _httpContextAccessor.HttpContext?.Session?.Clear();
        return RedirectToAction("Index");
    }
    
    public IActionResult Register()
    {
        return View();
    }
    
    [HttpPost]
    public IActionResult Register(RegisterViewModel model)
    {
        if (ModelState.IsValid)
        {
            var existingUser = _context.Users.FirstOrDefault(u => u.Username == model.Username);
            if (existingUser != null)
            {
                ModelState.AddModelError("Username", "این نام کاربری قبلاً ثبت شده است");
                return View(model);
            }
            
            var user = new User
            {
                Username = model.Username,
                Password = model.Password
            };
            
            _context.Users.Add(user);
            _context.SaveChanges();
            
            _httpContextAccessor.HttpContext?.Session?.SetString("UserId", user.Id.ToString());
            _httpContextAccessor.HttpContext?.Session?.SetString("Username", user.Username);
            
            return RedirectToAction("Index", "Books");
        }
        return View(model);
    }
}
