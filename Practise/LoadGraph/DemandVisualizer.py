from __future__ import annotations
from typing import Optional
import matplotlib.pyplot as plt

class DemandVisualizer:
    """
    Визуализация профилей нагрузки из экземпляра HourlyDemand.
    Использует часовые ряды, а подписи на оси X — по центрам месяцев/дней.
    """

    def __init__(self, hd: "HourlyDemand") -> None:
        self.hd = hd
        # фиксируем порядок месяцев из справочника самого класса
        self._days_in_month = self.hd.get_days_in_month()
        self._months = list(self._days_in_month.keys())

    # ---------- вспомогательные ----------
    @staticmethod
    def _stylize(ax, title: str, xlabel: str, ylabel: str):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)

    # ---------- год ----------
    def plot_year(self, show: bool = True, ax: Optional[plt.Axes] = None) -> plt.Axes:
        """
        Годовой профиль: сплошные линии средней/минимальной/максимальной мощности
        + прозрачный голубой «коридор» между минимумом и максимумом.
        """
        y = self.hd.year_hourly_demand()
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        month_centers = []
        monthly_mean, monthly_min, monthly_max = [], [], []

        pos = 0
        for m in self._months:
            hours = self._days_in_month[m] * 24
            seg = y[pos: pos + hours]
            pos += hours

            month_centers.append(pos - hours // 2)
            monthly_mean.append(sum(seg) / len(seg))
            monthly_min.append(min(seg))
            monthly_max.append(max(seg))

        # голубая полупрозрачная заливка между min и max
        ax.fill_between(month_centers, monthly_min, monthly_max,
                        color="lightblue", alpha=0.25,
                        label="Диапазон (мин–макс)")

        # сплошные линии
        ax.plot(month_centers, monthly_mean, color="tab:blue",
                marker="o", linewidth=2, label="Средняя")
        ax.plot(month_centers, monthly_max, color="tab:red",
                marker="o", linewidth=2, label="Максимум")
        ax.plot(month_centers, monthly_min, color="tab:green",
                marker="o", linewidth=2, label="Минимум")

        ax.set_ylim(top=max(monthly_max) * 1.2)

        # вертикальные разделители
        pos = 0
        for m in self._months:
            ax.axvline(pos + 1, linestyle="--", linewidth=0.8, alpha=0.3)
            pos += self._days_in_month[m] * 24

        ax.set_xticks(month_centers, self._months)
        self._stylize(ax, "Годовой профиль нагрузки (мин/сред/макс)",
                      "Месяцы", "Мощность")

        ax.legend()
        if show:
            plt.tight_layout()
            plt.show()
        return ax

    # ---------- месяц ----------
    def plot_month(self, month: str, show: bool = True,
                   ax: Optional[plt.Axes] = None) -> plt.Axes:
        """Профиль месяца: X — дни (подписи у центров дней), Y — мощность по часам."""
        if month not in self._days_in_month:
            raise ValueError("Неверно указан месяц")

        y = self.hd.month_hourly_demand(month)
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        x = range(1, len(y) + 1)
        ax.plot(x, y, linewidth=1)

        # границы дней и подписи по центрам
        day_starts, day_centers, pos = [], [], 1
        for d in range(1, self._days_in_month[month] + 1):
            day_starts.append(pos)
            center = pos + 12  # середина суток
            day_centers.append(center)
            pos += 24

        for s in day_starts:
            ax.axvline(s, linestyle="--", linewidth=0.6, alpha=0.3)

        ax.set_xticks(day_centers,
                      [str(i) for i in range(1, self._days_in_month[month] + 1)])
        self._stylize(ax, f"Почасовой профиль: {month}", "Дни месяца", "Мощность")

        # ▸ небольшой запас по Y
        ax.set_ylim(top=max(y) * 1.1)  # +10 % (или +константа: top=max(y)+20)

        if show:
            plt.tight_layout()
            plt.show()
        return ax

    # ---------- сутки ----------
    def plot_day(self, month: str, day: int, show: bool = True,
                 ax: Optional[plt.Axes] = None) -> plt.Axes:
        """Суточный профиль: X — часы 1..24, Y — мощность за час."""
        y_day = self.hd.daily_hourly_demand(month, day)
        if len(y_day) != 24:
            raise ValueError("Ожидались 24 значения для суток")

        hours = [str(h) for h in range(1, 25)]
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 4))

        # ▸ бардовый цвет + чуть более узкие столбцы (width<0.8 «сдвигает» ближе)
        ax.bar(hours, y_day,
               color="#800020",  # бордовый (можно 'maroon')
               width=0.9)  # меньше 0.8 для более плотного вида

        self._stylize(ax, f"Почасовая мощность: {month}, день {day}",
                      "Часы", "Мощность")

        # ▸ небольшой запас по Y
        ax.set_ylim(top=max(y_day) * 1.1)

        if show:
            plt.tight_layout()
            plt.show()
        return ax

