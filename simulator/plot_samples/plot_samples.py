from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

from producer.core.producers.traffic_producer import _multimodal_normal_gauss_value
from producer.core.producers.temperature_producer import _sinusoidal_value


def plot_chart(plots: [tuple[np.ndarray, np.ndarray]], title: str, x_label: str,
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
    modes = [(8.5, 0.425), (12.5, 1.88), (18, 0.38)]
    max_x = 18
    max_speed = 80
    mult_factor = 400

    probabilities = [_multimodal_normal_gauss_value(x_i, modes=modes, max_x=max_x) for
                     x_i in x]
    vehicles = [mult_factor * probability for probability in probabilities]
    speed = [max_speed - vehicles_i for vehicles_i in vehicles]

    plot_chart([(x, vehicles)], 'Vehicles per unit', 'Hours', 'Vehicles per s',
               x_ticks=1)
    plot_chart([(x, speed)], 'Average Speed', 'Hours', 'km/h',
               x_ticks=1)


def temperature() -> None:
    timestamp = datetime(2023, 8, 1, 0, 0, 0)
    x = np.linspace(0, 24, 1000)
    y = [round(_sinusoidal_value(timestamp + timedelta(hours=x_i)), 2) for x_i in x]
    formatted = timestamp.strftime('%Y-%m-%d')
    plot_chart([(x, y)], f'Temperature ({formatted})', 'Hours', 'Celsius', x_ticks=1)


def main():
    traffic()
    # temperature()


if __name__ == "__main__":
    main()
