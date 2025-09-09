class YearHourlyDemand:
    def __init__(self, daily_load_schedule: list[float], season_factors: dict[str, float]) -> None:
        self.daily_load_schedule = []
        if len(daily_load_schedule) == 12:
            self.daily_load_schedule = [x for x in daily_load_schedule for _ in range(2)]
        elif len(daily_load_schedule) == 24:
            self.daily_load_schedule = daily_load_schedule
        else: raise NotImplementedError
        self.season_factors = season_factors

    def season_max_lp(self, total_active_lp: float) -> dict[str, float]:
        season_max_lp_d = self.season_factors.copy()
        for k in self.season_factors:
            season_max_lp_d[k] = self.season_factors[k] * total_active_lp
        return season_max_lp_d

    def normalize_dls(self) -> list[float]:
        return [x/100 for x in self.daily_load_schedule]

    @staticmethod
    def get_days_in_month(leap: bool = False):
        return {
            "Январь": 31,
            "Февраль": 29 if leap else 28,
            "Март": 31,
            "Апрель": 30,
            "Май": 31,
            "Июнь": 30,
            "Июль": 31,
            "Август": 31,
            "Сентябрь": 30,
            "Октябрь": 31,
            "Ноябрь": 30,
            "Декабрь": 31
        }

    def year_hourly_demand(self, total_active_lp: float):
        days_in_month = self.get_days_in_month()
        year_hourly_demand_lst = []
        season_max_lp_d = self.season_max_lp(total_active_lp)
        dls_lst = self.normalize_dls()
        for month, max_lp in season_max_lp_d.items():
            daily_lp = [max_lp * dls for dls in dls_lst]
            monthly_lp = daily_lp * days_in_month[month]
            year_hourly_demand_lst.extend(monthly_lp)
        return year_hourly_demand_lst