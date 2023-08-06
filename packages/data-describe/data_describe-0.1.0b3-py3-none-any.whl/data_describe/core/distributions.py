from typing import Dict, Any, Optional

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np

from data_describe.config._config import get_option
from data_describe.metrics.univariate import spikey, skewed
from data_describe._widget import BaseWidget
from data_describe.compat import _is_dataframe
from data_describe.backends import _get_viz_backend, _get_compute_backend


class DistributionWidget(BaseWidget):
    """Container for distributions.

    This class (object) is returned from the ``distribution`` function. The
    attributes documented below can be accessed or extracted.

    Attributes:
        input_data: The input data
        spike_value: Measure of the "spikey"ness metric, which diagnoses spikey
            histograms where the tallest bin is ``n`` times taller than the average bin.
        skew_value: Measure of the skewness metric.
        spike_factor: The threshold factor used to diagnose "spikey"ness.
        skew_factor: The threshold factor used to diagnose skew.
    """

    def __init__(
        self,
        input_data=None,
        spike_value=None,
        skew_value=None,
        spike_factor=None,
        skew_factor=None,
        viz_backend=None,
    ):
        """Distribution Plots.

        Args:
            input_data: The input data
            spike_value: Measure of the "spikey"ness metric, which diagnoses spikey
                histograms where the tallest bin is ``n`` times taller than the average bin.
            skew_value: Measure of the skewness metric.
            spike_factor: The threshold factor used to diagnose "spikey"ness.
            skew_factor: The threshold factor used to diagnose skew.
            viz_backend: The visualization backend.
        """
        self.input_data = input_data
        self.spike_value = spike_value
        self.skew_value = skew_value
        self.spike_factor = spike_factor
        self.skew_factor = skew_factor
        self.viz_backend = viz_backend

    def show(self, viz_backend=None, **kwargs):
        """The default display for this output.

        Displays a summary of diagnostics.

        Args:
            viz_backend (str, optional): The visualization backend.
            **kwargs: Keyword arguments.
        """
        summary_string = """Distribution Summary:
        Skew detected in {} columns.
        Spikey histograms detected in {} columns.

        Use the method plot_distribution("column_name") to view plots for each feature.

        Example:
            dist = DistributionWidget(data)
            dist.plot_distribution("column1")
        """.format(
            np.sum(self.skew_value > self.skew_factor),
            np.sum(self.spike_value > self.spike_factor),
        )
        print(summary_string)

    def plot_distribution(
        self,
        x: Optional[str] = None,
        contrast: Optional[str] = None,
        viz_backend: Optional[str] = None,
        **kwargs,
    ):
        """Generate distribution plot(s).

        Numeric features will be visualized using a histogram/violin plot, and any other
        types will be visualized using a categorical bar plot.

        Args:
            x (str, optional): The feature name to plot. If None, will plot all features.
            contrast (str, optional): The feature name to compare histograms by contrast.
            mode (str): {'combo', 'violin', 'hist'} The type of plot to display.
                Defaults to a combined histogram/violin plot.
            hist_kwargs (dict, optional): Keyword args for seaborn.histplot.
            violin_kwargs (dict, optional): Keyword args for seaborn.violinplot.
            viz_backend (optional): The visualization backend.
            **kwargs: Additional keyword arguments for the visualization backend.

        Returns:
            Histogram plot(s).
        """
        backend = viz_backend or self.viz_backend

        return _get_viz_backend(backend).viz_distribution(
            data=self.input_data, x=x, contrast=contrast, **kwargs
        )


def distribution(
    data, diagnostic=True, compute_backend=None, viz_backend=None, **kwargs
) -> DistributionWidget:
    """Distribution Plots.

    Visualizes univariate distributions. This feature can be used for generating
    various types of plots for univariate distributions, including: histograms, violin
    plots, bar (count) plots.

    Args:
        data: Data Frame
        diagnostic: If True, will run diagnostics to select "interesting" plots.
        compute_backend: The compute backend.
        viz_backend: The visualization backend.
        **kwargs: Keyword arguments.

    Raises:
        ValueError: Invalid input data type.

    Returns:
        DistributionWidget
    """
    if not _is_dataframe(data):
        raise ValueError("DataFrame required.")

    widget = _get_compute_backend(compute_backend, data).compute_distribution(
        data, diagnostic=diagnostic, **kwargs
    )
    return widget


def _pandas_compute_distribution(
    data, diagnostic: bool = True, spike_factor=10, skew_factor=3, **kwargs
):
    """Compute distribution metrics.

    Args:
        data (DataFrame): The data
        diagnostic (bool): If True, will compute diagnostics used to select "interesting" plots.
        spike_factor (int): The spikey-ness factor used to flag spikey histograms. Defaults to 10.
        skew_factor (int): The skew-ness factor used to flag skewed histograms. Defaults to 3.
        **kwargs: Keyword arguments.

    Returns:
        DistributionWidget
    """
    num_data = data.select_dtypes("number")

    spike_value = num_data.apply(spikey, axis=0) if diagnostic else None
    skew_value = num_data.apply(skewed, axis=0) if diagnostic else None

    return DistributionWidget(
        input_data=data,
        spike_value=spike_value,
        skew_value=skew_value,
        spike_factor=spike_factor,
        skew_factor=skew_factor,
    )


def _seaborn_viz_distribution(data, x: str, contrast: Optional[str] = None, **kwargs):
    """Plots the distribution.

    Args:
        data: The data
        x (str): The column to visualize.
        contrast (str, optional): The column to use as a contrast.
        **kwargs: Keyword arguments passed to underlying plot functions.

    Returns:
        matplotlib.figure.Figure
    """
    if x in data.select_dtypes("number").columns:
        return _seaborn_viz_numeric(data, x, contrast, **kwargs)
    else:
        return _seaborn_viz_categorical(data, x, contrast, **kwargs)


