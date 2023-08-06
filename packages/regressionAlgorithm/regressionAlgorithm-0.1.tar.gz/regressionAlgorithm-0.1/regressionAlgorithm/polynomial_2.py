import numpy as np

class PolynomialOrderTwo:

    def __init__(self):
        self.x = []
        self.y = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.square_r = 0
        self.line = []
    
    def calculate(self):
        """
        general numerical operation
        """        
        x = self.x
        y = self.y

        # general value
        n = len(x)
        sumx = np.sum(x)
        sumy = np.sum(y)
        xy = np.sum(x * y)
        xsquare = np.sum(np.square(x))
        xsquarey = np.sum(np.square(x) * y)
        x_pangkat_tiga = np.sum(x**3)
        x_pangkat_empat = np.sum(x**4)

        # metrics
        m1 = np.matrix([
            [n, sumx, xsquare],
            [sumx, xsquare, x_pangkat_tiga],
            [xsquare, x_pangkat_tiga, x_pangkat_empat]
        ])

        # persamaan linear cramer oleh gabriel cramer

        d = np.linalg.det(m1)
        d1 = np.linalg.det(np.matrix([
            [sumy, sumx, xsquare],
            [xy, xsquare, x_pangkat_tiga],
            [xsquarey, x_pangkat_tiga, x_pangkat_empat]
        ]))
        d2 = np.linalg.det(np.matrix([
            [n, sumy, xsquare],
            [sumx,xy, x_pangkat_tiga],
            [xsquare,xsquarey,  x_pangkat_empat]
        ]))
        d3 = np.linalg.det(np.matrix([
            [n, sumx, sumy],
            [sumx, xsquare, xy],
            [xsquare, x_pangkat_tiga,xsquarey]
        ]))

        # mencari nilai koefisien
        a = d1 / d
        b = d2 / d
        c = d3 / d

        self.a = a
        self.b = b
        self.c = c
        
        # r square (koefisien determinasi)
        y_hat_table = a + b * x + c * np.square(x)

        # menghitung selisih square(y - y hat)
        selisih = np.square(y - y_hat_table)
        sumselisih = np.sum(selisih)

        # menghitung y bar square(y - ybar)
        ybar = np.square(y - (sumy / n))
        sumybar = np.sum(ybar)     

        # menghitung koefisien determinasi square(r)

        rsquare = 1 - (sumselisih / sumybar)
        self.square_r = rsquare


    def fit(self, x, y):
        """
        fit value x and y
        """
        self.x = np.array(x)
        self.y = np.array(y)

    def predict(self,x):
        """
        predict x value
        """
        val = self.a + (self.b * x) + (self.c * x**2)
        return val

    def plot(self):
        """
        data for plotting
        """
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c
        }

    def r_square(self):
        """
        return r square value
        """
        return self.square_r

    def draw_line(self):
        """
        draw the line
        """
        line = []
        for i in self.x:
            line.append(self.a + (self.b * i) + (self.c * i**2))
        return line

    def start(self):
        """
        start the operation
        """
        self.calculate()