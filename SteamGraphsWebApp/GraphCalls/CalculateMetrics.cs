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

            foreach (var group in groupingsByDay)
            {
                int numberOfPrices = group.Count();
                //if (numberOfPrices == 1) continue;

                if (numberOfPrices % 2 == 0)
                {   
                    var row1 = group.ElementAt(numberOfPrices / 2 - 1);
                    var row2 = group.ElementAt(numberOfPrices / 2);
                    double median = ((double)row1["price_usd"] + (double)row2["price_usd"]) / 2;
                    row1["price_usd"] = median;
                    newDateColumn.Append((DateTime) row1["daily_date"]);
                    newPriceColumn.Append(median);
                }
                else if (numberOfPrices % 2 == 1)
                {
                    int middleIndex = numberOfPrices / 2;
                    var row = group.ElementAt(middleIndex);
                    newDateColumn.Append((DateTime) row["daily_date"]);
                    newPriceColumn.Append((double) row["price_usd"]);
                }
            }

            DataFrame aggregatedPriceDF = new DataFrame(newDateColumn, newPriceColumn);

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

        public async Task<DataFrame> CalculateSma(DataFrame df, int period)
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

        public async Task<DataFrame> CalculateEma(DataFrame df, int period)
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
            var emaColumn = new DoubleDataFrameColumn("price_ema", emaValues.Skip(period).Select(v => v ?? double.NaN)); // Handle nulls
            var dateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date", emaDates.Skip(period));

            var resultDataFrame = new DataFrame(dateColumn, emaColumn);

            return resultDataFrame;
        }

        public List<Quote> DataFrameToQuotes(DataFrame df)
        {
            // Extract the date and price columns into a list of Quote
            var quotes = new List<Quote>();
            DateTime[] dates = df.Columns["daily_date"].Cast<DateTime>().ToArray();
            double[] prices = df.Columns["price_usd"].Cast<double>().ToArray();

            for (int i = 0; i < df.Rows.Count; i++)
            {
                quotes.Add(new Quote
                {
                    Date = dates[i],
                    Close = (decimal)prices[i]
                });
            }
            return quotes;
        }

    }
}