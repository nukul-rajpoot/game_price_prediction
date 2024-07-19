namespace SteamGraphsWebApp.Models
{
    using System.ComponentModel.DataAnnotations;
    using System.Runtime.CompilerServices;
    using SteamGraphsWebApp.GraphCalls;

    public class SteamItemModel
    {
        [Required]
        public string? InputItemName { get; set; } = "Glove Case Key";
        public bool IsValidName { get; set; }

        public void ValidateName(List<string> validNames)
        {
            if (string.IsNullOrEmpty(InputItemName))
            {
                IsValidName = false;
            }
            else
            {
                IsValidName = true;
            }
        }

    }

}
