class Voyager:
    def __init__(self, dry_mass, initial_fuel_mass, cf, v_is):
        # Начальные параметры Вояджера-1
        self.dry_mass = dry_mass
        self.current_fuel = initial_fuel_mass
        self.v_is = v_is
        self.cf = cf

        self.h = 0
        self.v = 0

    @property
    def current_mass(self):
        return self.dry_mass + self.current_fuel



    def get_position_at_time(self, time_elapsed):
        ...
