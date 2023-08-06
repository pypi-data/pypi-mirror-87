"""Simple one-off utility methods with no clear home."""

def check_matplotlib_support(caller_name: str) -> None:
    """Raise ImportError with detailed error message if matplotlib is not installed.

    Functionality requiring matplotlib should call this helper and then lazily import.

    Args:    
        caller_name: The name of the caller that requires matplotlib.

    Remarks:
        This pattern borrows heavily from sklearn. As of 6/20/2020 sklearn code could be found
        at https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/__init__.py
    """
    try:
        import matplotlib # type: ignore
    except ImportError as e:
        raise ImportError(
            caller_name + " requires matplotlib. You can "
            "install matplotlib with `pip install matplotlib`."
        ) from e

def check_vowpal_support(caller_name: str) -> None:
    """Raise ImportError with detailed error message if vowpalwabbit is not installed.

    Functionality requiring the vowpalwabbit should call this helper and then lazily import.

    Args:    
        caller_name: The name of the caller that requires matplotlib.

    Remarks:
        This pattern was inspired by sklearn (see coba.utilities.check_matplotlib_support for more information).
    """
    try:
        import vowpalwabbit # type: ignore
    except ImportError as e:
        raise ImportError(
            caller_name + " requires vowpalwabbit. You can "
            "install vowpalwabbit with `pip install vowpalwabbit`."
        ) from e

def check_pandas_support(caller_name: str) -> None:
    """Raise ImportError with detailed error message if pandas is not installed.

    Functionality requiring the pandas should call this helper and then lazily import.

    Args:
        caller_name: The name of the caller that requires pandas.

    Remarks:
        This pattern was inspired by sklearn (see coba.utilities.check_matplotlib_support for more information).
    """
    try:
        import pandas # type: ignore
    except ImportError as e:
        raise ImportError(
            caller_name + " requires pandas. You can "
            "install pandas with `pip install pandas`."
        ) from e