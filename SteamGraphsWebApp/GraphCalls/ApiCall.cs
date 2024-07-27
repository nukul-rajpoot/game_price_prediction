namespace SteamGraphsWebApp.GraphCalls
{
    using System;
    using System.Net.Http;
    using System.Threading.Tasks;
    using Newtonsoft.Json;
    using System.Data;
    using System.Globalization;
    using Newtonsoft.Json.Linq;
    using Microsoft.Data.Analysis;
    using System.Text.Json.Nodes;
    using Microsoft.AspNetCore.Http;
    using SteamGraphsWebApp.Models;

    public class ApiCalls
    {
        private HttpClient httpClient = new HttpClient();
        private string dailyCookie = "76561199704981720%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTcwQl8yNDkzRTBDMF80QkU4NSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MjIwOTM3MzUsICJuYmYiOiAxNzEzMzY1NzM1LCAiaWF0IjogMTcyMjAwNTczNSwgImp0aSI6ICIwRjdFXzI0QzlEMjQxX0RBN0M4IiwgIm9hdCI6IDE3MTgzNjI3ODYsICJydF9leHAiOiAxNzM2NjE4ODA2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiODEuMTA1LjIwMS41NyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.BTBZUmWW0tqsg68PCKAJx6w6CRe03Zx1cceRwHQistJhIBm-amBThkZc-L74ai70myDTx-pxC-YfUkYk1psECw";

        public ApiCalls()
        {
            // Assuming the cookie does not change frequently, set it once in the constructor
            httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={dailyCookie}");
        }

        public async Task<string?> FetchItemFromApi(SteamItemModel model)
        {
            string url = "https://steamcommunity.com/market/pricehistory/";
            var queryParams = new Dictionary<string, string>
            {
                {"country", "US"},
                {"currency", "1"},
                {"appid", "730"},
                {"market_hash_name", model.InputItemName}
            };

            httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={dailyCookie}");

            var response = await httpClient.GetAsync($"{url}?{await new FormUrlEncodedContent(queryParams).ReadAsStringAsync()}");

            if (response.IsSuccessStatusCode)
            {
                string rawPriceHistory = await response.Content.ReadAsStringAsync();
                string filteredPriceHistory = JObject.Parse(rawPriceHistory)["prices"].ToString();
                return filteredPriceHistory;

            }
            else
            {
                Console.WriteLine($"Failed to fetch data for {model.InputItemName}. Status code: {response.StatusCode}");
                return null;
            }
        }

        public async Task<DataFrame?> JsonToDataFrame(string filteredPriceHistory)
        {
            if (filteredPriceHistory == null) return null;

            var jsonArray = JArray.Parse(filteredPriceHistory);
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("date");
            var priceColumn = new PrimitiveDataFrameColumn<double>("price_usd");
            var volumeColumn = new PrimitiveDataFrameColumn<int>("volume");

            foreach (JArray item in jsonArray)
            {
                try
                {
                    string rawDate = (string) item[0];
                    string format = "MMM dd yyyy HH: z";
                    DateTimeOffset parsedDateTimeOffset = DateTimeOffset.ParseExact(rawDate, format, CultureInfo.InvariantCulture);
                    
                    dateColumn.Append(parsedDateTimeOffset.DateTime);
                    priceColumn.Append((double)item[1]);
                    volumeColumn.Append(int.Parse((string)item[2]));

                }
                catch (FormatException ex)
                {
                    // Handle parsing errors, or log them
                    Console.WriteLine($"Error parsing data: {ex.Message}");
                    return null;
                }
                catch (OverflowException ex)
                {
                    // Handle cases where numeric data is out of range
                    Console.WriteLine($"Data overflow: {ex.Message}");
                    return null;
                }
            }

            // aggregate data
            DataFrame PriceHistory = new DataFrame(dateColumn, priceColumn, volumeColumn);

            //DataFrame GroupedPriceHistory = PriceHistory.GroupBy("date").Mean("price_usd");
            //DataFrame df = GroupedPriceHistory.GroupBy("date").Sum("volume");

            return PriceHistory;


        }

        public async Task<DataFrame?> FetchItemToDataFrame(SteamItemModel model)
        {
            string? data = await FetchItemFromApi(model);
            //priceHistory.Info(); 
            if (data == null)
            {
                return null;
            }

            DataFrame? df = await JsonToDataFrame(data);

            return df;
            //Pass JSON data to the view
        }



        
    }

}
