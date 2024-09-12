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
        private readonly SteamItemModel _steamItemModel;

        public HomeController(ILogger<HomeController> logger, ItemFetchService itemFetchService, MakeGraphs makeGraphs, ApiCalls apiCalls)
        {
            _logger = logger;
            _itemFetchService = itemFetchService;
            _makeGraphs = makeGraphs;
            _apiCalls = apiCalls;
            _steamItemModel = new SteamItemModel();
            _steamItemModel.ItemList = _itemFetchService.GetItemList();
        }

        public async Task<IActionResult> Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Search(SteamItemModel model)
        {
            model.ValidateName(_steamItemModel.ItemList);
            if (model.IsValidName)
            {
                DataFrame? df = await _apiCalls.FetchItemToDataFrame(model);

                if (df != null)
                {
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
            }

            return View(model);
        }

        [HttpGet]
        public JsonResult AutoComplete(string prefix)
        {
            if (string.IsNullOrWhiteSpace(prefix) || prefix.Length < 2)
            {
                return Json(new List<object>());
            }

            var itemList = _steamItemModel.ItemList;
            var lowercasePrefix = prefix.ToLower();
            var suggestions = itemList
                .Where(item => item.MarketHashName.Split(' ')
                    .Any(word => word.StartsWith(lowercasePrefix, StringComparison.OrdinalIgnoreCase)))
                .Select(item => new { label = item.MarketHashName, value = item.MarketHashName, image = item.ImageUrl })
                .Take(5)
                .ToList();

            if (!suggestions.Any())
            {
                suggestions = itemList
                    .Where(item => item.MarketHashName.Contains(lowercasePrefix, StringComparison.OrdinalIgnoreCase))
                    .Select(item => new { label = item.MarketHashName, value = item.MarketHashName, image = item.ImageUrl })
                    .Take(5)
                    .ToList();
            }

            return Json(suggestions);
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
