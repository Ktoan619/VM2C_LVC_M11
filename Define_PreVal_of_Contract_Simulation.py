import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Constants
L = 1000
r = 0.029
TL = 120
num_bullets_per_year = 5
num_years = 10
max_bullets_per_month = 1
Mi_values = [i for i in range(50, 251, 50)]
Di_values = [1, 3, 6, 9, 12]
MinM = 50
MaxM = 250
MinD = 1
MaxD = 12

# Monthly distribution probabilities
monthly_probabilities = np.array([2.44, 2.44, 2.44, 13.754, 13.754, 13.755, 13.999, 13.999, 13.999, 3.14, 3.14, 3.14]) / 100
# print(sum(monthly_probabilities))
# Monte Carlo parameters
num_simulations = 100

# function to calculate the present value of a bullet
def calculate_pv(Ai, Ti, Di, r):
    return (Ai + Ai * r*(Di/12)) / ((1 + r) ** (Ti/12))
    # return Ai

# Function to generate a list of Ti values based on monthly distribution
def generate_bullets():
    T = []
    for year in range(1, num_years+1):
        cnt = [0] * 13
        num_bullets_per_year = np.random.randint(5, 7)
        for bullet_in_year in range(num_bullets_per_year):
            while True:
                month = np.random.choice(range(1, 13), p=monthly_probabilities)
                if year == 10 and month >= 10 and month <= 12 : continue
                if cnt[month] < max_bullets_per_month:
                    cnt[month] += 1
                    T.append((year - 1) * 12 + month)
                    break
    T.sort()
    return T

# Dynamic programming function
def dynamic_programming(Ti_list):
    num_bullets = len(Ti_list)
    print(Ti_list)

    cnt = np.zeros((num_bullets + 1, TL + 1, L + 1), dtype='float64')
    val = np.zeros((num_bullets + 1, TL + 1, L + 1), dtype='float64')

    for i in range(1, num_bullets + 1) :
        for Mi in Mi_values:
            for Di in Di_values:
                if Ti_list[i - 1] + Di > TL:
                    break
                for l in range(0, L - Mi + 1, 50):
                    c = cnt[i - 1][Ti_list[i - 1]][l]
                    if i == 1 and l == 0 :
                        c = 1
                    v = val[i - 1][Ti_list[i - 1]][l]
                    for nextt in range(Ti_list[i - 1], TL + 1):
                        if Ti_list[i - 1] + Di > nextt:
                            cnt[i][nextt][l + Mi] += c
                            val[i][nextt][l + Mi] += (v + c * calculate_pv(Mi, Di, Ti_list[i-1], r))
                        else:
                            cnt[i][nextt][l] += c
                            val[i][nextt][l] += (v + c * calculate_pv(Mi, Di, Ti_list[i-1], r))

    SV = 0
    Scnt = 0
    for l in range(L + 1):
        SV += val[num_bullets][Ti_list[-1]][l]
        Scnt += cnt[num_bullets][Ti_list[-1]][l]
    print(SV, Scnt)
    return SV / Scnt if Scnt != 0 else 0

# Monte Carlo simulation
def monte_carlo_simulation():
    e_pv_list = []

    for _ in range(num_simulations):
        Ti_list = generate_bullets()
        e_pv = dynamic_programming(Ti_list)
        e_pv_list.append(e_pv)

    return e_pv_list


# Run the Monte Carlo simulation
e_pv_results = monte_carlo_simulation()

# Get average E(PV)
print(sum(e_pv_results)/len(e_pv_results))

# Plotting the histogram
plt.hist(e_pv_results, bins=50, density=True, alpha=0.6, color='g')
plt.xlabel('Expected Present Value (E(PV))')
plt.ylabel('Frequency')
plt.title('Histogram of E(PV) from Monte Carlo Simulation')
plt.show()
