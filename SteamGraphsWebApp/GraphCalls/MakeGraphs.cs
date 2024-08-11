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
    using Skender.Stock.Indicators;

    public class MakeGraphs
    {
        private readonly CalculateMetrics _calculateMetrics = new CalculateMetrics();

        public async Task<List<LineSeriesData>> MakePriceHistoryLineGraph(DataFrame df)
        {
            List<LineSeriesData> priceHistoryList = new List<LineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            foreach (DataFrameRow row in aggregatedPriceDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                priceHistoryList.Add(new LineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_usd"])
                });
            }
            return priceHistoryList;
        }

        public async Task<List<AreasplineSeriesData>> MakePriceHistoryGraph(DataFrame df)
        {
            List<AreasplineSeriesData> priceHistoryList = new List<AreasplineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            foreach (DataFrameRow row in aggregatedPriceDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
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
                DateTime date = (DateTime)row["daily_date"];
                volumeDataList.Add(new ColumnSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["volume"])
                });
            }
            return volumeDataList;
        }

        public async Task<List<AreasplineSeriesData>> MakeLnPriceHistoryGraph(DataFrame df)
        {
            List<AreasplineSeriesData> LnPriceHistoryList = new List<AreasplineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            DataFrame lnPriceHistoryDf = await _calculateMetrics.CalculateLnPriceHistory(aggregatedPriceDf);

            foreach (DataFrameRow row in lnPriceHistoryDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                LnPriceHistoryList.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_usd_log"])
                });
            }
            return LnPriceHistoryList;
        }

        public async Task<List<AreasplineSeriesData>> MakeSmaGraph(DataFrame df)
        {
            List<AreasplineSeriesData> LnPriceHistoryList = new List<AreasplineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            DataFrame lnPriceHistoryDf = await _calculateMetrics.CalculateSma(aggregatedPriceDf, 7);

            foreach (DataFrameRow row in lnPriceHistoryDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                LnPriceHistoryList.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_sma"])
                });
            }
            return LnPriceHistoryList;
        }

        public async Task<List<AreasplineSeriesData>> MakeEmaGraph(DataFrame df)
        {
            List<AreasplineSeriesData> LnPriceHistoryList = new List<AreasplineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            DataFrame lnPriceHistoryDf = await _calculateMetrics.CalculateEma(aggregatedPriceDf, 7);

            foreach (DataFrameRow row in lnPriceHistoryDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                LnPriceHistoryList.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_ema"])
                });
            }
            return LnPriceHistoryList;
        }

        public async Task<List<ArearangeSeriesData>> MakeBollingerBandsGraph(DataFrame df)
        {
            //List<AreasplineSeriesData> smaList = new List<AreasplineSeriesData>();
            List<ArearangeSeriesData> bbList = new List<ArearangeSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            DataFrame bbDf = await _calculateMetrics.CalculateBollingerBands(aggregatedPriceDf);

            foreach (DataFrameRow row in bbDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                //smaList.Add(new AreasplineSeriesData
                //{
                //    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                //    Y = Convert.ToDouble(row["sma"]),
                //});
                bbList.Add(new ArearangeSeriesData
                {
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Low = Convert.ToDouble(row["price_bbl"]),
                    High = Convert.ToDouble(row["price_bbu"]),
                });
            }
            //var fullList = new List<object> { smaList, bbList };
            return bbList;
        }

        public async Task<List<LineSeriesData>> MakeSmaLineGraph(DataFrame df)
        {
            List<LineSeriesData> smaLineList = new List<LineSeriesData>();

            DataFrame aggregatedPriceDf = await _calculateMetrics.AggregatePrice(df);

            DataFrame smaLineDf = await _calculateMetrics.CalculateBollingerBands(aggregatedPriceDf);

            foreach (DataFrameRow row in smaLineDf.Rows)
            {
                DateTime date = (DateTime)row["daily_date"];
                smaLineList.Add(new LineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_sma"])
                });
            }
            return smaLineList;
        }

    }
}