#!/usr/bin/env python3
import sys
import os
import logging

sys.path.append(os.path.dirname(__file__))

from ui.interface import SolverInterface
import tkinter as tk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    root = tk.Tk()
    interface = SolverInterface(root)
    logger.info("Starting Runge-Kutta Suite application")
    root.mainloop()

if __name__ == "__main__":
    main()