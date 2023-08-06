import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class charts():
    def __init__(self, chart_type):
        self.chart_type = chart_type

    def line(self, array):
        if self.chart_type != "line":
            raise TypeError("Chart type must be a Line")
        if type(array).__module__ != np.__name__:
            raise ValueError("Array must be a type of Numpy Array")

        plt.plot(array)
        plt.show()
