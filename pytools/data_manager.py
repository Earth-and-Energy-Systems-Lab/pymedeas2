import re
import pathlib
import numpy as np
import pandas as pd

from pysd.py_backend.data import Columns
from pysd.py_backend.utils import load_outputs


class DataContainer:
    """Class for containing all data objects"""
    def __init__(self):
        self.data_objects = set()
        self._variable_list = set()
        self.current_var = None
        self.dimensions = None

    @property
    def variable_list(self):
        """holds the sorted list of variables without dimensions"""
        return sorted(self._variable_list)

    @variable_list.setter
    def variable_list(self, variables):
        """save only variable names not suscripts"""
        self._variable_list.update(variables)

    def add(self, data):
        """Add data from a new experiment"""
        self.data_objects.add(data)
        self.variable_list = data.variable_list

    def set_var(self, var_name):
        """Set the variable for all the data objects"""
        self.current_var = var_name
        self.dimensions = None
        for data in self.data_objects:
            data.set_var(var_name)
            if self.current_var in data.dimensions:
                self.dimensions = data.dimensions[self.current_var]

    def get_values(self, dimensions=None):
        """Get the values for all the data objects"""
        return {
            data.scenario: data.get_values(dimensions)
            for data in self.data_objects}

    def __len__(self):
        return len(self.data_objects)

    def clear(self):
        """Clear objects from memory"""
        for data in self.data_objects:
            data.clear()
            del data

        self.data_objects = set()
        self._variable_list = set()


class Data:
    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""
    def __init__(self):
        self.scenario = ""
        self._variable_list = []
        # TODO: convert cached_values in a FIFO
        self.cached_values = {}
        self.current_var = None
        self.data = pd.DataFrame()
        self.dimensions = {}
        self.columns = []

    @property
    def variable_list(self):
        """holds the sorted list of variables without dimensions"""
        return self._variable_list

    @variable_list.setter
    def variable_list(self, columns):
        """save only variable names not suscripts"""
        self._variable_list = set([
            "[".join(column.split("[")[:-1]) or column
            for column in columns
        ])

    def _add_to_cache(self):
        """Add variable to cache """

        if len(self.columns) == 1:
            self.cached_values[self.current_var] = self.current_var
            self.dimensions[self.current_var] = None
        elif len(self.columns) > 1:
            self.cached_values[self.current_var] = {}
            for column in self.columns:
                subs = tuple(sub.strip() for sub in
                             column[:-1].split("[")[-1].split(","))
                self.cached_values[self.current_var][subs] = column

            self.dimensions[self.current_var] = [
                sorted(set(dim))
                for dim in
                np.array(list(self.cached_values[self.current_var])
                        ).transpose()]

    def get_values(self, dimensions=None):
        """Get values for a given combination of dimensions"""
        if self.current_var not in self.cached_values:
            # variable not in this experiment
            return None
        if dimensions:
            return self.data[self.cached_values[self.current_var][dimensions]]
        else:
            return self.data[self.cached_values[self.current_var]]

    def clear(self):
        """Delete data"""
        del self.data, self.cached_values


class DataFile(Data):

    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.scenario = self._get_scen_name()
        self.variable_list, self.transpose = Columns.get_columns(self.filename)

        if self.transpose:
            self.time = pd.read_csv(
                self.filename, nrows=1, header=None).values[0, 1:]
        else:
            self.time = pd.read_csv(self.filename, usecols=[0]).values

    def _get_scen_name(self):
        """get scenario name from filename"""
        pattern = re.compile(
            r'results_(.*)(?=_[\d]{4}_[\d]{4}_[\d.]*(_old)*.csv)', re.I)
        try:
            return pattern.match(
                pathlib.PurePath(self.filename).name).group(1)
        except ValueError:
            print("To be able to import the scenario name, the output file "
                  "name should be the default one (e.g. results_ScenName_"
                  "InitDate_FinalDate_TimeStep.csv)")
            return input('Unknown Scenario. Please provide a name for the'
                              ' imported scenario: ')

    def set_var(self, var_name):
        """Set current variable and get it from file if necessary"""
        self.current_var = var_name
        self.columns = Columns.get_columns(self.filename, [var_name])[0]

        if self.current_var not in self.cached_values:
            self.data = self.data.join(
                load_outputs(
                    self.filename, self.transpose, columns=self.columns),
                how="outer")
            self._add_to_cache()


class DataLoaded(Data):

    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""

    def __init__(self, scenario, dataframe):
        super().__init__()
        self.scenario = scenario
        self.data = dataframe

        Columns._files[self.scenario] = (self.data.columns, False)

        self.variable_list = Columns.get_columns(self.scenario)[0]
        self.time = self.data.index.values

    def get_var(self, var_name):
        print(Columns.get_columns(self.scenario, var_name))


class DataVensim(Data):

    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""

    def __init__(self, scenario, dataframe):
        super().__init__()
        self.scenario = scenario
        self.data = dataframe



