namespace SteamGraphsWebApp.PythonServices
{
    using Python.Runtime;
    using System;
    using System.Runtime.InteropServices;

    public class PythonService
    {
        private static bool isInitialized = false;
        private static PyObject? _script = null;

        public void InitializePythonEngine()
        {
            if (!isInitialized)
            {
                // Runtime.PythonDLL = @".\PythonServices\python311.dll";
                Runtime.PythonDLL = @"C:\Users\Nukul\anaconda3\python311.dll";
                PythonEngine.Initialize();
                isInitialized = true;
            }
        }

        public string? RunScript()
        {
            InitializePythonEngine();
            try
            {
                using (Py.GIL())
                {
                    try
                    {

                        if (_script == null)
                        {
                            // make script PyObject
                            dynamic sys = Py.Import("sys");
                            sys.path.append(Path.Combine(@"C:\Users\Nukul\Desktop\Code\game_price_prediction\unused_code\python\webappscript.py"));

                            // Import python script
                            _script = Py.Import("webappscript");
                        }

                        // Call the specific function in the Python script with parameters
                        // dynamic result = script.__getattr__("supdog").Invoke();
                        var result = _script.InvokeMethod("supdog");
                        return result.ToString();
                    }
                    catch(Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                        return null;
                    }
                    
                }

            }
            catch (PythonException ex)
            {
                // Handle Python exceptions (e.g., script not found, runtime errors in Python)
                Console.WriteLine($"Python error: {ex.Message}");
                return null;
            }
            catch (Exception ex)
            {
                // Handle general .NET exceptions
                Console.WriteLine($"General error: {ex.Message}");
                return null;
            }
        }

        //public (dynamic current_item, dynamic non_aggregated_item) RunScript(string scriptName, string functionName, params object[] args)
        //{
        //    try
        //    {
        //        InitializePythonEngine();
        //        using (Py.GIL()) // Ensure the Python global interpreter lock is acquired
        //        {
        //            dynamic sys = Py.Import("sys");
        //            sys.path.append(@"C:/Users/Nukul/Desktop/Code/game_price_prediction/python_scripts");

        //            // Import python script
        //            dynamic script = Py.Import(scriptName);
        //            // Call the specific function in the Python script with parameters
        //            dynamic result = script.__getattr__(functionName).Invoke(args);

        //            return (result[0], result[1]);
        //        }
        //    }
        //    catch (PythonException ex)
        //    {
        //        // Handle Python exceptions (e.g., script not found, runtime errors in Python)
        //        Console.WriteLine($"Python error: {ex.Message}");
        //        return (null, null);
        //    }
        //    catch (Exception ex)
        //    {
        //        // Handle general .NET exceptions
        //        Console.WriteLine($"General error: {ex.Message}");
        //        return (null, null);
        //    }
        //}


        public void ShutdownPythonEngine()
        {
            if (isInitialized)
            {
                PythonEngine.Shutdown();
                isInitialized = false;
            }
        }
    }
}
