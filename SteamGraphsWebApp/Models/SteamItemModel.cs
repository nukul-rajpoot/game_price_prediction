namespace SteamGraphsWebApp.Models
{
    using System.ComponentModel.DataAnnotations;
    using System.Runtime.CompilerServices;
    using Microsoft.Data.Analysis;
    using SteamGraphsWebApp.GraphCalls;

    public class SteamItemModel
    {
        [Required]
        public string? InputItemName { get; set; } = "Glove Case Key";
        public bool IsValidName { get; set; }

        public void ValidateName(HashSet<Item> NamesList)
        {
            bool inList = NamesList.Contains(new Item { MarketHashName = InputItemName });
            if (string.IsNullOrEmpty(InputItemName) || !inList)
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
