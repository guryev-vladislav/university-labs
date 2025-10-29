// ui/services/numerical_service.cs
using NumericalMethodsUI.Models;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace NumericalMethodsUI.Services
{
    public class NumericalService : INumericalService
    {
        private readonly Bridge.NumericalBridge _bridge;

        public NumericalService()
        {
            _bridge = new Bridge.NumericalBridge();
        }

        public async Task<SolutionResult> SolveMainProblemAsync(int nodes)
        {
            return await Task.Run(() =>
            {
                try
                {
                    var result = _bridge.SolveMainProblem(nodes);
                    var x = result.Item1;
                    var v = result.Item2;
                    var x2 = result.Item3;
                    var v2 = result.Item4;
                    var diff = result.Item5;

                    var numericalSolution = x.Zip(v, (xVal, vVal) => new DataPoint(xVal, vVal)).ToArray();
                    var referenceSolution = x2.Zip(v2, (xVal, vVal) => new DataPoint(xVal, vVal)).ToArray();
                    var errors = x.Zip(diff, (xVal, errorVal) => new DataPoint(xVal, errorVal)).ToArray();

                    return new SolutionResult
                    {
                        NumericalSolution = numericalSolution,
                        ReferenceSolution = referenceSolution,
                        Errors = errors,
                        ProblemType = "Main",
                        Nodes = nodes,
                        MaxError = diff.Max(),
                        RmsError = Math.Sqrt(diff.Average(d => d * d))
                    };
                }
                catch (Exception ex)
                {
                    throw new InvalidOperationException($"Error solving main problem: {ex.Message}", ex);
                }
            });
        }

        public async Task<SolutionResult> SolveTestProblemAsync(int nodes)
        {
            return await Task.Run(() =>
            {
                try
                {
                    var result = _bridge.SolveTestProblem(nodes);
                    var x = result.Item1;
                    var v = result.Item2;
                    var u = result.Item3;
                    var diff = result.Item4;

                    var numericalSolution = x.Zip(v, (xVal, vVal) => new DataPoint(xVal, vVal)).ToArray();
                    var referenceSolution = x.Zip(u, (xVal, uVal) => new DataPoint(xVal, uVal)).ToArray();
                    var errors = x.Zip(diff, (xVal, errorVal) => new DataPoint(xVal, errorVal)).ToArray();

                    return new SolutionResult
                    {
                        NumericalSolution = numericalSolution,
                        ReferenceSolution = referenceSolution,
                        Errors = errors,
                        ProblemType = "Test",
                        Nodes = nodes,
                        MaxError = diff.Max(),
                        RmsError = Math.Sqrt(diff.Average(d => d * d))
                    };
                }
                catch (Exception ex)
                {
                    throw new InvalidOperationException($"Error solving test problem: {ex.Message}", ex);
                }
            });
        }

        public string[] GetAvailableProblems()
        {
            return _bridge.AvailableProblems;
        }
    }
}