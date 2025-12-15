import numpy as np

from mat_model.simulation import fuel_consamp


def v_is(imp, g):  # Удельный импульс
    return imp * g


def drag_force(cf, s, ro, v):  # Аэродинамическое сопротивление Fc
    return cf * s * (ro * v ** 2 / 2)


def current_g_h(h, r0=6378137, g0=9.80665):  # Изменение g(h)
    return g0 * (r0 / (r0 + h)) ** 2


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
    return v0 + aver_a * dt / 2


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
    if h_meters <= 11000:  # 0-11 км (тропосфера)
        # rho = rho0 * (T0/T)^(g/(R*L) + 1)
        # Упрощенно: rho0 = 1.225, H = 8500 м
        return 1.225 * np.exp(-h_meters / 8500)

    elif h_meters <= 25000:  # 11-25 км (стратосфера)
        # Плотность на 11 км: ~0.364 кг/м³
        return 0.364 * np.exp(-(h_meters - 11000) / 6340)

    elif h_meters <= 47000:  # 25-47 км
        return 0.041 * np.exp(-(h_meters - 25000) / 8000)

    elif h_meters <= 86000:  # 47-86 км
        return 0.0011 * np.exp(-(h_meters - 47000) / 10000)

    elif h_meters <= 150000:  # 86-150 км
        return 1.2e-7 * np.exp(-(h_meters - 86000) / 20000)

    else:  # 150+ км (экзосфера)
        return 1.2e-10 * np.exp(-(h_meters - 150000) / 50000)


def simulation(voyager, dt, total_time):
    times = [0]
    speeds = [0]
    heights = [0]
    acceleration = 0
    t = 0
    engine_on = True
    # # Итерации, на которых перестают работать ступени:
    # iter_step0_off = iter_step1_off = voyager.step0_time_to_work // dt + 1
    # iter_step2_off = voyager.step2_time_to_work // dt + 1 + iter_step1_off
    # iter_step3_off = voyager.step3_time_to_work // dt + 1 + iter_step2_off
    # iter_step4_off = voyager.step4_time_to_work // dt + 1 + iter_step3_off

    steps = total_time / dt
    for step in range(1, steps + 1):
        if (voyager.step1_fuel_mass is not None) and (voyager.step1_fuel_mass <= 0):
            # сразу перестают работать и ускорители, и первая ступень
            voyager.total_mass -= (
                    (voyager.step0_mass - voyager.step0_fuel_mass) - (voyager.step1_mass - voyager.step1_fuel_mass))
            fuel_consump = (voyager.step2_fuel_mass / voyager.step2_time_to_work)
            v_i = v_is(voyager.step2_impuls, current_g_h(heights[-1]))
            p_e = ...
            voyager.step1_fuel_mass = None
        elif (voyager.step2_fuel_mass is not None) and (voyager.step2_fuel_mass <= 0):
            voyager.total_mass -= (voyager.step2_mass - voyager.step2_fuel_mass)
            fuel_consump = (voyager.step3_fuel_mass / voyager.step3_time_to_work)
            v_i = v_is(voyager.step3_impuls, current_g_h(heights[-1]))
            p_e = ...
        elif (voyager.step3_fuel_mass is not None) and (voyager.step3_fuel_mass <= 0):
            voyager.total_mass -= (voyager.step3_mass - voyager.step3_fuel_mass)
            fuel_consump = (voyager.step4_fuel_mass / voyager.step4_time_to_work)
            v_i = v_is(voyager.step4_impuls, current_g_h(heights[-1]))
            p_e = ...
        elif (voyager.step4_fuel_mass is not None) and (voyager.step4_fuel_mass <= 0):
            voyager.total_mass -= (voyager.step4_mass - voyager.step4_fuel_mass)
        else:
            engine_on = False  # Топливо закончилось

        if voyager.step1_fuel_mass > 0:
            # Пока работают ускорители
            t1 = 2 * thrust_at_height(dt * (voyager.step0_fuel_mass / voyager.step0_time_to_work),
                                      v_is(voyager.step0_impuls, current_g_h(heights[-1])), voyager.s_nozzle, p_e,
                                      find_p_atm(heights[-1]))
            t2 = thrust_at_height(dt * (voyager.step1_fuel_mass / voyager.step1_time_to_work),
                                  v_is(voyager.step1_impuls, current_g_h(heights[-1])), voyager.s_nozzle, p_e,
                                  find_p_atm(heights[-1]))
            t = t1 + t2
        elif voyager.step4_fuel_mass > 0:
            # Пока работают какие-нибудь двигатели
            t = thrust_at_height(dt * fuel_consump, v_i, voyager.s_nozzle, p_e, find_p_atm(heights[-1]))


        if heights[-1] < 100000:
            # до 100000м высоты: A = (T - Fs - mg) / m
            d_force = drag_force(voyager.cf, voyager.s_surf, find_ro(heights[-1]), speeds[-1])
            a1 = (t - d_force - voyager.total_mass * current_g_h(heights[-1])) / voyager.total_mass

        elif heights[-1] < 300000:
            # до 300000м высоты: A = (T - mg) / m
            a1 = (t - voyager.total_mass * current_g_h(heights[-1])) / voyager.total_mass

        elif heights[-1] < 8.416 * 10 ** 7:
            # до 8.416*10**7м высоты: A = (T - Fs - mg) / m
            a1 = (t - d_force - voyager.total_mass * current_g_h(heights[-1])) / voyager.total_mass

        elif ...:  # кончится время работы движка:
            pass

        v1 = find_v(speeds[-1], (a1 + acceleration) / 2, dt)
        height = find_h(heights[-1], (v1 + speeds[-1]) / 2, (a1 + acceleration) / 2, dt)
        voyager.total_mass -= (dt * fuel_consump)
        acceleration = a1
        heights.append(height)
        speeds.append(v1)
        times.append(dt * step)
    return times, speeds, heights

# получение конечной массы, скорости, ускорения, высоты после секунды полета

# t = 2 * thrust_at_height(5 * fuel_consamp, v_i, s_sopla, p_e, p_atm)
# d_force = drag_force(cf, total_s, ro, v0)
# a5 = a(t, d_force, total_m, g)
# v5 = v(v0, (a5 + a0) / 2, dt)
# height5 = h(0, (v5 + v0) / 2, (a5 + a0) / 2, dt)
# m5 = total_m - dt * fuel_consamp
# print(
#     f"Скорость конечная:{v5}, высота:{height5}, масса конечная:{m5}, ускорение конечное:{a5}, тяга :{t}, скорость истечения:{v_i}")
