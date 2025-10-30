class Voyager:
    def __init__(self):
        # Начальные параметры Вояджера-1
        self.initial_mass = ...
        self.initial_position = [...]

    def current_mass(mission_time, initial_mass, initial_fuel, thrust_percent=100):
        dry_mass = initial_mass - initial_fuel
        thrust_level = thrust_percent / 100
        fuel_consumption_rate = ...  # по какой формуле считаем?
        fuel_used = min(fuel_consumption_rate * mission_time, initial_fuel)
        current_fuel = initial_fuel - fuel_used
        total_mass = dry_mass + current_fuel
        return total_mass

    def get_position_at_time(self, time_elapsed):
        ...
