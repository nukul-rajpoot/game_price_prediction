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
    using Microsoft.AspNetCore.DataProtection.KeyManagement;

    public class CalculateMetrics()
    {
        public async Task<DataFrame> MakeDailyDateColumn(DataFrame df)
        {
            var dailyDateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date");
            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime)row["date"];
                DateTime dailyDate = date.Date;
                dailyDateColumn.Append(dailyDate);
            }
            df["daily_date"] = dailyDateColumn;
            return df;
        }

        public async Task<DataFrame> AggregatePrice(DataFrame df)
        {
            df = await MakeDailyDateColumn(df);
            //DataFrame aggregatedPriceDf = df.GroupBy("daily_date").Median("price_usd");

            return CalculateMedian(df);
        }

        public async Task<DataFrame> AggregateVolume(DataFrame df)
        {
            df = await MakeDailyDateColumn(df);

            DataFrame aggregatedVolumeDf = df.GroupBy("daily_date").Sum("volume");

            return aggregatedVolumeDf;
        }

        public static DataFrame CalculateMedian(DataFrame dataFrame)
        {
            // Create a dictionary to group all rows (single group)
            var keyToRowIndices = new Dictionary<int, ICollection<long>> { { 0, Enumerable.Range(0, (int)dataFrame.Rows.Count).Select(i => (long)i).ToList() } };

            // Create a new DataFrame to store the result
            DataFrame result = new DataFrame();

            // Iterate over each column in the DataFrame
            foreach (var column in dataFrame.Columns)
            {
                // Convert the column to a list of doubles (if possible)
                var values = keyToRowIndices[0].Select(index => column[index])
                                                .Where(value => value != null && double.TryParse(value.ToString(), out _))
                                                .Select(value => Convert.ToDouble(value))
                                                .OrderBy(value => value)
                                                .ToList();

                // Calculate the median
                double median;
                int count = values.Count;
                if (count % 2 == 0)
                {
                    // Even number of elements
                    median = (values[count / 2 - 1] + values[count / 2]) / 2.0;
                }
                else
                {
                    // Odd number of elements
                    median = values[count / 2];
                }

                // Create a new column with the median value and add it to the result DataFrame
                var resultColumn = new PrimitiveDataFrameColumn<double>(column.Name, new double[] { median });
                result.Columns.Add(resultColumn);
            }

            return result;
        }


    }
}