import re
from pathlib import Path

import numpy as np
import pandas as pd

from tkinter import Entry, Label, Tk
from tkinter import ttk

from pysd.py_backend.data import Columns
from pysd.py_backend.utils import load_outputs
from pysd.tools.ncfiles import NCFile


class DataContainer:
    """Class for containing all data objects"""
    def __init__(self):
        self.data_objects = []
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
        self.data_objects.append(data)
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
        scen_rep = {}
        return_dict = {}

        for data in self.data_objects:
            values = data.get_values(dimensions)

            if data.scenario not in return_dict:
                return_dict.update({data.scenario: values})
            else:
                if data.scenario not in scen_rep:
                    scen_rep[data.scenario] = 1
                else:
                    scen_rep[data.scenario] += 1
                return_dict.update(
                    {data.scenario + "_" + str(scen_rep[data.scenario]): values
                     })

        return return_dict

    def __len__(self):
        return len(self.data_objects)

    def clear(self):
        """Clear objects from memory"""
        for data in self.data_objects:
            data.clear()
            del data

        self.data_objects = []
        self._variable_list = set()


class Data:
    """
    Class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame
    """
    def __init__(self):
        self.scenario = ""
        self._variable_list = []
        self.cached_values = {}
        self.current_var = None
        self.data = pd.DataFrame()
        self.dimensions = {}
        self.columns = []

    @property
    def variable_list(self):
        """
        Holds the sorted list of variables without dimensions
        """
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
        if not self.columns:
            self.cached_values[self.current_var] = None
        elif len(self.columns) == 1:
            (self.cached_values[self.current_var],) = self.columns
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
                np.array(
                    list(self.cached_values[self.current_var])
                ).transpose()
            ]

    def get_values(self, dimensions=None):
        """Get values for a given combination of dimensions"""
        column = self.cached_values[self.current_var]
        if not column or (dimensions and dimensions not in column):
            return None
        elif dimensions:
            return self.data[column[dimensions]]
        else:
            return self.data[column]

    def clear(self):
        """Delete data"""
        del self.data, self.cached_values


class DataLoaded(Data):

    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""

    def __init__(self, data, scenario):
        super().__init__()
        self.scenario = scenario
        self.data = data
        self.variable_list = self.get_variables_list()

    def get_variables_list(self):
        """Get list of variables in the data"""
        # Fake read of the columns to be able to use class methods
        Columns._files[Path(self.scenario)] =\
            (self.data.columns, False)
        return Columns.get_columns(self.scenario)[0]

    def set_var(self, var_name):
        """Set current variable"""
        self.current_var = var_name
        self.columns = None

        if self.current_var not in self.cached_values:
            self.columns = Columns.get_columns(self.scenario, [var_name])[0]
            self._add_to_cache()


class DataFile(Data):

    """
    Class that holds the data to be plotted when loaded from a csv or tab file
    """

    def __init__(self, filename, test=False):
        super().__init__()
        self.test = test
        self.filename = filename
        self.scenario = self._get_scen_name()
        self.variable_list, self.transpose = Columns.get_columns(self.filename)

    def _get_scen_name(self):
        """get scenario name from filename"""
        pattern = re.compile(
            r'results_(.*)(?=_[\d]{4}_[\d]{4}_[\d.]*(_[\d]{8}__[\d]{6})*.tab)',
            re.I)

        match = pattern.match(self.filename.name)

        if match:
            return match.group(1)

        res = ScenarioDefWindow()

        if self.test or res.scenario_name is None:
            return "Unknown"

        return res.scenario_name

    def set_var(self, var_name):
        """Set current variable and get it from file if necessary"""
        self.current_var = var_name
        self.columns = None

        if self.current_var not in self.cached_values:
            self.columns = Columns.get_columns(self.filename, [var_name])[0]
            if self.columns:
                # selected variable is not in this dataset
                self.data = self.data.join(
                    load_outputs(
                        self.filename, self.transpose, columns=self.columns),
                    how="outer")

            self._add_to_cache()



