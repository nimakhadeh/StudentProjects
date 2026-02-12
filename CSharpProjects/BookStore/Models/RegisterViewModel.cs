using System.ComponentModel.DataAnnotations;

namespace BookStore.Models;

public class RegisterViewModel
{
    [Required(ErrorMessage = "نام کاربری الزامی است")]
    [Display(Name = "نام کاربری")]
    public string Username { get; set; } = "";
    
    [Required(ErrorMessage = "رمز عبور الزامی است")]
    [DataType(DataType.Password)]
    [Display(Name = "رمز عبور")]
    public string Password { get; set; } = "";
    
    [Required(ErrorMessage = "تکرار رمز عبور الزامی است")]
    [DataType(DataType.Password)]
    [Display(Name = "تکرار رمز عبور")]
    [Compare("Password", ErrorMessage = "رمز عبور و تکرار آن یکسان نیستند")]
    public string ConfirmPassword { get; set; } = "";
}
