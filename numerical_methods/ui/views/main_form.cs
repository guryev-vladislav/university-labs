// ui/views/main_form.cs
using NumericalMethodsUI.ViewModels;
using System;
using System.Drawing;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace NumericalMethodsUI.Views
{
    public partial class MainForm : Form
    {
        private readonly MainViewModel _viewModel;
        private Chart chartSolution;
        private Chart chartErrors;
        private DataGridView dataGrid;
        private ComboBox comboProblems;
        private NumericUpDown numNodes;
        private Button btnCalculate;
        private Label lblStatus;
        private Label lblMaxError;
        private Label lblRmsError;

        public MainForm()
        {
            _viewModel = new MainViewModel();
            _viewModel.PropertyChanged += ViewModel_PropertyChanged;
            InitializeComponent();
            InitializeDataBinding();
        }

        private void InitializeComponent()
        {
            // Основные настройки формы
            this.Text = "Numerical Methods Visualizer";
            this.Size = new Size(1200, 800);
            this.StartPosition = FormStartPosition.CenterScreen;

            // Панель управления
            var controlPanel = new Panel
            {
                Dock = DockStyle.Top,
                Height = 100,
                BackColor = Color.LightGray,
                Padding = new Padding(10)
            };

            // Элементы управления
            var lblProblem = new Label { Text = "Problem:", Location = new Point(10, 15), AutoSize = true };
            comboProblems = new ComboBox { Location = new Point(70, 12), Width = 100, DropDownStyle = ComboBoxStyle.DropDownList };

            var lblNodes = new Label { Text = "Nodes:", Location = new Point(180, 15), AutoSize = true };
            numNodes = new NumericUpDown { Location = new Point(225, 12), Width = 60, Minimum = 5, Maximum = 1000, Value = 21 };

            btnCalculate = new Button { Text = "Calculate", Location = new Point(300, 10), Size = new Size(80, 30), BackColor = Color.LightBlue };

            lblStatus = new Label { Location = new Point(400, 15), AutoSize = true, Text = "Ready" };
            lblMaxError = new Label { Location = new Point(10, 45), AutoSize = true };
            lblRmsError = new Label { Location = new Point(10, 65), AutoSize = true };

            // Добавляем элементы на панель
            controlPanel.Controls.AddRange(new Control[] {
                lblProblem, comboProblems, lblNodes, numNodes, btnCalculate,
                lblStatus, lblMaxError, lblRmsError
            });

            // Создаем графики
            var splitContainer = new SplitContainer
            {
                Dock = DockStyle.Fill,
                Orientation = Orientation.Horizontal,
                SplitterDistance = 400
            };

            chartSolution = CreateChart("Numerical Solution", "x", "y");
            chartErrors = CreateChart("Errors", "x", "error");

            splitContainer.Panel1.Controls.Add(chartSolution);
            splitContainer.Panel2.Controls.Add(chartErrors);

            // Таблица данных
            dataGrid = new DataGridView
            {
                Dock = DockStyle.Right,
                Width = 300,
                ReadOnly = true,
                AllowUserToAddRows = false,
                AllowUserToDeleteRows = false,
                AutoGenerateColumns = false
            };

            // Настраиваем колонки таблицы
            dataGrid.Columns.Add(new DataGridViewTextBoxColumn { Name = "X", DataPropertyName = "X", HeaderText = "x", Width = 80 });
            dataGrid.Columns.Add(new DataGridViewTextBoxColumn { Name = "Y", DataPropertyName = "Y", HeaderText = "y", Width = 80 });

            // Добавляем элементы на форму
            this.Controls.AddRange(new Control[] { splitContainer, dataGrid, controlPanel });

            // События
            btnCalculate.Click += (s, e) => _viewModel.CalculateCommand.Execute(null);
        }

        private Chart CreateChart(string title, string xTitle, string yTitle)
        {
            var chart = new Chart
            {
                Dock = DockStyle.Fill
            };

            var chartArea = new ChartArea();
            chartArea.AxisX.Title = xTitle;
            chartArea.AxisY.Title = yTitle;
            chartArea.AxisX.MajorGrid.Enabled = true;
            chartArea.AxisY.MajorGrid.Enabled = true;

            chart.ChartAreas.Add(chartArea);

            var series = new Series
            {
                ChartType = SeriesChartType.Line,
                Color = Color.Blue,
                BorderWidth = 2
            };

            chart.Series.Add(series);

            return chart;
        }

        private void InitializeDataBinding()
        {
            // Привязка данных
            comboProblems.DataSource = _viewModel.AvailableProblems;
            comboProblems.DataBindings.Add("SelectedItem", _viewModel, "SelectedProblem");

            numNodes.DataBindings.Add("Value", _viewModel, "Nodes");

            btnCalculate.DataBindings.Add("Enabled", _viewModel, "IsCalculating", true, DataSourceUpdateMode.OnPropertyChanged, false);

            lblStatus.DataBindings.Add("Text", _viewModel, "StatusMessage");
            lblMaxError.DataBindings.Add("Text", _viewModel, "MaxError", true, DataSourceUpdateMode.OnPropertyChanged, "Max error: {0:E4}");
            lblRmsError.DataBindings.Add("Text", _viewModel, "RmsError", true, DataSourceUpdateMode.OnPropertyChanged, "RMS error: {0:E4}");

            // Привязка данных графиков и таблицы
            var chartSolutionSeries = chartSolution.Series[0];
            chartSolutionSeries.Points.DataBind(_viewModel.ChartData, "X", "Y", "");

            var chartErrorsSeries = chartErrors.Series[0];
            chartErrorsSeries.Points.DataBind(_viewModel.ErrorData, "X", "Y", "");

            dataGrid.DataSource = _viewModel.ChartData;
        }

        private void ViewModel_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            if (e.PropertyName == nameof(_viewModel.IsCalculating))
            {
                btnCalculate.Text = _viewModel.IsCalculating ? "Calculating..." : "Calculate";
            }
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);
            _viewModel.CalculateCommand.Execute(null);
        }
    }
}