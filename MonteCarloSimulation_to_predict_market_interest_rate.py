import numpy as np
import matplotlib.pyplot as plt

# Dữ liệu lãi suất thị trường 10 năm gần nhất
years = np.array([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
interest_rates = np.array([3.50, 2.70, 2.70, 2.70, 2.90, 2.70, 2.50, 3.00, 3.25, 3.50, 3.00]) / 100

# Tính toán các tỷ lệ biến động lãi suất

changes = np.diff(interest_rates)
mean_change = np.mean(changes)
std_change = np.std(changes)

# Tính xác suất dựa trên phân phối chuẩn của các thay đổi
p_up = np.sum(changes > 0) / len(changes)
p_down = np.sum(changes < 0) / len(changes)
p_stay = np.sum(changes == 0) / len(changes)

print(f"Xác suất lãi suất tăng (p_up): {p_up}")
print(f"Xác suất lãi suất giảm (p_down): {p_down}")
print(f"Xác suất lãi suất giữ nguyên (p_stay): {p_stay}")

# Số lần mô phỏng (số kịch bản lãi suất)

N = 10000
# Thời gian mô phỏng (số năm)

T = 11

# Khởi tạo ma trận lưu trữ lãi suất cho N kịch bản trong T năm
interest_rates_simulation = np.zeros((N, T))
interest_rates_simulation[:, 0] = interest_rates[-1]

# Mô phỏng sự biến động của lãi suất
for i in range(1, T):
    random_numbers = np.random.rand(N)
    change = np.random.normal(loc=mean_change, scale=std_change, size=N)
    interest_rates_simulation[:, i] = interest_rates_simulation[:, i-1] + change

# Tính giá trị kỳ vọng của lãi suất qua các năm
expected_interest_rates = np.mean(interest_rates_simulation, axis=0)

# In kết quả mô phỏng
print("Giá trị kỳ vọng của lãi suất qua các năm:")
for year in range(T):
    print(f"Năm {year + 1}: {expected_interest_rates[year] * 100:.2f}%")

# Vẽ đồ thị mô phỏng
plt.figure(figsize=(10, 6))
for i in range(100):  # Vẽ 100 kịch bản đầu tiên để đồ thị rõ ràng
    plt.plot(range(T), interest_rates_simulation[i, :], color='grey', alpha=0.1)
plt.plot(range(T), expected_interest_rates, color='red', linewidth=2, label='Giá trị kỳ vọng')
plt.xlabel('Năm')
plt.ylabel('Lãi suất')
plt.title('Mô phỏng biến động lãi suất bằng phương pháp Monte Carlo')
plt.legend()
plt.show()
