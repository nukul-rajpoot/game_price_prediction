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

    public class SteamMarketApiCall
    {
        private HttpClient httpClient = new HttpClient();
        private string dailyCookie = "76561199704981720%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTcwQl8yNDkzRTBDMF80QkU4NSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MjAzMTAwODksICJuYmYiOiAxNzExNTgzMzY2LCAiaWF0IjogMTcyMDIyMzM2NiwgImp0aSI6ICIwRjJEXzI0QTRFNzk3X0VGRUYzIiwgIm9hdCI6IDE3MTgzNjI3ODYsICJydF9leHAiOiAxNzM2NjE4ODA2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiODEuMTA1LjIwMS41NyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.WQUvXi9FBtDbzqXUcDYXVOeCICgH80t-yp-3ys5qK90QRAAcW6Ejdz_YE30WwWETbFTlCB29CYJvJmiCsv9wBA";

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


        public async Task<DataFrame> FetchItemFromApiAsync(string item)
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

            string jsonContent = await response.Content.ReadAsStringAsync();
            var jsonDocument = JArray.Parse(JObject.Parse(jsonContent)["prices"].ToString());

            var dates = new PrimitiveDataFrameColumn<DateTime>("Date");
            var prices = new PrimitiveDataFrameColumn<double>("PriceUSD");
            var volumes = new PrimitiveDataFrameColumn<int>("Volume");

            foreach (JArray record in jsonDocument)
            {
                string dateString = record[0].ToString();
                dates.Append(DateTime.ParseExact(dateString.Substring(0, dateString.Length - 4), "MMM dd yyyy HH", CultureInfo.InvariantCulture));
                prices.Append(double.Parse(record[1].ToString()));
                volumes.Append(int.Parse(record[2].ToString()));
            }

            var df = new DataFrame(dates, prices, volumes);
            df.Columns["Date"].SetName("Index");
            return df;
        }

        public string DataFrameToJson(DataFrame df)
        {
            var rows = new List<Dictionary<string, object>>();
            foreach (var row in df.Rows)
            {
                var rowDict = new Dictionary<string, object>();
                foreach (var column in df.Columns)
                {
                    rowDict[column.Name] = row[column.Name];
                }
                rows.Add(rowDict);
            }
            return JsonConvert.SerializeObject(rows);
        }

        public async Task<DataFrame> JArrayToDataFrame(JArray jsonArray)
        {
            return await Task.Run(() =>
            {
                var dateColumn = new PrimitiveDataFrameColumn<DateTime>("date");
                var priceColumn = new PrimitiveDataFrameColumn<double>("price_usd");
                var volumeColumn = new PrimitiveDataFrameColumn<int>("volume");

                foreach (JArray item in jsonArray)
                {
                    try
                    {
                        dateColumn.Append(DateTime.Parse((string)item[0]));
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
            });
        }


    }


}
