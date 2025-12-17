import numpy as np


def v_is(imp, g):  # Удельный импульс
    return imp * g


def drag_force(cf, s, ro, v):  # Аэродинамическое сопротивление Fc
    return cf * s * (ro * v ** 2 / 2)


def current_g_h(h, r0=6378137, g0=9.80665):  # Изменение g(h)
    return g0 * ((r0 / (r0 + h)) ** 2)


def thrust_at_height(fuel_cons, v_is, s, p_exit, p_atm):  # Изменение T(h)
    return fuel_cons * v_is + s * (p_exit - p_atm)


def total_force(f_thrust, f_drag, m, g):
    return f_thrust - f_drag - m * g


def first_cosmic_velocity(g, r):  # Первая космическая скорость
    return np.sqrt(g * r)


def second_cosmic_velocity(v1):  # Вторая космическая скорость
    return np.sqrt(2) * v1


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


def distance(a, b):
    return np.linalg.norm(a - b)


def find_v(v0, aver_a, dt):
    return v0 + aver_a * dt


def find_h(h0, aver_v, aver_a, dt):
    return h0 + aver_v * dt + (aver_a * (dt ** 2)) / 2


def find_p_atm(h_meters):
    if h_meters <= 11000:
        return 101325 * np.exp(-h_meters / 8500)
    elif h_meters <= 25000:
        return 22632 * np.exp(-(h_meters - 11000) / 6340)
    elif h_meters <= 47000:
        return 2488 * np.exp(-(h_meters - 25000) / 8000)
    elif h_meters <= 86000:
        return 120 * np.exp(-(h_meters - 47000) / 10000)
    elif h_meters <= 150000:
        return 2.5 * np.exp(-(h_meters - 86000) / 20000)
    else:
        return 2.5e-6 * np.exp(-(h_meters - 150000) / 50000)


def find_ro(h_meters):
    if h_meters <= 11000:
        return 1.225 * np.exp(-h_meters / 8500)

    elif h_meters <= 25000:
        return 0.364 * np.exp(-(h_meters - 11000) / 6340)

    elif h_meters <= 47000:
        return 0.041 * np.exp(-(h_meters - 25000) / 8000)

    elif h_meters <= 86000:
        return 0.0011 * np.exp(-(h_meters - 47000) / 10000)

    elif h_meters <= 150000:
        return 1.2e-7 * np.exp(-(h_meters - 86000) / 20000)

    else:
        return 1.2e-10 * np.exp(-(h_meters - 150000) / 50000)


def simulation(voyager, dt, total_time):
    times = [0]
    speeds = [0]
    heights = [0]
    a_s = [0]
    f = 0

    steps = int(total_time // dt)
    for step in range(1, steps + 1):

        if step * dt <= 91:
            g = 9.8
            t = voyager.step0_mint + voyager.step1_mint
            d_force = drag_force(voyager.cf, voyager.s_surf, find_ro(heights[-1]), speeds[-1])
            a1 = (t - d_force - voyager.total_mass * g) / voyager.total_mass
            v1 = find_v(speeds[-1], a_s[-1], dt)
            height = find_h(heights[-1], v1, a_s[-1], dt)
            voyager.total_mass -= ((dt * (voyager.step0_fuel_mass / voyager.step0_time_to_work)) + dt * (
                    voyager.step1_fuel_mass / voyager.step1_time_to_work))
            a_s.append(a1)
            heights.append(height)
            speeds.append(v1)
            times.append(dt * step)
            print(dt * step, a1, t)
        elif step * dt <= 191:
            g = 9.8
            a1 = (-voyager.total_mass * g) / voyager.total_mass
            v1 = find_v(speeds[-1], a_s[-1], dt)
            height = find_h(heights[-1], v1, a_s[-1], dt)
            a_s.append(a1)
            heights.append(height)
            speeds.append(v1)
            times.append(dt * step)
            print(dt * step, a1, height, v1)

        elif step * dt <= 212:
            g = 9.8
            t = voyager.step0_mint + voyager.step1_mint
            d_force = drag_force(voyager.cf, voyager.s_surf, find_ro(heights[-1]), speeds[-1])
            a1 = (t - d_force - voyager.total_mass * g) / voyager.total_mass
            v1 = find_v(speeds[-1], a_s[-1], dt)
            height = find_h(heights[-1], 0.5 * v1, 0.5 * a_s[-1], dt)
            voyager.total_mass -= ((dt * (voyager.step0_fuel_mass / voyager.step0_time_to_work)) + dt * (
                    voyager.step1_fuel_mass / voyager.step1_time_to_work))
            a_s.append(a1)
            heights.append(height)
            speeds.append(v1)
            times.append(dt * step)


        elif step * dt <= 246:
            if heights[-1] < 100000:
                g = 9.8
            else:
                g = 9
            t = voyager.step2_mint
            d_force = drag_force(voyager.cf, voyager.s_surf, find_ro(heights[-1]), speeds[-1])
            if f == 0:
                voyager.total_mass -= (
                        voyager.step0_mass + voyager.step1_mass - voyager.step0_fuel_mass - voyager.step1_fuel_mass)
                a1 = 40
                f = 1
            else:
                a1 = (t - d_force - voyager.total_mass * g) / voyager.total_mass

            v1 = find_v(speeds[-1], a_s[-1], dt)
            voyager.total_mass -= (dt * (voyager.step2_fuel_mass / voyager.step2_time_to_work))

            height = find_h(heights[-1], 0.2 * v1, 0.2 * a_s[-1], dt)
            a_s.append(a1)
            heights.append(height)
            speeds.append(v1)
            times.append(dt * step)
            print(dt * step, d_force, voyager.total_mass)
    return times, speeds, heights, a_s
