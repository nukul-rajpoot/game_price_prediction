using Microsoft.AspNetCore.Mvc;
using SteamGraphsWebApp.Models;
using System.Diagnostics;
using SteamGraphsWebApp.PythonServices;
using SteamGraphsWebApp.GraphCalls;
using System.Data;
using Newtonsoft.Json.Linq;
using Microsoft.Data.Analysis;
using Newtonsoft.Json;
using Python.Runtime;

namespace SteamGraphsWebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly SteamMarketApiCall steamMarketApiCall = new SteamMarketApiCall();

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            string data = await steamMarketApiCall.FetchItemFromApiAsync("AK-47 | Redline (Field-Tested)");
            //priceHistory.Info(); 

            DataFrame df= await steamMarketApiCall.JsonToDataFrame(data);

            //Pass JSON data to the view
            ViewBag.jsonPriceHistoryDate = df["date"];
            ViewBag.jsonPriceHistoryPrice = df["price_usd"];

            //string jsonObj = steamMarketApiCall.DataFrameToJson(priceHistory);
            //ViewBag.ExampleData = jsonObj;
            return View();
        }


        //public void PrintDataTable(DataTable table)
        //{
        //    foreach (DataColumn column in table.Columns)
        //    {
        //        Console.Write($"{column.ColumnName}\t");
        //    }
        //    Console.WriteLine();

        //    foreach (DataRow row in table.Rows)
        //    {
        //        foreach (var item in row.ItemArray)
        //        {
        //            Console.Write($"{item}\t");
        //        }
        //        Console.WriteLine();
        //    }
        //}

        // POST: Home
        [HttpPost]
        public IActionResult Index(SteamItemViewModel model)
        {
            return View(model);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
