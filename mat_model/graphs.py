import matplotlib.pyplot as plt
import numpy as np

from objects import Voyager
from calc import simulation

voyager = Voyager(
    total_mass=815000, step0=[2 * 226233, 2 * 192435, 4 * 5849411, 263, 2 * 115],
    step1=[116573, 111130, 2339760, 302, 147],
    step2=[29188, 26535, 4 * 4537140, 316, 205], step3=[16258, 13627, 131222, 444, 470],
    step4=[1123, 1040, 68000, 284, 42],
    s_nozzle=7.3, s_surf=14.6, cf=0.2,
)

total_time = 250
delta_t = 0.06  # наш шаг времени

f1 = open("table_h.txt")
f2 = open("table_v.txt")
s1 = list(map(float, f1.read().split()))
s2 = list(map(float, f2.read().split()))
f1.close()
f2.close()

# Создаем массив времени
t = np.arange(0, total_time + delta_t, delta_t)

# Вычисляем значения через нашу функцию
times, speeds, heights, a_s = simulation(voyager, delta_t, total_time)
# Данные о полете из KSP
times_h_ksp = s1[0::2]
heights_ksp = s1[1::2]
times_v_ksp = s2[0::2]
speeds_ksp = s2[1::2]

plt.figure()
plt.plot(times, speeds, 'b-', linewidth=1, label='Мат. модель')
plt.plot(times_v_ksp, speeds_ksp, 'r--', linewidth=1, label='KSP')
plt.xlabel("Время, с")
plt.ylabel("Cкорость, м/с")
plt.title("Зависимость скорости от времени")
plt.legend()
plt.show()

plt.figure()
plt.plot(times, heights, 'b-', linewidth=1, label='Мат. модель')
plt.plot(times_v_ksp, heights_ksp, 'r--', linewidth=1, label='KSP')
plt.xlabel("Время, с")
plt.ylabel("Высота, м")
plt.title("Зависимость высоты от времени")
plt.legend()
plt.show()
