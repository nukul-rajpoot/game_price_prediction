namespace SteamGraphsWebApp.Models
{
    using System.ComponentModel.DataAnnotations;
    public class SteamItemViewModel
    {
        [Required]
        public string? SteamItemName { get; set; }

        //[Required]
        //[DataType(DataType.Password)]
        //public string Password { get; set; }

        //[Display(Name = "Remember me?")]
        //public bool RememberMe { get; set; }
    }

}
