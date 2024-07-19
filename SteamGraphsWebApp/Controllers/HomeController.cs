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
            SteamItemModel initialModel = new SteamItemModel();
            DataFrame? df = await steamMarketApiCall.FetchItemToDataFrame(initialModel);
            //Pass JSON data to the view
            ViewBag.jsonPriceHistoryDate = df["date"];
            ViewBag.jsonPriceHistoryPrice = df["price_usd"];

            return View();
        }


        // POST: Home
        [HttpPost]
        public async Task<IActionResult> Index(SteamItemModel model)
        {
            if (model.InputItemName != null)
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
