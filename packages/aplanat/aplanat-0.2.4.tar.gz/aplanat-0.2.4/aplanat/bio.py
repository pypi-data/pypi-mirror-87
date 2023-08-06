"""Bio specific plots, could be generalised."""

from io import StringIO

from bokeh.models import Range1d
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure
import numpy as np
import pandas as pd

# TODO: replace this with data read from a fasta.fai or similar
chrom_data = """
order chrom length
1 1 249250621
2 2 243199373
3 3 198022430
4 4 191154276
5 5 180915260
6 6 171115067
7 7 159138663
8 8 146364022
9 9 141213431
10 10 135534747
11 11 135006516
12 12 133851895
13 13 115169878
14 14 107349540
15 15 102531392
16 16 90354753
17 17 81195210
18 18 78077248
19 19 59128983
20 20 63025520
21 21 48129895
22 22 51304566
23 X 155270560
24 Y 59373566
"""
chrom_data = pd.read_csv(StringIO(chrom_data), delimiter=" ")


def karyotype(x_datas, y_datas, names=None, colors=None, alpha=0.2, **kwargs):
    """Create a heatmap from three columns.

    :param x: x-axis coordinates (chromosome position)
    :param y: y-axis coordinates (chromosome)
    :param name: title for z-axis.
    :param colors: colours to plot tics for each data series.
    :param alpha: alpha level (transparency) with which to plot tics.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    """
    if names is None:
        names = [None] * len(x_datas)
    if colors is None:
        colors = [None] * len(x_datas)
    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)
    p = figure(**defaults)
    width = 0.8
    p.rect(
        chrom_data["length"] // 2, chrom_data["order"],
        chrom_data["length"], width,
        fill_color='white', line_color='black')

    plot_order = dict(zip(chrom_data['chrom'], chrom_data['order']))
    for x, y, name, color in zip(x_datas, y_datas, names, colors):
        y = np.array([plot_order[i] for i in y])
        kw = {'alpha': alpha}
        if name is not None:
            kw['legend_label'] = name
        if color is not None:
            kw['color'] = color
        p.segment(
            x, y - width / 2, x, y + width / 2, **kw)

    # set up the axes
    p.xaxis.formatter.use_scientific = False
    p.yaxis.ticker = FixedTicker()
    p.yaxis.ticker.ticks = list(range(1, 25))
    p.yaxis.major_label_overrides = {23: 'X', 24: 'Y'}
    p.x_range = Range1d(
        start=0, end=max(chrom_data['length']),
        bounds=(0, max(chrom_data['length'])))
    miny, maxy = 0, len(chrom_data) + 1
    p.y_range = Range1d(
        start=miny, end=maxy, bounds=(miny, maxy))
    return p
