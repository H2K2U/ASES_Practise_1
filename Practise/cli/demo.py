import matplotlib.pyplot as plt
import pandas as pd

from Practise import LoadType, TotalLoad, YearHourlyDemand


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

    yhd = YearHourlyDemand(daily_load_schedule, season_factors)
    annual_load = yhd.year_hourly_demand(consumers.total_active_lp())

    # ---------- Визуализация ----------
    idx = pd.date_range(start="2024-01-01", periods=len(annual_load), freq="H")
    s = pd.Series(annual_load, index=idx)

    # агрегируем по месяцам
    monthly_mean = s.resample("M").mean()
    monthly_max = s.resample("M").max()
    monthly_min = s.resample("M").min()

    # подписи месяцев
    months = monthly_mean.index.strftime("%b")

    plt.figure(figsize=(10, 5))

    # заливка между минимумом и максимумом
    plt.fill_between(months, monthly_min.values, monthly_max.values,
                     color="lightblue", alpha=0.3, label="Диапазон (мин–макс)")

    # линия средней нагрузки
    plt.plot(months, monthly_mean.values, marker="o", linewidth=2,
             color="tab:blue", label="Средняя нагрузка")

    # линии min и max (для наглядности)
    plt.plot(months, monthly_max.values, linestyle="--", color="tab:red", label="Максимум")
    plt.plot(months, monthly_min.values, linestyle="--", color="tab:green", label="Минимум")

    plt.title("Месячные нагрузки за год", fontsize=14)
    plt.xlabel("Месяц")
    plt.ylabel("Мощность, кВт")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()