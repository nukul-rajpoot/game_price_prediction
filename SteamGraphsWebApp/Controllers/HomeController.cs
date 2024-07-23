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
using System.Reflection;
using Highsoft.Web.Mvc.Stocks;
using System;

namespace SteamGraphsWebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly SteamMarketApiCall steamMarketApiCall = new SteamMarketApiCall();
        private readonly NameService _nameService;

        public HomeController(ILogger<HomeController> logger, NameService nameService)
        {
            _logger = logger;
            _nameService = nameService;
        }

        public async Task<IActionResult> Index()
        {
            SteamItemModel model = new SteamItemModel();
            model.ValidateName(_nameService.ReadFileToDict());
            DataFrame? df = await steamMarketApiCall.FetchItemToDataFrame(model);
            //Pass JSON data to the view
            ViewBag.jsonPriceHistoryDate = df["date"];
            ViewBag.jsonPriceHistoryPrice = df["price_usd"];

            // new code
            List<AreasplineSeriesData> appleData = new List<AreasplineSeriesData>();

            foreach (DataFrameRow row in df.Rows)
            {
                DateTime date = (DateTime) row["date"];
                appleData.Add(new AreasplineSeriesData
                {
                    //X = (data.Date.ToUniversalTime() - new DateTime(1970, 1, 1, DateTimeKind.Utc)).TotalMilliseconds,
                    X = new DateTimeOffset(date).ToUnixTimeMilliseconds(),
                    Y = Convert.ToDouble(row["price_usd"])
                });
            }

            ViewBag.AppleData = appleData.OrderBy(o => o.X).ToList();

            return View(model);
        }

        // POST: Home
        [HttpPost]
        public async Task<IActionResult> Index(SteamItemModel model)
        {
            model.ValidateName(_nameService.ReadFileToDict());
            if (model.IsValidName)
            {
                DataFrame? df = await steamMarketApiCall.FetchItemToDataFrame(model);

                if (df != null)
                {
                    //Pass JSON data to the view
                    ViewBag.jsonPriceHistoryDate = df["date"];
                    ViewBag.jsonPriceHistoryPrice = df["price_usd"];
                }
            }
            else
            {
                ModelState.AddModelError("InputItemName", "Invalid item name");
                await Index();
            }

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
