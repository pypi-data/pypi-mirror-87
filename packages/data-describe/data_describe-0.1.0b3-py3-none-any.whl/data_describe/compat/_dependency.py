from importlib.util import find_spec
from importlib import import_module
import warnings
from functools import wraps
from types import ModuleType
from typing import Dict, Callable, List

from data_describe.misc.logging import OutputLogger
from data_describe.compat._notebook import _check_plotly_extension


class _DependencyManager:
    """Manages optional dependencies for data-describe.

    Examples:
        Optional modules can be accessed using dictionary-style attributes::

            _compat = _DependencyManager()
            engine = _compat["presidio_analyzer"].AnalyzerEngine()

    Attributes:
        imports (Dict[str, Callable]): A mapping of package names and associated
            import functions to download additional resources.
        installed_modules (Dict[str, bool]): A mapping of packages detected as being
            installed.
        modules (Dict[str, ModuleType]): A mapping of the imported modules. Typically
            accessed using dictionary-style access.
    """

    def __init__(self, imports: Dict[str, Callable]):
        """Manages optional dependencies for data-describe.

        Validates the expected optional dependencies for data-describe and executes
        any additional import logic.

        Args:
            imports (Dict[str, Callable]): A dictionary of module names mapped to callables.
                The Callable will be executed when the module is imported, and can be used to
                run additional download or other set up processes that should happen on import.
        """
        self.imports = imports
        self.installed_modules: Dict[str, bool] = {}
        self.modules: Dict[str, ModuleType] = {}
        self.check_all_install(list(imports.keys()))

    def check_all_install(self, modules: List[str]):
        """Searches for installed modules and determines if they exist.

        The attribute `installed_modules` maps module names to booleans
        for modules which are found.

        Args:
            modules (List[str]): List of module names
        """
        for module in modules:
            self.check_install(module)

    def check_install(self, module: str) -> bool:
        """Checks to see if a module is installed."""
        try:
            return self.installed_modules[module]
        except KeyError:
            try:
                if find_spec(module) is not None:
                    self.installed_modules[module] = True
                else:
                    self.installed_modules[module] = False
            except ImportError as err:
                warnings.warn(f"Failed to import {module}: {str(err)}")
                self.installed_modules[module] = False
            return self.installed_modules[module]

    def import_module(self, module_name: str):
        """Attempts to import the module and execute any side imports."""
        try:
            with OutputLogger(module_name, "INFO"):
                module = import_module(module_name)
                if self.imports.get(module_name) is not None:
                    # Call any side imports
                    if self.imports[module_name]:
                        self.imports[module_name](module)
                self.modules[module_name] = module
                return module
        except ImportError as e:
            raise ImportError(
                f"Unable to import module {module_name} which is required by this feature."
            ) from e

    def __getitem__(self, key: str) -> ModuleType:
        """Allows dictionary-style access to optional modules.

        Args:
            key (str): The module.

        Returns:
            The module.
        """
        # Module already imported
        if key in self.modules.keys():
            return self.modules[key]

        return self.import_module(key)


def plotly_check(module):
    """Check for the plotly notebook extension."""
    _check_plotly_extension()


def nltk_download(module):
    """Downloads NLTK corpora."""
    try:
        module.data.find("tokenizers/punkt")
    except LookupError:
        module.download("punkt")
    try:
        module.data.find("corpora/wordnet")
    except LookupError:
        module.download("wordnet")
    try:
        module.data.find("corpora/stopwords")
    except LookupError:
        module.download("stopwords")


def presidio_download(module):
    """Downloads SpaCy language model."""
    try:
        import spacy  # noqa

        if not spacy.util.is_package("en_core_web_lg"):
            warnings.warn(
                "Downloading en_core_web_lg model for Spacy. This may take several minutes."
            )
            spacy.cli.download("en_core_web_lg")
    except ImportError as err:
        raise ImportError(
            "Couldn't find SpaCy which is required of presidio_analyzer."
        ) from err


_compat = _DependencyManager(
    {
        "nltk": nltk_download,
        "presidio_analyzer": presidio_download,
        "plotly": plotly_check,
    }
)


def _requires(package_name):
    """Marks a method or class that _requires an optional dependency."""

    def f(func):
        @wraps(func)
        def g(*args, **kwargs):
            if not _compat.check_install(package_name):
                raise ImportError(f"{package_name} required to use this feature.")
            _compat[package_name]  # Run any side imports, if applicable
            return func(*args, **kwargs)

        return g

    return f
