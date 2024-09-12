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
    using SteamGraphsWebApp.Models;

    public class ItemFetchService
    {
        public HashSet<Item> GetItemList()
        {
            var config = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = true,
                TrimOptions = TrimOptions.Trim,
            };

            using (var reader = new StreamReader("Data/market_hash_names.csv"))
            using (var csv = new CsvReader(reader, config))
            {
                var items = csv.GetRecords<Item>();
                return new HashSet<Item>(items);
            }
        }
    }

}