class DataNCFile(Data):

    """
    Class that holds the xarray Dataset to be plotted when loading from netCDF
    """

    def __init__(self, filename, test=False):
        super().__init__()
        self.test = test
        self.filename = Path(filename)
        # lazy loading (requires dask)
        self.dataset = NCFile(filename=filename, parallel=True).ds
        self.scenario = self._get_scen_name()
        self.time_dim = None
        self.dimensions = {}


        # get the time array
        for da in self.dataset.data_vars.values():
            if "time" in da.dims:
                self.time_dim = da.coords["time"].values
                break

        self.real_and_pyname = {
            self.remove_quotes(self.dataset[name].attrs["Real Name"]
                               ): name
            for name in self.dataset.data_vars.keys()}

        self.variable_list = sorted(self.real_and_pyname.keys())

    def remove_quotes(self, var):
        if var.startswith('"') and var.endswith('"'):
            return var[1:-1]
        return var

    def _get_scen_name(self):
        """get scenario name from filename"""
        pattern = re.compile(
            r'results_(.*)(?=_[\d]{4}_[\d]{4}_[\d.]*(_[\d]{8}__[\d]{6})*.nc)',
            re.I)

        # try to detect the scenario name from the file name (only works if
        # filename is default)
        match = pattern.match(self.filename.name)

        if match:
            return match.group(1)

        # ask user for a scenario name
        res = ScenarioDefWindow()

        if self.test or res.scenario_name is None:
            return "Unknown"

        return res.scenario_name

    def set_var(self, var_name):
        """
        Sets the data, dimensions and columns attributes
        """
        self.current_var = var_name

        # these three attrs are updated every time a variable is selected in
        # the GUI
        self.data = None
        self.columns = None

        # xarray DataArray
        if var_name in self.real_and_pyname.keys():

            self.dimensions[self.current_var] = None

            self.data = self.dataset[self.real_and_pyname[var_name]]

            # adding time dimension to constant variables
            if "time" not in self.data.dims:
                self.data = self.data.expand_dims(dim={"time": self.time_dim})

            # removing time from dims
            dims_without_time = [d for d in self.data.dims if d != "time"]

            # getting all coords combinations
            if dims_without_time:
                stacked_dims = self.data.stack(
                    stacked_dim=dims_without_time).coords["stacked_dim"].values

                self.columns = {
                    coords: {
                        dim: coord_val
                        for (dim, coord_val) in zip(dims_without_time, coords)
                        } for coords in stacked_dims}

                self.dimensions[self.current_var] = [
                    self.data.coords[dim].values
                    for dim in self.data.dims
                    if dim != "time"]

    def get_values(self, dimensions=None):
        """Get values for a given combination of dimensions"""

        if (self.data is None) or (dimensions and dimensions
             not in self.columns):
            return None

        if dimensions:
            return self.data.loc[self.columns[dimensions]].to_series()

        return self.data.to_series()


class DataVensim(Data):

    """
    Class that holds the data to plot when loading Vensim outputs.
    """

    def __init__(self, filename, doc):
        super().__init__()
        self.filename = filename
        self.scenario = "Vensim output"
        self.doc = doc[["Py Name", "Real Name"]]
        self.namespace = {}
        self.variable_list, self.transpose = Columns.get_columns(self.filename)

    def set_var(self, var_name):
        """
        Set current variable and get it from file if necessary
        """
        self.current_var = var_name
        self.columns = None

        if self.current_var not in self.cached_values:
            if var_name in self.namespace:
                self.columns = Columns.get_columns(
                    self.filename,
                    [self.namespace[var_name]])[0]

                new_data = load_outputs(
                        self.filename, self.transpose, columns=self.columns)

                # remove nan from constant values
                nan_cols = np.isnan(new_data.iloc[1:, :]).all()
                new_data.loc[:, nan_cols] =\
                    new_data.loc[:, nan_cols].iloc[0].values

                self.data = self.data.join(new_data, how="outer")

            self._add_to_cache()

    @property
    def variable_list(self):
        """holds the sorted list of variables without dimensions"""
        return self._variable_list

    @variable_list.setter
    def variable_list(self, columns):
        """save only variable names not suscripts"""
        inverse_space = {
            original.replace("\"", ""): py_name
            for py_name, original in
            zip(self.doc["Py Name"], self.doc["Real Name"])
        }

        self.namespace = {}

        for column in columns:
            file_name = ("[".join(column.split("[")[:-1]) or column)
            sub_name = file_name.replace("\"", "")
            if sub_name in inverse_space:
                self.namespace[inverse_space[sub_name]] = file_name
            else:
                self.namespace[sub_name] = file_name

        self._variable_list = set(self.namespace)


class ScenarioDefWindow:

    def __init__(self):

        self._scenario_name = None
        self.initialize_window()
        self.scenario_name = self._scenario_name

    def initialize_window(self):
        # Create an instance of Tkinter frame
        self.master = Tk()
        self.master.geometry("250x250")
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.title("Write scenario name for unknown scenario")
        # Initialize a Label to display the User Input
        self.label1 = Label(self.master, text="No scenario name could be "
                           "retrieved from the loaded file. \n Please name "
                           "your scenario:\n\n")
        self.label1.pack()

        # Create an Entry widget to accept User Input
        self.entry = Entry(self.master, width= 40)
        self.entry.focus_set()
        self.entry.pack()

        self.label2 = Label(self.master, text="")
        self.label2.pack()

        # Create a Button to validate Entry Widget
        ttk.Button(self.master, text= "Set", width=20,
                   command=self.display_text).pack(pady=20)
        # Create a Button to validate Entry Widget
        ttk.Button(self.master, text= "Close", width=20,
                   command=self.close).pack(pady=20)

        self.master.mainloop()

    def display_text(self):
        self._scenario_name = self.entry.get()
        self.label2.config(text=f"Scenario name set to {self._scenario_name}, "
                           "click on the Close button to continue")

    def close(self):
        self.master.quit()
        self.master.destroy()
