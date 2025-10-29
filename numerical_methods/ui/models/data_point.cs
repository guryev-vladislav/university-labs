// ui/models/data_point.cs
using System;

namespace NumericalMethodsUI.Models
{
    public class DataPoint
    {
        public double X { get; set; }
        public double Y { get; set; }

        public DataPoint(double x, double y)
        {
            X = x;
            Y = y;
        }
    }

    public class SolutionResult
    {
        public DataPoint[] NumericalSolution { get; set; }
        public DataPoint[] ReferenceSolution { get; set; }
        public DataPoint[] Errors { get; set; }
        public string ProblemType { get; set; }
        public int Nodes { get; set; }
        public double MaxError { get; set; }
        public double RmsError { get; set; }
    }

    public enum ProblemType
    {
        Main,
        Test
    }
}