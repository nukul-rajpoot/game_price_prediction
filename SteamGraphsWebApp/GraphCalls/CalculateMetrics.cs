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

    public class CalculateMetrics()
    {
        public async Task<DataFrame> AggregateVolume(DataFrame df)
        {
            var dailyDateColumn = new PrimitiveDataFrameColumn<DateTime>("daily_date");
            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime) row["date"];
                DateTime dailyDate = date.Date;
                dailyDateColumn.Append(dailyDate);
            }
            df["daily_date"] = dailyDateColumn;
            DataFrame aggregatedVolumeDf = df.GroupBy("daily_date").Sum("volume");

            return aggregatedVolumeDf;
        }
    }
}