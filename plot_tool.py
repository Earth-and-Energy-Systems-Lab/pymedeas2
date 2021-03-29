#!/usr/bin/python
# coding: utf-8

__author__ = "Emilio Ramon Garcia Ladona"
__maintainer__ = "Roger Samsó"
__status__ = "Development"


"""
This tool allows plotting the model simulation results. When running run.py with
the option -p, it shows up at the end of the simulation and displays the simulation
results. It can also run independently, in which case the results must be imported
from a csv file. In both cases, only two curves can be represetnted at the same
time.
"""

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename
from tkinter import messagebox, Button
import numpy as np
import os
from configparser import ConfigParser
import re
from itertools import cycle

import pandas as pd
import tkinter as tk
import sys
import warnings
warnings.filterwarnings("ignore")


class Plot_tool(tk.Frame):

    last_col = ''

    # default list of variables
    default_list = list(sorted(
        ['tpe_from_res_ej',  # total primary energy supply from RES (MToe/Year)
         'total_extraction_nre_ej',
         # Annual total extraction of non-renewable energy resources (EJ/Year)
         'percent_res_vs_tpes',
         # Percent of primary energy from RES in the TPES (%)
         'temperature_change',
         # Temperature of the Atmosphere and Upper Ocean, relative to preindustrial reference period (degreesC)
         'total_land_requirements_renew_mha',
         # Land required for RES power plants and total bioenergy (land competition + marginal lands (MHa)
         'share_blue_water_use_vs_ar',
         # Share of blue water used vs accessible runoff water (Dmnl)
         'gdppc',  # GDP per capita (1995T$ per capita) ($/people)
         'eroist_system',  # EROI standard of the system (Dmnl)
         'tfes_intensity_ej_tdollar',  # Total final energy intensity (EJ/T$)
         'real_tfec',  # Real total final energy consumption (EJ)
         'gdp',  # Global GDP in T1995T$ (T$)
         'population',  # Population projection (people)
         'total_co2_emissions_gtco2'
         ]))

    markers = ["o", "v", "<", "^", "1", "s", "p", "P", "h", "X", "D"]

    def __init__(self, master, data=None, results_folder=None, scenario=''):
        tk.Frame.__init__(self, master)  # esto define self.master
        self.master = master
        self.master.option_add('*tearOff', 'FALSE')  # menus no detaching
        self.master.title("MEDEAS Plotting tool")
        self.results_folder = results_folder
        self.column = ''
        self.data_container = []  # list that will contain all data objects
        self.scenario = scenario

        # attributes of the window
        self.toolbar = None
        self.search_tit = None  # title of the search bar
        self.search_var = None  # gets the value input by user
        self.entry = None  # user input
        self.lstbox = None
        self.subplot = None     # axis canvas
        self.canvas = None  # canvas
        self.button = None  # button to clear data

        # setting the default folder to store saved plots
        matplotlib.rcParams['savefig.directory'] = self.results_folder

        #  Data
        if data is not None:
            pdDF = Data(self.scenario, dataframe=data)
            self.data_container.append(pdDF)
            self.all_vars = [var for var in self.default_list if var in pdDF.df.columns] + ['--------'] + pdDF.variables_list
        else:
            self.all_vars = []

        # generate funcname: (unit, legend) dictionary from file
        self.legend_by_name = {}

        try:
            with open(os.path.join('plotting', 'legend_by_name.txt'), 'r', encoding='utf-8') as f:
                legend_by_name_list = f.readlines()
        except:
            print('legend_by_name.txt cannot be read correctly\n No legends and'
                  ' units generated')
        else:
            for line in legend_by_name_list:
                funcname, unit, legend = [x.strip() for x in line.split('@@')]
                self.legend_by_name[funcname] = (unit, legend)

        self.init_window()

    def init_window(self):
                
        self.pack(fill=tk.BOTH, expand=1)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Load data", command=self.open_file)
        filemenu.add_command(label="Exit", command=lambda: on_closing(self))
        menubar.add_cascade(label="File", menu=filemenu)

        p = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        p.pack(side="left", fill=tk.BOTH, expand=1)

        f1 = tk.LabelFrame(p, text='Variables', width=100, height=100)
        f2 = tk.Frame(p, width=100, height=100)

        p.add(f1)
        p.add(f2)

        f3 = tk.Frame(f1)
        f3.pack(side=tk.TOP)

        right_scrollbar = tk.Scrollbar(f1, orient=tk.VERTICAL)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lstbox = tk.Listbox(f1, yscrollcommand=right_scrollbar.set, width=80)
        self.lstbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        right_scrollbar.config(command=self.lstbox.yview)
        self.lstbox.bind('<<ListboxSelect>>', self.on_click)

        self.populate_list()

        self.search_tit = tk.Label(f3, text="Search")
        self.search_tit.pack(side=tk.LEFT, expand=0)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list(self.all_vars))

        self.entry = tk.Entry(f3, textvariable=self.search_var, width=50)
        self.entry.pack(side=tk.LEFT, expand=0)

        fig = Figure(figsize=(200, 100))
        plt.rc('legend', fontsize='medium')
        self.subplot = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=f2)

        self.toolbar = NavigationToolbar2Tk(self.canvas, f2)
        self.canvas.get_tk_widget().pack()

        self.button = Button(self.toolbar, text="Clear data", command=self.clear_plots)
        self.button.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.toolbar.update()
        self.canvas.draw()

    def populate_list(self):
        """
        populating the list with variable names
        """
        for item in self.all_vars:
            self.lstbox.insert(tk.END, item)

    def update_list(self, list_):
        """
        Updates the list of variables in lstbox based on the user input
        :param list_:
        :return:
        """
        search_term = self.search_var.get()

        # populate the listbox with default values
        lbox_list = list_

        self.lstbox.delete(0, tk.END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.lstbox.insert(tk.END, item)

    def clear_plots(self):
        """Clear plot displayed and imported data"""
        self.subplot.clear()
        self.canvas.draw()
        self.data_container = []
        self.scenario = ''
        self.lstbox.delete(0, last=len(self.all_vars))

    @staticmethod
    def replace_let_by_x(stri):
        for let in '\"\'-+\%?&\/=\(\)': stri = stri.replace(let, 'x')
        return stri
        
    def open_file(self):
        ext = (("csv", "*.*csv"), ("all files", "*.*"))
        filename = askopenfilename(initialdir="./", title="Open file", filetypes=ext)

        if filename.split('.')[-1] == "csv":
            datafile = Data(self.config, filename=filename)
            self.data_container.append(datafile)
            if len(self.data_container) < 2:
                self.all_vars = [var for var in self.default_list if
                                 var in datafile.df.columns] + [
                                    '--------'] + datafile.variables_list
                self.populate_list()
        else:
            print("Incompatible file format. Compatible file formats are 'csv' "
                  "and... 'csv' (for now)")

    dict_correct = {
        'year': 'Year',
        'ej': 'EJ',
        'tw': 'TW',
        'mdollar': 'M Dollar',
        'pj': 'PJ', 'gj': 'GJ',
        'beTWeen': 'between',
        'DegreesC': u'Temperature (\u00B0C)',
        'degrees Celsius': u'\u00B0C',
        'degree C': u'\u00B0C',
        'degrees C': u'\u00B0C',
        'yr': 'Year',
        'Dmnl': 'Dimensionless'
        }

    def define_units(self, varname):
        def adjust_format(name):
            for wrong in self.dict_correct:
                name = name.replace(wrong, self.dict_correct[wrong])
            return name
        dicti = {'ej': 'EJ', 'mtoe': 'mtoe', 'tw': 'TW', 'twh': 'TWh', 'mt': 'Mt', 'DegreesC': u'Temperature (\u00B0C)'}
        clean_name = varname.split('[')[0].strip(' x')
        ret = None
        for unit in dicti:
            if clean_name.endswith(unit):
                ret = dicti[unit]
                break
        else:
            for name in self.legend_by_name:
                if varname.startswith(name):
                    ret = adjust_format(self.legend_by_name[name][0])
        return ret

    def define_title(self, varname):
        # specific update of the legend
        def adjust_format(name):
            for wrong in self.dict_correct:
                name = name.replace(wrong, self.dict_correct[wrong])
            name = name.replace('\\', '\n').replace('\t', ' ')
            return name.split('.')[0].strip()
        dicti = {}
        clean_name = varname.split('[')[0].strip(' x')
        ret = ''
        for unit in dicti:
            if clean_name.startswith(unit):
                ret = dicti[unit]
                break
        else:
            for name in self.legend_by_name:
                if varname.startswith(name):
                    ret = adjust_format(self.legend_by_name[name][1].split('[')[0]) #.split('(')[0])
        return ret

    def on_click(self, event):

        w = event.widget
        try:
            index = w.curselection()[0]
        except:
            self.column = Plot_tool.last_col
        else:
            self.column = w.get(index)
            Plot_tool.last_col = self.column

        self.draw()

    def draw(self):

        self.subplot.clear()
        self.canvas.draw()
        
        # image name will be named after the plotted variable name
        self.canvas.get_default_filename = lambda: self.column 

        title = self.define_title(self.column)
        title = title + '\n({})'.format(self.column) if title else self.column
        self.subplot.set_title(title)
        self.subplot.set_xlabel('Year')

        ylabel = self.define_units(self.column)

        if ylabel:
            self.subplot.set_ylabel(ylabel, rotation='vertical')

        mark = cycle(Plot_tool.markers)

        if not self.column.lower().startswith('-'):

            for obj in self.data_container:
                m = next(mark)  # updates the line marker
                nt = len(np.where(obj.time_updated < 2014)[0])

                try:
                    self.subplot.plot(obj.time_updated[0:nt], obj.py_dict[self.column][0:nt], marker=m, markersize=3, label='Historical ' + obj.scenario)
                    self.subplot.plot(obj.time_updated[nt - 1:], obj.py_dict[self.column][nt - 1:], marker=m, markersize=5, label='Projected ' + obj.scenario)
                except KeyError:
                    print('No data available for {}'.format(self.column))
                else:
                    print('Plotting ' + self.column)

                self.subplot.legend()
                self.canvas.draw()


def on_closing(root):
    """behaviour when the window is closed"""
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()
    sys.exit()


class Data:

    """class that holds the data to be plotted. It can either be loaded from
    a csv or from a pandas DataFrame"""

    def __init__(self, scenario='', filename=None, dataframe=None):

        self.filename = filename
        self.df = dataframe

        # these attributes will be used by the Plot_tool
        self.time_updated = []
        self.py_dict = {}
        self.variables_list = []

        if self.filename and not isinstance(self.df, pd.DataFrame):
            self._load_data_file()

        if isinstance(self.df, pd.DataFrame) and not self.filename:
            self.scenario = scenario.capitalize()
            self._df_to_dict()

        print('Data loaded for scenario {}'.format(self.scenario))

        self.variables_list = [var for var in sorted(self.df.columns) if
                               var not in Plot_tool.default_list]

    def _load_data_file(self):
        """loads data from a csv file"""

        print("Reading csv file {}".format(self.filename))
        self.df = pd.read_csv(self.filename, index_col=0).T
        self.df.index = pd.to_numeric(self.df.index)
        pattern = re.compile(r'results_(.*)(?=_[\d]{4}_[\d]{4}_[\d.]*(_old)*.csv)', re.I)
        try:
            scen_name = pattern.match(os.path.basename(self.filename)).group(1)
        except:
            print("To be able to import the scenario name, the output file "
                      "name should be the default one (e.g. results_ScenName_"
                      "InitDate_FinalDate_TimeStep.csv)")
            scen_name = input('Unknown Scenario. Please provide a name for the imported scenario: ')
            if scen_name == "":
                scen_name = 'Unknown Scenario'

        self.py_dict = self.df.to_dict(orient='list')
        self.time_updated = self.df.index.values
        self.scenario = scen_name.capitalize()

    def _df_to_dict(self):
        """convert a pandas dataframe to a dictionary"""
        self.py_dict = self.df.to_dict(orient='list')
        self.time_updated = self.df.index.values


def main(folder, df, scenario=''):

    if __name__ == '__main__':
        root = tk.Tk()
    else:
        root = tk.Toplevel()

    root.geometry("1200x600")
    Plot_tool(root, data=df, results_folder=folder, scenario=scenario)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()


if __name__ == '__main__':

    # load configuration file
    conf = ConfigParser()
    conf.read('config.ini')

    region = conf.get('inputs', 'MODEL')
    path_to_results = os.path.join(os.path.dirname(os.path.abspath(__file__)), region)

    main(path_to_results, None)


