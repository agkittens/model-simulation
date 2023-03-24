# Model-Simulation

## Table of Contents
* [General Info](#general-info)
* [Examples and Usage](#examples-and-usage)
* [Requirements](#requirements)
* [Conclusion](#conclusion)


## General Info
This repository contains a simulation of the mathematical model shown below. It allows for testing out different combinations of parameters, input signals and displaying the corresponding output signal and root locus.

![model](https://github.com/StainedMentor/Model-Simulation/blob/main/model.png?raw=true)



### Input vectors
The 3 input signals (sine, square wave, step) are created by calculating the value of the chosen function at every simulation step and saving them in the input vector. The input vector is then used for further calculations using a numerical approach.

### Stability
To check the stability of the system we use the Hurwitz criterion which for this model simplifies to checking if the coefficients of the denominator are greater than 0. The reason for this is that the determinant of the Hurwitz matrix consists of a single multiplication of coefficients.

### Output Signal
Generating the output signal first calculates the matrices defining the model. Then using Euler's method the program then calculates each step of the output signal. The matrix multiplication is done by using numpy's builtin functions.

### Root locus
The root locus is calculated by find the roots of the characteristic equation for every value K in the range given by the base simulation parameters. Every point is then plotted on a complex number graph.


## Examples and Usage
The simulations default paramters are shown below.
```
SIMULATION_TIME = 10.0
STEP = 0.01
SIGNAL_PERIOD = 2.5
SIGNAL_MAGNITUDE = 2
a = -2
b = 3
k = 4
A = 2
```


The base parameter input vectors and root locus are drawn using matplotlib as shown below.
![plot](https://github.com/StainedMentor/Model-Simulation/blob/main/plot.png?raw=true)
![plot](https://github.com/StainedMentor/Model-Simulation/blob/main/assets/root_locus.png?raw=true)


The simulation can can be started by running the app.py file.

## Requirements
The required packages for this project are listed in the requirements.txt file. To install them, simply run the following command:
```
$ pip install -r requirements.txt
```
## Conclusion
The simulation is correct in all aspects with some minor limitations like matplotlib scaling to always show full graph and not being correctly incorporated into tkinters windows. 


![plot](https://github.com/StainedMentor/Model-Simulation/blob/main/assets/Tresc_zadania.png?raw=true)


