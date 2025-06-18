# src/visuals.py

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import seaborn as sns

def plot_dual_radar(row1, row2, label1, label2):
    categories = row1.index.tolist()
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    values1 = row1.tolist() + [row1.tolist()[0]]
    values2 = row2.tolist() + [row2.tolist()[0]]

    fig, axes = plt.subplots(1, 2, subplot_kw=dict(polar=True), figsize=(14, 6))

    for ax, values, label in zip(axes, [values1, values2], [label1, label2]):
        ax.plot(angles, values, marker='o')
        ax.fill(angles, values, alpha=0.25)
        ax.set_title(label, y=1.1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)
        for txt, angle in zip(ax.get_xticklabels(), angles):
            txt.set_y(txt.get_position()[1] + 0.1)

    return fig

def plot_indicator_over_time(df, country, indicator, ylabel=None):
    data = df[df["country"] == country].copy()
    data = data.sort_values("date")
    data = data.dropna(subset=[indicator])

    data["date"] = data["date"].astype(int)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(x="date", y=indicator, data=data, ax=ax)
    ax.set_title(f"{indicator.replace('_', ' ').title()} – {country}")
    ax.set_xlabel("Año")
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) 
    return fig