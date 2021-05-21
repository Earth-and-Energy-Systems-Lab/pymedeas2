"""
These are the decorators used by the functions in the model file.
functions.py
"""
from functools import wraps
import xarray as xr


def subs(dims, subcoords):
    """
    This decorators returns the python object with the correct dimensions
    xarray.DataArray. The algorithm is a simple version of utils.rearrange
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args):
            data = function(*args)
            coords = {dim: subcoords[dim] for dim in dims}

            if isinstance(data, xr.DataArray):
                dacoords = {coord: list(data.coords[coord].values)
                            for coord in data.coords}
                if data.dims == tuple(dims) and dacoords == coords:
                    # If the input data already has the output format
                    # return it.
                    return data
                if set(data.dims).issubset(set(dims)):
                    # The coordinates are expanded or transposed
                    return xr.DataArray(0, coords, dims) + data

                # Vensim equivalent:
                # Subscript X appears on the right, but not left.
                raise ValueError(
                    "Some subscripts are in the output, but not"
                    + " in the definition of the function.\n"
                    + "Function name: {}\n".format(function.__name__)
                    + "Definition subscripts: {}\n".format(tuple(dims))
                    + "Output subscripts: {}\n".format(data.dims)
                    + "Output value: {}\n".format(data))

            elif data is not None:
                return xr.DataArray(data, coords, dims)

            return data

        return wrapper
    return decorator


def to_float(function):
    """
    This decorators ensures to return a float if it crashes, then means
    that something went wrong inside the computation.
    """
    @wraps(function)
    def wrapper(*args):
        try:
            return float(function(*args))
        except TypeError:
            out = function(*args)
            if out is None:
                return None
            else:
                # Vensim equivalent:
                # Subscript X appears on the right, but not left.
                raise TypeError(
                    "Trying to convert to a float an xarray.\n"
                    + "Function name: {}\n".format(function.__name__)
                    + "Output subscripts: {}\n".format(out.dims)
                    + "Output value: {}\n".format(out))
    return wrapper


class Cache(object):
    """
    This is the class for the chache. Several cache types can be saved
    in dictionaries and acces using cache.data[cache_type].
    """
    def __init__(self):
        self.types = ['run', 'step']
        self.data = {t: {} for t in self.types}
        self.time = None

    def run(self, func, *args):
        """ Decorator for caching at a run level"""
        func.type = "run"
        @wraps(func)
        def cached_func(*args):
            """Run wise cache function"""
            try:  # fails if cache is not instantiated
                return self.data['run'][func.__name__]
            except KeyError:
                value = func(*args)
                self.data['run'][func.__name__] = value
                return value
        return cached_func

    def step(self, func, *args):
        """ Decorator for caching at a step level"""
        func.type = "step"
        @wraps(func)
        def cached_func(*args):
            """Step wise cache function"""
            try:  # fails if cache is not instantiated or if it is None
                value = self.data['step'][func.__name__]
                assert value is not None
            except (KeyError, AssertionError):
                value = func(*args)
                self.data['step'][func.__name__] = value
            return value
        return cached_func

    def reset(self, time):
        """
        Resets the time to the given one and cleans the step cache.

        Parameters
        ----------
        time: float
          The time to be set.

        """
        for key in self.data['step']:
            self.data['step'][key] = None

        self.time = time

    def clean(self, horizon=None):
        """
        Cleans the cache.

        Parameters
        ----------
        horizon: str or list of str (optional)
          Name(s) of the cache(s) to clean.

        """
        if horizon is None:
            horizon = self.types
        elif isinstance(horizon, str):
            horizon = [horizon]

        for k in horizon:
            self.data[k] = {}


# create cache object, this way we can still keep importing cache as before
cache = Cache()
