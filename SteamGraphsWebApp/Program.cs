using SteamGraphsWebApp.GraphCalls;
using SteamGraphsWebApp.PythonServices;
using Microsoft.Extensions.Azure;

var builder = WebApplication.CreateBuilder(args);

// Add python service
builder.Services.AddScoped<PythonService>();
builder.Services.AddScoped<NameService>();
builder.Services.AddScoped<MakeGraphs>();
builder.Services.AddScoped<ApiCalls>();
builder.Services.AddHttpClient<ApiCalls>();

// Add services to the container.
builder.Services.AddControllersWithViews();
builder.Services.AddAzureClients(clientBuilder =>
{
    clientBuilder.AddBlobServiceClient(builder.Configuration["steamgraphsconnection:blob"]!, preferMsi: true);
    clientBuilder.AddQueueServiceClient(builder.Configuration["steamgraphsconnection:queue"]!, preferMsi: true);
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
