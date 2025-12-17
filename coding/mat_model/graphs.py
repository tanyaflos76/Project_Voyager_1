import matplotlib.pyplot as plt
import numpy as np

from objects import Voyager
from calc import simulation

voyager = Voyager(
    total_mass=251074,
    step1=[182470, 144000, 3 * 1379032, 3 * 285, 112],
    step2=[33370, 24000, 1379032, 285, 205], step3=[35444, 24000, 64286, 444, 470],

    s_nozzle=7.3, s_surf=14.6, cf=0.2,
)

total_time = 250
delta_t = 0.06  # наш шаг времени

f1 = open("table_h.txt")
f2 = open("table_v.txt")
f3 = open("table_a_smoothed.txt")
s1 = list(map(float, f1.read().split()))
s2 = list(map(float, f2.read().split()))
s3 = list(map(float, f3.read().split()))
f1.close()
f2.close()
f3.close()

# Создаем массив времени
t = np.arange(0, total_time + delta_t, delta_t)

# Вычисляем значения через нашу функцию
times, speeds, heights, a_s = simulation(voyager, delta_t, total_time)
# Данные о полете из KSP
times_h_ksp = s1[0::2]
heights_ksp = s1[1::2]
times_v_ksp = s2[0::2]
speeds_ksp = s2[1::2]
times_a_ksp = s3[0::2]
a_ksp = s3[1::2]

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

plt.figure()
plt.plot(times, a_s, 'b-', linewidth=1, label='Мат. модель')
plt.plot(times_a_ksp, a_ksp, 'r--', linewidth=1, label='KSP')
plt.xlabel("Время, с")
plt.ylabel("Ускорение, м")
plt.title("Зависимость ускорение от времени")
plt.legend()
plt.show()
