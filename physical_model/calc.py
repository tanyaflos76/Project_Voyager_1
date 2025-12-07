import numpy as np


def current_a(m, T, F_d, g):  # Из уравнения движения
    return (T - F_d - m * g) / m


def impuls_p(v_is, g):  # Удельный импульс
    return v_is / g


def thrust_force(v_is, dm, dt):  # Тяга двигателей
    return v_is * dm / dt


def drag_force(Cf, S, ro, v):  # Аэродинамическое сопротивление
    return Cf * S * (ro * v ** 2 / 2)


def current_g_h(h, r0=6378137, g0=9.80665):  # Изменение g(h)
    return g0 / (r0 / (r0 + h)) ** 2


def thrust_at_height(fuel_cons, v_is, s, p_exit, p_atm):  # Изменение T(h)
    return fuel_cons * v_is + s * (p_exit - p_atm)


def total_force(F_thrust, F_drag, m, g):
    return F_thrust - F_drag - m * g


def first_cosmic_velocity(g, R):  # Первая космическая скорость
    return np.sqrt(g * R)


def second_cosmic_velocity(V1):  # Вторая космическая скорость
    return np.sqrt(2) * V1


def hohmann_transfer_velocity(v1, v2):  # Гомановская траектория
    return np.sqrt((v1 ** 2 + v2 ** 2) / 2)


def hohmann_impulses(m, v1, v2):  # Импульсы на начало и конец манёвра
    v = hohmann_transfer_velocity(v1, v2)
    p1 = m * v1 * (v1 / v - 1)
    p2 = m * v2 * (1 - v2 / v)
    return p1, p2


def tsiolkovsky_many(I, dry_mass, m_stages):  # Уравнение Циолковского для многоступенчатой ракеты
    v = 0
    n = len(I)
    for i in range(n):
        sum1 = sum(m_stages[i:])
        sum2 = sum(m_stages[i + 1:])
        v += I[i] * np.log((dry_mass + sum1) /
                           (dry_mass + m_stages[i] + sum2))
    return v
