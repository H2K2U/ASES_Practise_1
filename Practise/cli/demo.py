import matplotlib.pyplot as plt
import pandas as pd

from Practise import LoadType, TotalLoad, HourlyDemand, DemandVisualizer


def main():
    residential_sector_1 = LoadType("Жилой сектор", 67, 0.95)
    residential_sector_2 = LoadType("Жилой сектор", 67, 0.95)
    utility_needs = LoadType("Хоз. нужды", 12, 0.6)
    lightning = LoadType("Освещение", 7, 1)
    farming = LoadType("Фермерское хозяйство", 192, 0.8)
    drying = LoadType("Сушильная", 12, 1)

    consumers = TotalLoad()
    consumers.append_load(residential_sector_1)
    consumers.append_load(residential_sector_2)
    consumers.append_load(utility_needs)
    consumers.append_load(lightning)
    consumers.append_load(farming)
    consumers.append_load(drying)

    daily_load_schedule = [15, 15, 25, 70, 60, 70, 80, 55, 70, 100, 65, 30]
    season_factors = {
        "Январь": 1.0,
        "Февраль": 1.0,
        "Март": 0.9,
        "Апрель": 0.8,
        "Май": 0.8,
        "Июнь": 0.7,
        "Июль": 0.7,
        "Август": 0.7,
        "Сентябрь": 0.8,
        "Октябрь": 0.9,
        "Ноябрь": 0.9,
        "Декабрь": 1.0
    }

    hourlydemand = HourlyDemand(consumers.total_active_lp(), daily_load_schedule, season_factors)

    yearly_demand = hourlydemand()
    monthly_demand = hourlydemand("Январь")
    daily_demand = hourlydemand("Январь", 10)

    # hd = HourlyDemand(total_active_lp, daily_load_schedule, season_factors)
    viz = DemandVisualizer(hourlydemand)

    viz.plot_year()              # месяцы по X, часовой ряд за год по Y
    viz.plot_month("Апрель")     # дни по X, часовой ряд месяца по Y
    viz.plot_day("Апрель", 10)   # часы 1..24 по X, суточный профиль по Y


if __name__ == '__main__':
    main()