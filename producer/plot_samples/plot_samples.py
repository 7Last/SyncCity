from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

from producer.core.producers.traffic_producer import _multimodal_normal_gauss_value
from producer.core.producers.temperature_producer import _sinusoidal_value


def plot_chart(x: np.ndarray, y: np.ndarray, title: str, x_label: str, y_label: str,
               x_ticks: float = 1) -> None:
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.xticks(np.arange(min(x), max(x) + 1, x_ticks))
    plt.show()


def traffic() -> None:
    x = np.linspace(0, 24, 1000)
    modes = [(8.5, 0.425), (12.5, 1.88), (18, 0.38)]
    max_x = 18
    y = [1000 * _multimodal_normal_gauss_value(x_i, modes=modes, max_x=max_x) for x_i in
         x]
    plot_chart(x, y, 'Traffic', 'Time', 'Traffic', x_ticks=1)


def temperature() -> None:
    timestamp = datetime(2023, 1, 1, 0, 0, 0)
    x = np.linspace(0, 24, 1000)
    y = [round(_sinusoidal_value(timestamp + timedelta(hours=x_i)), 2) for x_i in x]
    plot_chart(x, y, 'Temperature', 'Time', 'Temperature', x_ticks=1)


def main():
    traffic()
    temperature()


if __name__ == "__main__":
    main()
