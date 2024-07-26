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
    using Highsoft.Web.Mvc.Stocks;
    using SteamGraphsWebApp.GraphCalls;


    public class MakeGraphs
    {
        private readonly CalculateMetrics _calculateMetrics = new CalculateMetrics();

        public async Task<List<AreasplineSeriesData>> MakePriceHistoryGraph(DataFrame df)
        {
            List<AreasplineSeriesData> priceHistoryList= new List<AreasplineSeriesData>();

            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime) row["date"];
                priceHistoryList.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_usd"])
                });
            }
            return priceHistoryList;
        }

        public async Task<List<ColumnSeriesData>> MakeVolumeGraph(DataFrame df)
        {
            List<ColumnSeriesData> volumeDataList = new List<ColumnSeriesData>();

            DataFrame aggregatedVolumeDf = await _calculateMetrics.AggregateVolume(df);

            foreach (DataFrameRow row in aggregatedVolumeDf.Rows)
            {
                DateTime date = (DateTime) row["daily_date"];
                volumeDataList.Add(new ColumnSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["volume"])
                });
            }
            return volumeDataList;
        }

    }
}