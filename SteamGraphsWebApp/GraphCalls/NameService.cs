namespace SteamGraphsWebApp.GraphCalls
{
    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.IO;
    using System.Reflection.PortableExecutable;
    using CsvHelper;
    using CsvHelper.Configuration;
    using CsvHelper.Configuration.Attributes;
    using Microsoft.Extensions.Hosting;

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

    public class NameService
    {
        public HashSet<Item> ReadFileToDict()
        {
            using (var reader = new StreamReader("Data\\market_hash_names.csv"))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var NamesList = csv.GetRecords<Item>().ToHashSet();
                return NamesList;
            }
        }
        
    }

}
