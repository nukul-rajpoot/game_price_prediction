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
        [Index(0), Name("market_hash_name")]
        public string? MarketHashName { get; set; }

        [Index(1), Name("hash")]
        public string? Hash { get; set; }
    }

    public class NameService
    {
        public HashSet<Item> ReadFileToDict()
        {

            using (var reader = new StreamReader("C:\\Users\\Nukul\\Desktop\\Code\\game_price_prediction\\SteamGraphsWebApp\\hashed_items.csv"))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var records = csv.GetRecords<Item>().ToHashSet();
                return records;
            }
        }
        // clean item list ""

        
    }

}
