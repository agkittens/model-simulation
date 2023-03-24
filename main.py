from math import sin, pi, floor
import numpy as np
from matplotlib.figure import Figure


TESTRUN = True
RUNS = 20

# general parameters for the simulation
SIMULATION_TIME = 10.0
STEP = 0.01
SIGNAL_PERIOD = 2.5
SIGNAL_MAGNITUDE = 2
GAINS = np.linspace(0.0, 100, num = 30000)



class Model:
    def __init__(self):
        # init with standard simulation parameters
        self.h = STEP
        self.T = SIMULATION_TIME
        self.L = SIGNAL_PERIOD
        self.M = SIGNAL_MAGNITUDE
        self.gains = GAINS

        self.params = {'a': -2, 'b': 3, 'k': 4, 'A': 2}
        self.coeffs = []
        self.calculate_coeffs()

        self.input_signal = []
        self.output_signal = []
        self.generate_square_input()


        self.A = np.array([[0, 1], [0, 0]])
        self.B = [0, 1]
        self.C = [0, 0]
        self.xi = [0, 0]
        self.xi_1 = [0, 0]

        #H(s) * G(s) = (k*A)/(s2 + (a+b)s +ab)
        self.zeros_coeffs = np.array(self.params['k'] * self.params['A'])
        self.poles_coeffs = np.array([1, self.params['a'] + self.params['b'], self.params['a']*self.params['b']])

        self.zeros = []
        self.poles = []
        self.roots = []

        self.fig = Figure(figsize=(6, 6), edgecolor= "#c258f8", linewidth=8)
        self.plot = self.fig.add_subplot(111)


    # calculates coefficients of the denominator and saves them in the model
    def calculate_coeffs(self):
        calc_coeffs = [
            1,
            self.params['a'] + self.params['b'],
            self.params['a'] * self.params['b'] + self.params['k'] * self.params['A']
        ]

        self.coeffs = calc_coeffs

    # checks stability of the model / 1 if stable 0 if unstable
    # due to the simplicity of the model only needs to check a_i > 0
    def check_stability(self):
        for coeff in self.coeffs:
            if coeff < 0:
                return 0

        return 1

    # creates a sine wave vector for the input signal
    def generate_sin_input(self):
        self.input_signal = []
        w = 2 * pi * self.L / self.T

        for i in range(round(self.T / self.h)):
            self.input_signal.append(self.M * sin(w * i * self.h))

    # creates a square wave vector for the input signal
    def generate_square_input(self):
        self.input_signal = [0]
        w = self.L / self.h

        for i in range(round(self.T / self.h) - 1):
            if floor(i / w) % 2 == 0:
                self.input_signal.append(self.M)
            else:
                self.input_signal.append(-self.M)

    # creates a step vector for the input signal
    def generate_step_input(self):
        self.input_signal = [0]
        for i in range(round(self.T / self.h) - 1):
            self.input_signal.append(self.M)

    # creates the matrices for the state model base on current parameters
    def create_matrices(self):
        self.A = [[0, 1], [-self.coeffs[2], -self.coeffs[1]]]
        self.B = [0, 1]
        self.C = [self.params['k']*self.params['A'], 0]

    # calculates the system response using Euler's method
    def calculate_response(self):
        self.output_signal = []
        self.xi_1 = [0, 0]
        for i in range(round(self.T/self.h)):
            Ax = np.dot(self.A, self.xi_1)
            Bu = np.dot(self.B, self.input_signal[i])
            Cx = np.dot(self.C, self.xi_1)
            self.xi = (Ax + Bu)*self.h + self.xi_1
            self.xi_1 = self.xi
            self.output_signal.append(Cx)

    def draw_response(self):
        self.plot.cla()
        self.create_matrices()
        self.calculate_response()
        self.plot.set_title("Output signal")
        self.plot.set_xlabel("Time")
        self.plot.plot(range(1000), self.output_signal)
        self.plot.plot(range(1000), self.input_signal)


    def find_roots(self):
        #transfer function fraction elements
        num = np.poly1d(self.zeros_coeffs)
        denum = np.poly1d(self.poles_coeffs)

        self.zeros = np.roots(num)
        self.poles = np.roots(denum)

        #range of gains with num density

        for gain in self.gains:
            # = D(s) + K * N(s)
            ch_eq = denum + gain * num
            ch_roots = np.roots(ch_eq)
            self.roots.append(ch_roots)

        #all the neccessary points based on characteristic equation
        self.roots = np.vstack(self.roots)

    def draw_root_locus(self):
        if self.check_stability() and self.params['k']>0:
            self.find_roots()

            #sorting to parts of complex argument
            real_val = np.real(self.roots)
            imaginary_val = np.imag(self.roots)

            #creates a plot figure
            self.plot.cla()
            self.plot.set_title("Root locus")
            self.plot.set_xlabel("Re")
            self.plot.set_ylabel("Im")
            self.plot.grid(True, which = "both")

            #drawing points
            self.plot.scatter(np.real(self.poles), np.imag(self.poles), marker='x', c = "black")
            self.plot.scatter(np.real(self.zeros), np.imag(self.zeros), marker='o', c = "orange")

            #drawing lines
            lines_colors = real_val.shape[1]
            colors = ["blue", "red", "green"]

            for r_ax, i_ax, c_value in zip(real_val.T, imaginary_val.T, range(lines_colors)):
                self.plot.plot(r_ax, i_ax, color=colors[c_value])
