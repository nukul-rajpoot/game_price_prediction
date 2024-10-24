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
    using Microsoft.AspNetCore.DataProtection.KeyManagement;
    using System.Text.RegularExpressions;
    using Microsoft.Ajax.Utilities;
    using System.Linq;
    using Skender.Stock.Indicators;
    using Highsoft.Web.Mvc.Stocks;

    public class CalculateMetrics()
    {
        public async Task<DataFrame> MakeDailyDateColumn(DataFrame df)
        {
            var dailyDateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date");
            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime)row["date"];
                DateOnly dailyDate = DateOnly.FromDateTime(date);
                DateTime dateTimeWithoutTime = dailyDate.ToDateTime(TimeOnly.MinValue);

                dailyDateColumn.Append(dateTimeWithoutTime);
            }
            df["daily_date"] = dailyDateColumn;
            return df;
        }

        public async Task<DataFrame> AggregatePrice(DataFrame df)
        {
            df = await MakeDailyDateColumn(df);
            var groupingsByDay = df.Rows.GroupBy(row => row["daily_date"]);
            var newDateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date");
            var newPriceColumn = new PrimitiveDataFrameColumn<double>("price_usd");
            var closePriceColumn = new PrimitiveDataFrameColumn<double>("close");

            DataFrame lowDf = df.GroupBy("daily_date").Min("price_usd");
            DataFrame highDf = df.GroupBy("daily_date").Max("price_usd");
            DataFrame openDf = df.GroupBy("daily_date").First("price_usd");
            //DataFrame closeDf = df.GroupBy("daily_date").Last("price_usd");

            var lowPriceColumn = lowDf["price_usd"];
            lowPriceColumn.SetName("low");

            var highPriceColumn = highDf["price_usd"];
            highPriceColumn.SetName("high");

            var openPriceColumn = openDf["price_usd"];
            openPriceColumn.SetName("open");

            // calculate median for each day
            foreach (var group in groupingsByDay)
            {
                int numberOfPrices = group.Count();

                // only 1 daily value = add it to new
                if (numberOfPrices == 1)
                {
                    var row = group.ElementAt(0);
                    newDateColumn.Append((DateTime)row["daily_date"]);
                    newPriceColumn.Append((double)row["price_usd"]);
                    // add to close column
                    closePriceColumn.Append((double)row["price_usd"]);
                    continue;
                }

                // sort and calculate median value in group
                var sortedGroup = group.OrderBy(row => (double)row["price_usd"]);

                if (numberOfPrices % 2 == 0)
                {
                    var row1 = sortedGroup.ElementAt(numberOfPrices / 2 - 1);
                    var row2 = sortedGroup.ElementAt(numberOfPrices / 2);
                    double median = ((double)row1["price_usd"] + (double)row2["price_usd"]) / 2;
                    newDateColumn.Append((DateTime)row1["daily_date"]);
                    newPriceColumn.Append(median);
                }
                else if (numberOfPrices % 2 == 1)
                {
                    var row = sortedGroup.ElementAt(numberOfPrices / 2);
                    double median = (double)row["price_usd"];
                    newDateColumn.Append((DateTime)row["daily_date"]);
                    newPriceColumn.Append((double)row["price_usd"]);
                }

                // add close value of group to close price column
                var closeValueRow = group.Last();
                closePriceColumn.Append((double)closeValueRow["price_usd"]);

            }

            DataFrame aggregatedPriceDF = new DataFrame(newDateColumn, newPriceColumn, lowPriceColumn, highPriceColumn, openPriceColumn, closePriceColumn);
            //var test = aggregatedPriceDF.Tail(5);
            return aggregatedPriceDF;
        }

        public async Task<DataFrame> AggregateVolume(DataFrame df)
        {
            df = await MakeDailyDateColumn(df);

            DataFrame aggregatedVolumeDf = df.GroupBy("daily_date").Sum("volume");
            //var tail = aggregatedVolumeDf.Tail(5);

            return aggregatedVolumeDf;
        }

        public async Task<DataFrame> CalculateLnPriceHistory(DataFrame df)
        {
            // Create a copy of the original DataFrame

            // Apply log transformation to 'price_usd' column
            var priceUsdColumn = df.Columns["price_usd"] as PrimitiveDataFrameColumn<double>;
            var priceUsdLogColumn = new PrimitiveDataFrameColumn<double>("price_usd_log", priceUsdColumn.Select(price => Math.Log(1 + (double) price)));
            // Apply log transformation to 'volume' column
            //var volumeColumn = df.Columns["volume"] as PrimitiveDataFrameColumn<double>;
            //var volumeLogColumn = new PrimitiveDataFrameColumn<double>("volume_log", volumeColumn.Select(volume => Math.Log(1 + (double) volume)));

            // Add the new columns to the DataFrame
            DataFrame lnDf = df;

            lnDf.Columns.Add(priceUsdLogColumn);
            //lnDf.Columns.Add(volumeLogColumn);

            return lnDf;
        }

        public async Task<DataFrame> CalculateSma(DataFrame df, int period = 50)
        {
            // Extract the date and price columns into a list of Quote
            var quotes = DataFrameToQuotes(df);

            // Calculate SMA
            IEnumerable<SmaResult> smaResults = quotes.GetSma(period);

            // Prepare new DataFrame columns
            var smaDates = new List<DateTime>();
            var smaValues = new List<double?>();

            foreach (var result in smaResults)
            {
                smaDates.Add(result.Date);
                smaValues.Add(result.Sma);
            }

            // Create the resulting DataFrame
            var smaColumn = new DoubleDataFrameColumn("price_sma", smaValues.Skip(period).Select(v => v ?? double.NaN)); // Handle nulls
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", smaDates.Skip(period));

            var resultDataFrame = new DataFrame(dateColumn, smaColumn);

            return resultDataFrame;
        }

        public async Task<DataFrame> CalculateEma(DataFrame df, int period = 20)
        {

            var quotes = DataFrameToQuotes(df);
            // Calculate EMA
            IEnumerable<EmaResult> emaResults = quotes.GetEma(period);

            // Prepare new DataFrame columns
            var emaDates = new List<DateTime>();
            var emaValues = new List<double?>();

            foreach (var result in emaResults)
            {
                emaDates.Add(result.Date);
                emaValues.Add(result.Ema);
            }

            // Create the resulting DataFrame
            // skip the null rows!
            var emaColumn = new DoubleDataFrameColumn("price_ema", emaValues.Skip(period).Select(v => v ?? double.NaN)); // Handle nulls
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", emaDates.Skip(period));

            var resultDataFrame = new DataFrame(dateColumn, emaColumn);

            return resultDataFrame;
        }

        public async Task<DataFrame> CalculateBollingerBands(DataFrame df, int period = 20, int k = 2)
        {
            var quotes = DataFrameToQuotes(df);

            // Calculate Bollinger Bands
            var bbResults = quotes.GetBollingerBands(period, k).ToList();

            // Create the resulting DataFrame columns
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", bbResults.Skip(period).Select(r => r.Date));
            var middleBandColumn = new DoubleDataFrameColumn("price_sma", bbResults.Skip(period).Select(r => r.Sma ?? double.NaN));
            var upperBandColumn = new DoubleDataFrameColumn("price_bbl", bbResults.Skip(period).Select(r => r.UpperBand ?? double.NaN));
            var lowerBandColumn = new DoubleDataFrameColumn("price_bbu", bbResults.Skip(period).Select(r => r.LowerBand ?? double.NaN));

            // Create and return the DataFrame
            var resultDataFrame = new DataFrame(dateColumn, middleBandColumn, upperBandColumn, lowerBandColumn);

            return resultDataFrame;
        }

        public async Task<DataFrame> CalculateRsi(DataFrame df, int period = 14)
        {

            var quotes = DataFrameToQuotes(df);
            // Calculate EMA
            IEnumerable<RsiResult> rsiResults = quotes.GetRsi(period);

            // Prepare new DataFrame columns
            var rsiDates = new List<DateTime>();
            var rsiValues = new List<double?>();

            foreach (var result in rsiResults)
            {
                rsiDates.Add(result.Date);
                rsiValues.Add(result.Rsi);
            }

            // Create the resulting DataFrame
            // skip the null rows!
            var rsiColumn = new DoubleDataFrameColumn("price_rsi", rsiValues.Skip(period).Select(v => v ?? double.NaN)); // Handle nulls
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", rsiDates.Skip(period));

            var resultDataFrame = new DataFrame(dateColumn, rsiColumn);

            return resultDataFrame;
        }

        public async Task<DataFrame> CalculateMfi(DataFrame df, int period = 14)
        {

            var quotes = DataFrameToQuotes(df);

            //var aggregatedQuotes = quotes
            //.GroupBy(q => new { Year = q.Date.Year, Week = CultureInfo.InvariantCulture.Calendar.GetWeekOfYear(q.Date, CalendarWeekRule.FirstFourDayWeek, DayOfWeek.Monday) })
            //.Select(g => new Quote
            //{
            //    Date = g.Last().Date,
            //    Open = g.First().Open,
            //    High = g.Max(q => q.High),
            //    Low = g.Min(q => q.Low),
            //    Close = g.Last().Close,
            //    Volume = g.Sum(q => q.Volume)
            //})
            //.ToList();


            // Calculate EMA
            IEnumerable<MfiResult> mfiResults = quotes.GetMfi(2);

            // Prepare new DataFrame columns
            var mfiDates = new List<DateTime>();
            var mfiValues = new List<double?>();

            foreach (var result in mfiResults)
            {
                mfiDates.Add(result.Date);
                mfiValues.Add(result.Mfi);
            }

            // Create the resulting DataFrame
            // skip the null rows!
            var mfiColumn = new DoubleDataFrameColumn("price_mfi", mfiValues.Skip(period).Select(v => v ?? double.NaN)); // Handle nulls
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", mfiDates.Skip(period));

            var resultDataFrame = new DataFrame(dateColumn, mfiColumn);

            return resultDataFrame;
        }

        public List<Quote> DataFrameToQuotes(DataFrame df)
        {
            // Extract the date and price columns into a list of Quote
            var quotes = new List<Quote>();
            DateTime[] dates = df.Columns["daily_date"].Cast<DateTime>().ToArray();
            double[] prices = df.Columns["price_usd"].Cast<double>().ToArray();
            double[] low = df.Columns["low"].Cast<double>().ToArray();
            double[] high = df.Columns["high"].Cast<double>().ToArray();
            double[] open = df.Columns["open"].Cast<double>().ToArray();
            double[] close = df.Columns["close"].Cast<double>().ToArray();
            var test = df.Tail(100);
            for (int i = 0; i < df.Rows.Count; i++)
            {
                quotes.Add(new Quote
                {
                    Date = dates[i],
                    Low = (decimal)low[i],
                    High = (decimal)high[i],
                    Open = (decimal)open[i],
                    Close = (decimal)close[i],
                });
            }
            return quotes;
        }

    }
}