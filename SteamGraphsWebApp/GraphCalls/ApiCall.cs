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
    using SteamGraphsWebApp.GraphCalls;
    using Microsoft.Net.Http.Headers;

    public class ApiCalls
    {
        private HttpClient _httpClient;
        private string cookie;

        public ApiCalls(HttpClient httpClient)
        {
            _httpClient = httpClient;
            cookie = GetCookieFromBlob().Result;
            _httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={cookie}");
        }

        public async Task<string> GetCookieFromBlob()
        {
            String blobUrl = "https://steamgraphsstorage.blob.core.windows.net/container-for-blob/cookie.txt?sp=r&st=2024-08-06T19:20:44Z&se=2024-08-07T03:20:44Z&spr=https&sv=2022-11-02&sr=c&sig=Csu5jI%2BbxXvLLBJMiV3KQWLEiFhp9uYDiUIoAUaKLoA%3D";

            var response = await _httpClient.GetAsync(blobUrl);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
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

            _httpClient.DefaultRequestHeaders.Add("Cookie", $"steamLoginSecure={cookie}");

            var response = await _httpClient.GetAsync($"{url}?{await new FormUrlEncodedContent(queryParams).ReadAsStringAsync()}");

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
