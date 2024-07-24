﻿namespace SteamGraphsWebApp.GraphCalls
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
    using Highsoft.Web.Mvc.Stocks;

    public class MakeGraphs
    {
        public async Task<List<AreasplineSeriesData>> ListPriceHistoryGraph(DataFrame df)
        {
            List<AreasplineSeriesData> appleData = new List<AreasplineSeriesData>();

            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime)row["date"];
                appleData.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_usd"])
                });
            }
            return appleData;
        }

    }
}