class Voyager:
    def __init__(self, total_mass, step1, step2, step3, s_nozzle, s_surf, cf):
        self.total_mass = total_mass
        self.step1_mass, self.step1_fuel_mass, self.step1_mint, self.step1_impuls, self.step1_time_to_work = step1
        self.step2_mass, self.step2_fuel_mass, self.step2_mint, self.step2_impuls, self.step2_time_to_work = step2
        self.step3_mass, self.step3_fuel_mass, self.step3_mint, self.step3_impuls, self.step3_time_to_work = step3

        self.s_nozzle = s_nozzle
        self.s_surf = s_surf

        self.cf = cf

    @property
    def current_mass(self):
        return self.total_mass
