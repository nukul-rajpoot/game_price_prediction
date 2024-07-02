using Microsoft.AspNetCore.Mvc;
using SteamGraphsWebApp.Models;
using System.Diagnostics;
using SteamGraphsWebApp.PythonServices;

namespace SteamGraphsWebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly PythonService _pythonService;
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger, PythonService pythonService)
        {
            _pythonService = pythonService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View(new SteamItemViewModel());
        }

        // POST: Home
        [HttpPost]
        public IActionResult Index(SteamItemViewModel model)
        {
            string hello = _pythonService.RunScript();
            try
            {
                ViewBag.hello = hello;

            }
            catch (Exception ex) {
                Console.WriteLine(ex.Message);
            }
            //(dynamic current_item, dynamic non_aggregated_item) = pythonService.RunScript("webappscript", "fetch_df_to_webapp", "Glove Case");
            //ViewData["CurrentItem"] = current_item;
            //ViewData["NonAggregatedItem"] = non_aggregated_item;
            // Just pass the same model back to the view
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
