from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

from simulator.core.simulators.temperature_simulator import _sinusoidal_value
from simulator.core.simulators.traffic_simulator import _multimodal_gauss_value


def plot_chart(plots: [tuple[np.ndarray, np.ndarray]], title: str, *, x_label: str,
               y_label: str, legend: [str] = None, x_ticks: float = 1) -> None:
    for x, y in plots:
        plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if legend:
        plt.legend(legend)
    plt.title(title)
    plt.grid(True)
    plt.xticks(np.arange(0, 24, x_ticks))
    plt.show()


def traffic() -> None:
    x = np.linspace(0, 24, 1000)
    modes = [
        (0, 2.1),
        (4, 2.2),
        (13, 3),
        (21, 3),
        (24, 3)
    ]

    speed = [
        100 * _multimodal_gauss_value(x_i, modes=modes)
        for x_i in x
    ]

    plot_chart(
        plots=[(x, speed)],
        title='Speed in km/h',
        x_label='Time',
        y_label='Speed in km/h',
        x_ticks=1,
    )

    modes = [
        (0, 4),
        (8.5, 1.8),
        (13, 2),
        (17.5, 1.7),
        (21, 3)
    ]
    vehicles = [
        200 * _multimodal_gauss_value(x_i, modes=modes)
        for x_i in x
    ]

    plot_chart(
        plots=[(x, vehicles)],
        title='Vehicles per Hour',
        x_label='Time',
        y_label='Vehicles per hour',
        x_ticks=1,
    )


def temperature() -> None:
    timestamp = datetime(2023, 8, 1, 0, 0, 0)
    x = np.linspace(0, 24, 1000)
    y = [round(_sinusoidal_value(timestamp + timedelta(hours=x_i)), 2) for x_i in x]
    formatted = timestamp.strftime('%Y-%m-%d')
    plot_chart([(x, y)], f'Temperature ({formatted})', x_label='Time',
               y_label='Celsius', x_ticks=1)


def main():
    traffic()
    # temperature()


if __name__ == "__main__":
    main()
