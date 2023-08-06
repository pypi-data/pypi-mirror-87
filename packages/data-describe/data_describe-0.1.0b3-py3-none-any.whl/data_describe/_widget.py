from abc import ABC, abstractmethod


class BaseWidget(ABC):
    """Interface for collecting information and visualizations for a feature.

    A "widget" serves as a container for data, diagnostics, and other outputs
    (i.e. DataFrames, plots, estimators etc.) for a feature in data-describe.
    """

    def __init__(self, compute_backend=None, viz_backend=None, **kwargs):
        """Instantiates a BaseWidget.

        Attributes are not explicitly required to be assigned on instantiation;
        data-describe does not constrain or require assignment of (possibly "private")
        attributes after instantiation. Widgets may be used to pass data between
        internal calculations (possibly across different backends) as the final widget
        state is accumulated.

        However, it is strongly recommended to add all expected attributes to
        the __init__ signature for documentation purposes.

        Args:
            compute_backend: The compute backend
            viz_backend: The visualization backend. Must be assigned if the user
                specified a value
            **kwargs: Keyword arguments.
        """
        self.compute_backend = compute_backend
        self.viz_backend = viz_backend
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __str__(self):
        return "data-describe Base Widget"

    # TODO (haishiro): Use @final from typing; requires Python 3.8+
    def _repr_html_(self):
        """Displays the object (widget) when it is on the last line in a Jupyter Notebook cell."""
        try:
            from IPython.display import display

            return display(self.show())
        except ImportError:
            return self.show()

    @abstractmethod
    def show(self, viz_backend=None):
        """Show the default output.

        Assembles the object to be displayed by _repr_html_. This should respect the
        viz_backend, if applicable.

        Args:
            viz_backend: The visualization backend

        Raises:
            NotImplementedError: No default visualization defined.
        """
        backend = viz_backend or self.viz_backend  # noqa: F841

        raise NotImplementedError(
            "No default visualization defined defined on this widget."
        )
