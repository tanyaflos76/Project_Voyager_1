import krpc
import math
import time
import time_warp
import matplotlib.pyplot as plt

# ---------- mission params ----------
TARGET_PARKING_ALT = 100000.0  # 100 km

# -------------statistic---------------
h_t = []
v_t = []
a_t = []
dt = 0.08


def smooth_angle(current, target, factor=0.1):
    diff = (target - current + 180) % 360 - 180
    return (current + diff * factor) % 360


def smooth(value, target, smooth_factor=0.1):
    return value + (target - value) * smooth_factor


def desired_heading_function(alt):
    if alt < 1000:
        return vessel.flight().heading
    return 90.0


def compute_smooth_pitch(alt, vel,
                         turn_start=2000.0,
                         turn_end=45000.0):
    if alt < turn_start:
        return 90.0

    x = (alt - turn_start) / (turn_end - turn_start)
    x = max(0.0, min(1.0, x))
    s = 3 * x * x - 2 * x * x * x

    pitch = 90.0 * (1.0 - s)

    if alt >= turn_end:
        blend = min((alt - turn_end) / 3000.0, 1.0)
        pitch = pitch * (1.0 - blend)

    if vel < 250:
        min_pitch = 70.0
    elif vel < 400:
        min_pitch = 50.0
    else:
        min_pitch = 0.0

    if pitch < min_pitch:
        blend = 0.2  # 20% сглаживания
        pitch = pitch * (1 - blend) + min_pitch * blend

    return pitch


def execute_node(sc, vessel, node, burn_threshold=3):
    print("[node] Δv:", node.delta_v)
    ap = vessel.auto_pilot
    ap.disengage()
    ap.reference_frame = node.reference_frame
    ap.target_direction = (0, 1, 0)
    ap.target_roll = 0
    ap.engage()

    dv = node.delta_v
    thrust = vessel.available_thrust
    mass = vessel.mass

    if thrust > 0:
        burn_time = dv / (thrust / mass)
    else:
        burn_time = dv * 8.0

    start_ut = node.ut - burn_time

    while sc.ut < start_ut - 0.5:
        time.sleep(0.05)

    # burn
    print("[node] burn start UT:", sc.ut)
    vessel.control.throttle = 1.0

    flag = True
    while node.remaining_delta_v > burn_threshold:
        if flag:
            engine = vessel.parts.engines[-1]  # двигатель первой ступени
            if not engine.has_fuel:
                vessel.control.activate_next_stage()
                vessel.control.throttle = 0.0
                time.sleep(2)
                vessel.control.throttle = 1.0
                vessel.control.activate_next_stage()
                flag = False
        time.sleep(0.05)

    vessel.control.throttle = 0.0

    node.remove()
    print("[node] complete")
    time.sleep(0.3)


def circularize_at_apoapsis(sc, vessel):
    print("[circularize] building node")

    t = vessel.orbit.time_to_apoapsis
    node_ut = sc.ut + t
    try:
        mu = vessel.orbit.body.gravitational_parameter
        r_ap = vessel.orbit.semi_major_axis * (1 + vessel.orbit.eccentricity)
        v_ap = math.sqrt(mu * (2.0 / r_ap - 1.0 / vessel.orbit.semi_major_axis))
        v_circ = math.sqrt(mu / r_ap)
        dv = abs(v_circ - v_ap)
    except:
        dv = 150.0

    node = vessel.control.add_node(node_ut, prograde=dv)
    execute_node(sc, vessel, node)


# ============================================================
#                   ASCENT WITH MANUAL STAGING
# ============================================================

def launch_to_parking(sc, vessel, target_alt=TARGET_PARKING_ALT):
    print("[ascent] starting manual ascent to", target_alt)

    ap = vessel.auto_pilot
    ap.target_pitch_and_heading(90, 90)

    ap.engage()
    time.sleep(0.2)

    print("[ascent] STAGE: ignition + clamps")
    vessel.control.throttle = 1.0
    vessel.control.activate_next_stage()
    vessel.control.activate_next_stage()
    time.sleep(1.0)

    print("[ascent] thrust:", vessel.thrust)
    print("[ascent] liftoff!")

    flag = False

    while True:
        flight = vessel.flight(vessel.surface_reference_frame)

        current_pitch = vessel.auto_pilot.target_pitch
        current_heading = vessel.auto_pilot.target_heading
        alt = flight.mean_altitude
        vel = flight.speed

        desired_pitch = compute_smooth_pitch(alt, vel)
        desired_heading = desired_heading_function(alt)
        pitch = smooth(current_pitch, desired_pitch, 0.08)  # плавность 8%
        heading = smooth_angle(current_heading, desired_heading, 0.08)

        ap.target_pitch = pitch
        ap.target_heading = heading

        apo = vessel.orbit.apoapsis_altitude
        t_to_apo = vessel.orbit.time_to_apoapsis

        if not flag:
            if alt > 36000 and apo > target_alt:
                time.sleep(1.0)
                vessel.control.throttle = 0.0
                flag = True

        if apo > target_alt and t_to_apo < 75.0:
            print("[ascent] approaching apoapsis → circularizing")
            circularize_at_apoapsis(sc, vessel)
            break

        time.sleep(0.04)

    print("[ascent] orbit established.")
    print("Apoapsis:", vessel.orbit.apoapsis_altitude)
    print("Periapsis:", vessel.orbit.periapsis_altitude)


if __name__ == "__main__":
    conn = krpc.connect(name="ManualAutopilot")
    sc = conn.space_center
    vessel = sc.active_vessel

    time_warp.safe_warp_to(sc, vessel, 3955248)
    t0 = sc.ut

    launch_to_parking(sc, vessel)

    print("[mission] waiting for orbit stabilization...")
    time.sleep(3)

    x = [p[0] - t0 for p in h_t]
    y = [p[1] for p in h_t]

    plt.plot(x, y)
    plt.xlabel("Время, с")
    plt.ylabel("Высота, м")
    plt.title("График высоты")
    plt.grid(True)
    plt.show()

    x = [p[0] - t0 for p in v_t]
    y = [p[1] for p in v_t]

    plt.plot(x, y)
    plt.xlabel("Время, с")
    plt.ylabel("Скорость, м/с")
    plt.title("График скорости")
    plt.grid(True)
    plt.show()

    x = [p[0] - t0 for p in a_t]
    y = [p[1] for p in a_t]

    plt.plot(x, y)
    plt.xlabel("Время, с")
    plt.ylabel("Ускорение, м/(с^2)")
    plt.title("График ускорения")
    plt.grid(True)
    plt.show()
