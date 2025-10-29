// ui/services/inumerical_service.cs
using NumericalMethodsUI.Models;
using System.Threading.Tasks;

namespace NumericalMethodsUI.Services
{
    public interface INumericalService
    {
        Task<SolutionResult> SolveMainProblemAsync(int nodes);
        Task<SolutionResult> SolveTestProblemAsync(int nodes);
        string[] GetAvailableProblems();
    }
}