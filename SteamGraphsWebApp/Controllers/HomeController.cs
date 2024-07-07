using Microsoft.AspNetCore.Mvc;
using SteamGraphsWebApp.Models;
using System.Diagnostics;
using SteamGraphsWebApp.PythonServices;
using SteamGraphsWebApp.GraphCalls;
using System.Data;
using Newtonsoft.Json.Linq;
using Microsoft.Data.Analysis;
using Newtonsoft.Json;

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



        public IActionResult Index()
        {

            //DataFrame priceHistory = new DataFrame(new List<DataFrameColumn> {
            //    new DateTimeDataFrameColumn("Index", new DateTime[] {
            //        new DateTime(2014, 2, 21, 1, 0, 0),
            //        new DateTime(2014, 2, 22, 1, 0, 0),
            //        new DateTime(2014, 2, 23, 1, 0, 0),
            //        new DateTime(2014, 2, 24, 1, 0, 0),
            //        new DateTime(2014, 2, 25, 1, 0, 0),
            //        new DateTime(2014, 2, 26, 1, 0, 0),
            //        new DateTime(2014, 2, 27, 1, 0, 0),
            //        new DateTime(2014, 2, 28, 1, 0, 0),
            //        new DateTime(2014, 3, 1, 1, 0, 0)
            //    }),
            //    new DoubleDataFrameColumn("PriceUSD", new double[] { 32.34, 27.399, 25.891, 28.326, 31.973, 32.784, 33.181, 33.472, 24.643 }),
            //    new Int32DataFrameColumn("Volume", new int[] { 198, 225, 183, 128, 90, 90, 75, 123, 238 })
            //});


            ////DataFrame priceHistory = await steamMarketApiCall.FetchItemFromApiAsync("AK-47 | Redline (Field-Tested)");
            //string jsonData = JsonConvert.SerializeObject(priceHistory);

            //// Pass JSON data to the view
            //ViewBag.JsonData = jsonData;
            ////string jsonObj = steamMarketApiCall.DataFrameToJson(priceHistory);
            ////ViewBag.JsonData = jsonObj;
            return View();
        }


        public void PrintDataTable(DataTable table)
        {
            foreach (DataColumn column in table.Columns)
            {
                Console.Write($"{column.ColumnName}\t");
            }
            Console.WriteLine();

            foreach (DataRow row in table.Rows)
            {
                foreach (var item in row.ItemArray)
                {
                    Console.Write($"{item}\t");
                }
                Console.WriteLine();
            }
        }

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