def _seaborn_viz_numeric(
    data,
    x: str,
    contrast: Optional[str] = None,
    mode: str = "combo",
    hist_kwargs: Optional[dict] = None,
    violin_kwargs: Optional[dict] = None,
    **kwargs,
):
    """Plots a histogram/violin plot.

    Args:
        data (DataFrame): The data
        x (str): The name of the column to plot
        contrast (str, optional): The name of the categorical column to use for multiple contrasts.
        mode (str): {'combo', 'violin', 'hist'} The type of plot to display.
            Defaults to a combined histogram/violin plot.
        hist_kwargs (dict, optional): Keyword args for seaborn.histplot.
        violin_kwargs (dict, optional): Keyword args for seaborn.violinplot.
        **kwargs: Keyword args to be passed to all underlying plotting functions.

    Raises:
        ValueError: Unknown plot mode.

    Returns:
        Matplotlib figure
    """
    hist_kwargs = hist_kwargs or {}
    violin_kwargs = violin_kwargs or {}
    fig = Figure(
        figsize=(
            get_option("display.matplotlib.fig_width"),
            get_option("display.matplotlib.fig_height"),
        )
    )
    if mode == "combo":
        gs = GridSpec(nrows=5, ncols=1)
        ax1 = fig.add_subplot(gs.new_subplotspec((0, 0), 1, 1))
        ax2 = fig.add_subplot(gs.new_subplotspec((1, 0), 4, 1))

        ax1.spines["right"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        _seaborn_viz_histogram(data, x, contrast, ax=ax1, **hist_kwargs)
        _seaborn_viz_violin(data, x, contrast, ax=ax2, **violin_kwargs)
        ax1.set_title(x)
        return fig
    elif mode == "hist":
        ax = fig.add_subplot()
        _seaborn_viz_histogram(
            data, x, contrast=contrast, ax=ax, **hist_kwargs, **kwargs
        )
        ax.set_title(x)
        return fig
    elif mode == "violin":
        ax = fig.add_subplot()
        _seaborn_viz_violin(
            data, x, contrast=contrast, ax=ax, **violin_kwargs, **kwargs
        )
        ax.set_title(x)
        return fig
    else:
        raise ValueError("Unknown value for 'mode' plot type")


def _seaborn_viz_categorical(data, x: str, contrast: Optional[str] = None, **kwargs):
    """Plots a bar count plot for a categorical feature.

    Args:
        data (DataFrame): The data
        x (str): The name of the column to plot
        contrast (str, optional): The name of the categorical column to use for multiple contrasts.
        **kwargs: Keyword args for seaborn.countplot.

    Returns:
        Matplotlib figure
    """
    bar_kwargs = kwargs or {}
    fig = Figure(
        figsize=(
            get_option("display.matplotlib.fig_width"),
            get_option("display.matplotlib.fig_height"),
        )
    )
    ax = fig.add_subplot()
    _seaborn_viz_bar(data, x, contrast, ax=ax, **bar_kwargs)
    ax.set_title(x)
    return fig


def _seaborn_viz_histogram(data, x: str, contrast: Optional[str] = None, **kwargs):
    """Plot a single histogram.

    Args:
        data (DataFrame): The data
        x (str): The name of the column to plot.
        contrast (str, optional): The name of the categorical column to use for multiple contrasts.
        **kwargs: Keyword arguments passed to seaborn.distplot

    Raises:
        ValueError: Not a numeric column.

    Returns:
        Seaborn Axis Object
    """
    if x not in data.select_dtypes("number").columns:
        raise ValueError("x must be numeric column")

    default_hist_kwargs: Dict[str, Any] = {}
    hist_kwargs = {**default_hist_kwargs, **(kwargs or {})}
    if contrast:
        data[contrast] = data[contrast].astype("category")
        ax = sns.histplot(x=x, hue=contrast, data=data, **hist_kwargs)
    else:
        ax = sns.histplot(data[x], **hist_kwargs)
        ax.set_title(f"Histogram of {x}")
    return ax


def _seaborn_viz_violin(data, x: str, contrast: Optional[str] = None, **kwargs):
    """Plot a single violin plot.

    Args:
        data (DataFrame): The data
        x (str): The name of the column to plot.
        contrast (str, optional): The name of the categorical column to use for multiple contrasts.
        **kwargs: Keyword arguments passed to seaborn.violinplot

    Raises:
        ValueError: Not a numeric column.

    Returns:
        Seaborn Axis Object
    """
    if x not in data.select_dtypes("number").columns:
        raise ValueError("x must be numeric column")

    default_violin_kwargs = {"cut": 0}
    violin_kwargs = {**default_violin_kwargs, **(kwargs or {})}
    if contrast:
        data[contrast] = data[contrast].astype("category")
        ax = sns.violinplot(x=x, y=contrast, data=data, **violin_kwargs)
    else:
        ax = sns.violinplot(x=x, data=data, **violin_kwargs)
    return ax


def _seaborn_viz_bar(data, x: str, contrast: Optional[str] = None, **kwargs):
    """Plot a bar chart (count plot) for categorical features.

    Args:
        data (DataFrame): The data
        x (str): The name of the column to plot.
        contrast (str, optional): The name of the column to use for multiple histograms.
        **kwargs: Keyword arguments passed to seaborn.countplot

    Returns:
        Seaborn Axis Object
    """
    default_bar_kwargs = {"orient": "h"}
    bar_kwargs = {**default_bar_kwargs, **(kwargs or {})}
    if contrast:
        ax = sns.countplot(x=x, hue=contrast, data=data, **bar_kwargs)
    else:
        ax = sns.countplot(x=x, data=data, **bar_kwargs)
    return ax
