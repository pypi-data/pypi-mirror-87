import numpy as np

class PolynomialOrderOne:

    def __init__(self):
        self.x = []
        self.y = []
        self.line = []
        self.a = 0
        self.b = 0
        self.r = 0
        self.squared_r = 0
    def fit(self, x, y):
        """
        Fit the data to x (independet) variable 
        and y variable (dependent)
        """
        self.x = np.array(x)
        self.y = np.array(y)

    def calculation(self):
        """
        calculate the data
        """
        x = self.x
        y = self.y
        n = len(x)
        sumx = np.sum(x)
        sumy = np.sum(y)
        sumxy = np.sum(x * y)
        xsqrt = np.sum(np.square(x))
        ysqrt = np.sum(np.square(y))

        # mean
        xbar = sumx / n
        ybar = sumy / n

        # sum of square
        ssxy = sumxy - (sumx * sumy / n)
        ssxx = xsqrt - (sumx**2 / n)
        ssyy = ysqrt - (sumy**2 / n)

        # define regresion function

        b = ssxy / ssxx
        a = ybar - (b * xbar)

        # define relation between x and y variable
        r_squared = b * (ssxy / ssyy)
        r = ssxy / np.sqrt(ssxx*ssyy)

        # draw the line

        line = []
        for data in x:
            line.append(a + (b * data))
        self.line = line
        # put it into global properties

        self.squared_r = r_squared
        self.r = r
        self.a = a
        self.b = b
        self.y = y

    def get_line(self):
        """
        get the line value
        """
        line = []
        for data in self.x:
            line.append(self.a + self.b * data)
        return line
    
    def r_squared(self):
        """
        return r squared value
        """
        return self.squared_r

    def r_value(self):
        """
        return r value
        """
        return self.r

    def plot(self):
        """
        get data for plotting
        """
        return {
            "x": self.x,
            "y": self.y,
            "a": self.a,
            "b": self.b
        }
    
    def predict(self, x):
        """
        predict with random value
        """
        return self.a + self.b * x

    def start(self):
        self.calculation()