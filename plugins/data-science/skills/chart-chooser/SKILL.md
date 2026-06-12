---
name: chart-chooser
description: >
  Pick the right chart type for a dataset and analytical question, and name a
  Python library to draw it. Use when the user asks "how should I plot/visualize
  this", which chart fits their data, or is choosing between bar/line/scatter/etc.
  Starter skill — extend as needed.
metadata:
  version: "2026-06-12"
---

# Chart Chooser

Choose by the **question** and the **variable types**, not by habit.

> Starter heuristic — pair with the `data-visualization` skill (if installed) for
> styling and accessibility.

## By intent

| You want to show… | Chart | Notes |
| ----------------- | ----- | ----- |
| Comparison across categories | Bar (horizontal if labels are long) | Sort by value unless order is meaningful. |
| Trend over time | Line | One line per series; avoid > ~5 lines. |
| Relationship between two numerics | Scatter | Add a trend/LOESS line if assessing correlation. |
| Distribution of one numeric | Histogram / KDE / box / violin | Box for compact comparison across groups. |
| Part-to-whole | Stacked bar (preferred) or pie (≤ ~4 slices) | Avoid pies for precise comparison. |
| Composition over time | Stacked area | Watch for occlusion of small series. |
| Two categoricals (counts) | Heatmap / grouped bar | Heatmap scales to many categories. |
| Geospatial | Choropleth / point map | Match projection to the region. |
| Ranking / magnitude per item | Lollipop / dot plot | Cleaner than bars for many items. |

## Variable-type cheat sheet

```
1 categorical            → bar (counts), pie (few slices)
1 numeric                → histogram, KDE, box, violin
1 categorical + 1 numeric→ grouped/box-by-category, bar of summary stat
2 numeric                → scatter (+ trend), hexbin (dense), 2D density
time + numeric           → line, area
2 categorical            → heatmap, mosaic, grouped bar
3+ variables             → facets / small multiples; encode 3rd as color/size
```

## Library pick (Python)

- **matplotlib** — full control, publication figures.
- **seaborn** — statistical plots in one line (`sns.boxplot`, `sns.scatterplot`).
- **plotly** — interactive / hover / dashboards.

## Guardrails

- Start the y-axis of **bar** charts at zero; line charts may use a focused range.
- Don't encode the same variable twice (e.g. color + x for the same field).
- Prefer direct labels over legends when there are few series.
- Check color choices for color-vision deficiency (use a CVD-safe palette).
