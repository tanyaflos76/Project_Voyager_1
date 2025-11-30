import numpy as np


def current_a(m, T, F_d, g):
    return (T - F_d - m * g) / m


def thrust_force(v_is, dm, dt):
    return v_is * dm / dt


def drag_force(Cf, S, rho, v):  # Аэродинамическое сопротивление
    return Cf * S * (rho * v ** 2 / 2)


def total_force(F_thrust, F_drag, m, g):
    return F_thrust - F_drag - m * g


def first_cosmic_velocity(g, R):
    return np.sqrt(g * R)


def second_cosmic_velocity(V1):
    return np.sqrt(2) * V1


def hohmann_transfer_velocity(v1, v2):  # Гомановская траектория
    return np.sqrt((v1 ** 2 + v2 ** 2) / 2)


def hohmann_impulses(m, v1, v2):  # Импульсы на начало и конец манёвра
    v_mid = hohmann_transfer_velocity(v1, v2)
    p1 = m * v1 * (v1 / v_mid - 1)
    p2 = m * v2 * (1 - v2 / v_mid)
    return p1, p2


def tsiolkovsky_many(I, dry_mass, m_stages):  # Для многоступенчатой ракеты
    v = 0
    n = len(I)
    for i in range(n):
        sum1 = sum(m_stages[i:])
        sum2 = sum(m_stages[i + 1:])
        v += I[i] * np.log((dry_mass + sum1) /
                           (dry_mass + m_stages[i] + sum2))
    return v
