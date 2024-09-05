namespace SteamGraphsWebApp.Models
{
    using System.ComponentModel.DataAnnotations;
    using System.Runtime.CompilerServices;
    using CsvHelper.Configuration.Attributes;
    using Microsoft.Data.Analysis;
    using SteamGraphsWebApp.GraphCalls;

    public class Item
    {
        [Name("market_hash_name")]
        public string? MarketHashName { get; set; }

        public override bool Equals(object? obj)
        {
            return obj is Item item &&
                   MarketHashName == item.MarketHashName;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(MarketHashName);
        }
    }

    public class SteamItemModel
    {
        [Required]
        public string? InputItemName { get; set; } = "Glove Case Key";
        public bool IsValidName { get; set; }

        public HashSet<Item> ItemList { get; set;
        }
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
