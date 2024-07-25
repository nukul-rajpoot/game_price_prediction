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
            DataFrame aggregatedVolume = df.GroupBy("date").Sum("volume");
            return aggregatedVolume;
        }
    }
}