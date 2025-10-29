// ui/viewmodels/main_viewmodel.cs
using NumericalMethodsUI.Models;
using NumericalMethodsUI.Services;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Input;

namespace NumericalMethodsUI.ViewModels
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private readonly INumericalService _numericalService;
        private SolutionResult _currentResult;
        private bool _isCalculating;
        private string _statusMessage;

        public MainViewModel()
        {
            _numericalService = new NumericalService();
            CalculateCommand = new RelayCommand(async _ => await CalculateAsync(), _ => !IsCalculating);
            AvailableProblems = new ObservableCollection<string>(_numericalService.GetAvailableProblems());
            SelectedProblem = AvailableProblems.FirstOrDefault();
            Nodes = 21;
        }

        public ObservableCollection<string> AvailableProblems { get; }
        public ObservableCollection<DataPoint> ChartData { get; } = new ObservableCollection<DataPoint>();
        public ObservableCollection<DataPoint> ErrorData { get; } = new ObservableCollection<DataPoint>();

        public ICommand CalculateCommand { get; }

        public string SelectedProblem
        {
            get => _selectedProblem;
            set
            {
                _selectedProblem = value;
                OnPropertyChanged(nameof(SelectedProblem));
            }
        }
        private string _selectedProblem;

        public int Nodes
        {
            get => _nodes;
            set
            {
                _nodes = value;
                OnPropertyChanged(nameof(Nodes));
            }
        }
        private int _nodes;

        public bool IsCalculating
        {
            get => _isCalculating;
            set
            {
                _isCalculating = value;
                OnPropertyChanged(nameof(IsCalculating));
                ((RelayCommand)CalculateCommand).RaiseCanExecuteChanged();
            }
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set
            {
                _statusMessage = value;
                OnPropertyChanged(nameof(StatusMessage));
            }
        }

        public SolutionResult CurrentResult
        {
            get => _currentResult;
            set
            {
                _currentResult = value;
                OnPropertyChanged(nameof(CurrentResult));
                UpdateChartData();
            }
        }

        public double MaxError => CurrentResult?.MaxError ?? 0;
        public double RmsError => CurrentResult?.RmsError ?? 0;

        private async Task CalculateAsync()
        {
            IsCalculating = true;
            StatusMessage = "Calculating...";

            try
            {
                SolutionResult result;
                if (SelectedProblem == "main")
                {
                    result = await _numericalService.SolveMainProblemAsync(Nodes);
                }
                else if (SelectedProblem == "test")
                {
                    result = await _numericalService.SolveTestProblemAsync(Nodes);
                }
                else
                {
                    throw new InvalidOperationException("Unknown problem type");
                }

                CurrentResult = result;
                StatusMessage = $"Calculation completed. Max error: {MaxError:E4}, RMS error: {RmsError:E4}";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error: {ex.Message}";
            }
            finally
            {
                IsCalculating = false;
            }
        }

        private void UpdateChartData()
        {
            ChartData.Clear();
            ErrorData.Clear();

            if (CurrentResult?.NumericalSolution != null)
            {
                foreach (var point in CurrentResult.NumericalSolution)
                {
                    ChartData.Add(point);
                }

                if (CurrentResult.Errors != null)
                {
                    foreach (var error in CurrentResult.Errors)
                    {
                        ErrorData.Add(error);
                    }
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class RelayCommand : ICommand
    {
        private readonly Action<object> _execute;
        private readonly Func<object, bool> _canExecute;

        public RelayCommand(Action<object> execute, Func<object, bool> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public bool CanExecute(object parameter) => _canExecute?.Invoke(parameter) ?? true;
        public void Execute(object parameter) => _execute(parameter);

        public event EventHandler CanExecuteChanged;
        public void RaiseCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
    }
}