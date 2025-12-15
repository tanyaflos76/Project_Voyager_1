import matplotlib.pyplot as plt
import numpy as np

from objects import Voyager
from calc import simulation

voyager = Voyager(
    total_mass=815, step0=[226, 192.4, 596.5, 263, 91], step1=[116.5, 111.1, 238, 302, 91],
    step2=[29.2, 26.6, 46.3, 316, 205], step3=[16.2, 13.6, 13.3, 444, 470],
    step4=[],
    s_nozzle=7.3, s_surf=14.6, cf=0.2,
    # s=7.0,
    # cf=0.0,
    # v_is=0
)

total_time = 10
delta_t = 0.1  # наш шаг времени

# Создаем массив времени
t = np.arange(0, total_time + delta_t, delta_t)

# Вычисляем значения через нашу функцию
times, speeds, heights = simulation(t, delta_t)

plt.figure()
plt.plot(times / 86400, speeds)
plt.xlabel("дни")
plt.ylabel("скорость (м/с)")
plt.title("Скорость vs время")
plt.show()

plt.figure()
plt.plot(times / 86400, heights / 1e9)
plt.xlabel("дни")
plt.ylabel("расстояние от Земли (млрд м)")
plt.title("Расстояние от Земли vs время")
plt.show()
