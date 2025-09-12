import pandas as pd

from Practise import LoadType, TotalLoad, HourlyDemand, DemandVisualizer, DieselPowerUnit, DieselGenerator


def build_consumers():
    residential_sector_1 = LoadType("Жилой сектор", 67, 0.95)
    residential_sector_2 = LoadType("Жилой сектор", 67, 0.95)
    utility_needs = LoadType("Хоз. нужды", 12, 0.6)
    lighting = LoadType("Освещение", 7, 1)
    farming = LoadType("Фермерское хозяйство", 192, 0.8)
    drying = LoadType("Сушильная", 12, 1)

    consumers = TotalLoad()
    for cons in (residential_sector_1, residential_sector_2, utility_needs, lighting, farming, drying):
        consumers.append_load(cons)

    return consumers

def load_graph_params():
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

    return daily_load_schedule, season_factors

def demand_data(type):
    hourlydemand = HourlyDemand(build_consumers().total_active_lp(), *load_graph_params())
    match(type):
        case "yearly": return hourlydemand()
        case "monthly": return hourlydemand("Январь")
        case "daily": return hourlydemand("Январь", 1)

def demand_visualizer(type):
    hourlydemand = HourlyDemand(build_consumers().total_active_lp(), *load_graph_params())
    viz = DemandVisualizer(hourlydemand)
    match(type):
        case "yearly": viz.plot_year()
        case "monthly": viz.plot_month("Январь")
        case "daily": viz.plot_day("Январь", 1)

def dpu_base():
    url = ("https://github.com/H2K2U/ASES_Practise_1/raw/refs/heads/main/"
           "Practise/data/%D0%9F%D0%B0%D1%80%D0%B0%D0%BC%D0%B5%D1%82%D1%80%D1%8B"
           "%20%D0%B4%D0%B8%D0%B7%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20"
           "%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B9.xlsx")

    df = pd.read_excel(url, sheet_name="Лист1")
    dpu_base = []
    for _, row in df.iterrows():
        dpu = DieselPowerUnit(name=row["Марка генератора"],
                              rated_active_power=row["Pном (кВт)"],
                              rated_apparent_power=row["Sном (кВА)"],
                              peak_active_power=row["Pпик (кВт)"],
                              spec_fuel_cons=row["q (л/кВт*ч)"]
                              )
        dpu_base.append(dpu)
    dpu_base = list(filter(lambda dpu: dpu.rated_apparent_power, dpu_base))
    return dpu_base

def assembly_dg(name, assembly_type):
    dg = DieselGenerator(name, assembly_type)
    dg.auto_assembly_dg(dpu_base(), build_consumers().total_active_lp())
    return dg

def main():
    #demand_visualizer("daily")
    dg = assembly_dg("Ядерная", "3x30+10")
    print(build_consumers().total_apparent_lp())
    dg.show_table()
    print(dg.rated_apparent_power)


if __name__ == '__main__':
    main()