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
using System.Net;

namespace SteamGraphsWebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly ApiCalls _apiCalls;
        private readonly ItemFetchService _itemFetchService;
        private readonly MakeGraphs _makeGraphs;

        public HomeController(ILogger<HomeController> logger, ItemFetchService itemFetchService, MakeGraphs makeGraphs, ApiCalls apiCalls)
        {
            _logger = logger;
            _itemFetchService = itemFetchService;
            _makeGraphs = makeGraphs;
            _apiCalls = apiCalls;
        }

        public async Task<IActionResult> Index()
        {
            SteamItemModel model = new SteamItemModel();
            model.ValidateName(_itemFetchService.GetItemList());
            DataFrame? df = await _apiCalls.FetchItemToDataFrame(model);
            //Pass JSON data to the view
            ViewBag.jsonPriceHistoryDate = df["date"];
            ViewBag.jsonPriceHistoryPrice = df["price_usd"];

            ViewBag.NavigatorData = await _makeGraphs.MakePriceHistoryLineGraph(df);

            ViewBag.PriceHistoryHighChart = await _makeGraphs.MakePriceHistoryGraph(df);
            ViewBag.LnPriceHistoryHighChart = await _makeGraphs.MakeLnPriceHistoryGraph(df);
            ViewBag.SmaHighChart = await _makeGraphs.MakeSmaGraph(df);
            ViewBag.EmaHighChart = await _makeGraphs.MakeEmaGraph(df);

            ViewBag.BBHighChart = await _makeGraphs.MakeBollingerBandsGraph(df);
            ViewBag.SmaLineHighChart = await _makeGraphs.MakeSmaLineGraph(df);

            ViewBag.RsiHighChart = await _makeGraphs.MakeRsiGraph(df);

            // need to use with data with multiple price values for a day
            //ViewBag.MfiHighChart = await _makeGraphs.MakeMfiGraph(df);

            ViewBag.VolumeData = await _makeGraphs.MakeVolumeGraph(df);

            return View(model);
        }

       //POST: Home
       [HttpPost]
        public async Task<IActionResult> Index(SteamItemModel model)
        {
            model.ValidateName(_itemFetchService.GetItemList());
            if (model.IsValidName)
            {
                DataFrame? df = await _apiCalls.FetchItemToDataFrame(model);

                if (df != null)
                {
                    //Pass JSON data to the view
                    ViewBag.jsonPriceHistoryDate = df["date"];
                    ViewBag.jsonPriceHistoryPrice = df["price_usd"];

                    ViewBag.NavigatorData = await _makeGraphs.MakePriceHistoryLineGraph(df);

                    ViewBag.PriceHistoryHighChart = await _makeGraphs.MakePriceHistoryGraph(df);
                    ViewBag.LnPriceHistoryHighChart = await _makeGraphs.MakeLnPriceHistoryGraph(df);
                    ViewBag.SmaHighChart = await _makeGraphs.MakeSmaGraph(df);
                    ViewBag.EmaHighChart = await _makeGraphs.MakeEmaGraph(df);

                    ViewBag.BBHighChart = await _makeGraphs.MakeBollingerBandsGraph(df);
                    ViewBag.SmaLineHighChart = await _makeGraphs.MakeSmaLineGraph(df);

                    ViewBag.RsiHighChart = await _makeGraphs.MakeRsiGraph(df);

                    // need to use with data with multiple price values for a day
                    //ViewBag.MfiHighChart = await _makeGraphs.MakeMfiGraph(df);

                    ViewBag.VolumeData = await _makeGraphs.MakeVolumeGraph(df);
                }
            }
            else
            {
                ModelState.AddModelError("InputItemName", "Invalid item name");
                await Index();
            }

            return View(model);
        }

        //[HttpGet]
        //public ActionResult Index()
        //{
        //    return View();
        //}

        //[HttpPost]
        //public JsonResult Index(string Prefix)
        //{
        //    HashSet<Item> ItemList = _itemFetchService.GetItemList();

        //    //Searching records from list using LINQ query
        //    var Name = (from N in ItemList
        //                where N.MarketHashName.StartsWith(Prefix)
        //                select new { N.MarketHashName });
        //    return Json(Name);
        //}

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
