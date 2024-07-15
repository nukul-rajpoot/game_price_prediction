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

    public class SteamMarketApiCall
    {
        private HttpClient httpClient = new HttpClient();
        private string dailyCookie = "76561199704981720%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTcwQl8yNDkzRTBDMF80QkU4NSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MjEwNzczNTcsICJuYmYiOiAxNzEyMzUwMDkxLCAiaWF0IjogMTcyMDk5MDA5MSwgImp0aSI6ICIxN0EwXzI0QkI0MTEzXzg0NTU2IiwgIm9hdCI6IDE3MTgzNjI3ODYsICJydF9leHAiOiAxNzM2NjE4ODA2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiODEuMTA1LjIwMS41NyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.M3nzFki4BXTfumFlJsrFMteUxMv-0-Ipu25fMUikOo70hgtoVPhRJ3EZtcRumGgfXILLpc5lvPoNDdbXGMMFCQ";

        public SteamMarketApiCall()
        {
            // Assuming the cookie does not change frequently, set it once in the constructor
            httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={dailyCookie}");
        }

        //public async Task<JArray?> FetchItemFromApi(string item)
        //{
        //    string url = "https://steamcommunity.com/market/pricehistory/";
        //    var parameters = new Dictionary<string, string>
        //    {
        //        ["country"] = "US",
        //        ["currency"] = "1",
        //        ["appid"] = "730",
        //        ["market_hash_name"] = item
        //    };

        //    var response = await client.GetAsync(url + "?" + await new FormUrlEncodedContent(parameters).ReadAsStringAsync());

        //    if (response.IsSuccessStatusCode)
        //    {
        //        var json = await response.Content.ReadAsStringAsync();
        //        var jsonData = JObject.Parse(json);
        //        var prices = jsonData["prices"] as JArray;

        //        return prices;
        //    }
        //    else
        //    {
        //        Console.WriteLine($"Failed to fetch data for {item}. Status code: {response.StatusCode}");
        //        return null;
        //    }
        //}


        public async Task<string> FetchItemFromApiAsync(string item)
        {
            string url = "https://steamcommunity.com/market/pricehistory/";
            var queryParams = new Dictionary<string, string>
        {
            {"country", "US"},
            {"currency", "1"},
            {"appid", "730"},
            {"market_hash_name", item}
        };

            httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={dailyCookie}");

            var response = await httpClient.GetAsync($"{url}?{await new FormUrlEncodedContent(queryParams).ReadAsStringAsync()}");

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine($"Failed to fetch data for {item}. Status code: {response.StatusCode}");
                return null;
            }

            string rawPriceHistory = await response.Content.ReadAsStringAsync();
            string filteredPriceHistory = JObject.Parse(rawPriceHistory)["prices"].ToString();

            return filteredPriceHistory;
        }

        public async Task<DataFrame> JsonToDataFrame(string filteredPriceHistory)
        {
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
                }
                catch (OverflowException ex)
                {
                    // Handle cases where numeric data is out of range
                    Console.WriteLine($"Data overflow: {ex.Message}");
                }
            }

            return new DataFrame(dateColumn, priceColumn, volumeColumn);
            
        }


    }


}
