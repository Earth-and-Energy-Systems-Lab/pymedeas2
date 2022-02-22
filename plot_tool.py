#!/usr/bin/python
# coding: utf-8
import sys
import warnings
import tkinter as tk
from tkinter.filedialog import askopenfilename

import json
from pathlib import Path
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pandas.core.indexing import IndexingError

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
     NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
import pysd

from pytools.config import read_config, read_model_config
from pytools.data_manager import DataContainer, DataFile, DataLoaded,\
                                 DataVensim

__author__ = "Eneko Martin, Emilio Ramon Garcia Ladona"
__maintainer__ = "Roger Samsó, Eneko Martin"
__status__ = "Development"


warnings.filterwarnings("ignore")


class PlotTool(tk.Frame):
    """
    Main plotting class with tkinter
    """

    markers = ["o", "v", "<", "^", "1", "s", "p", "P", "h", "X", "D"]
    line_styles = ['--', '-.', ':']

    def __init__(self, master, data=None, config=None, scenario="Current"):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.option_add('*tearOff', 'FALSE')  # menus no detaching
        self.master.title("pymedeas plotting tool")

        # current variable and data container
        self.column = ""
        self.data_container = DataContainer()
        self.title, self.units, self.description = "", None, None
        self.doc = None

        # attributes of the main window
        self.toolbar = None
        self.search_tit = None  # title of the search bar
        self.search_var = None  # gets the value input by user
        self.entry = None  # user input
        self.lstbox = None
        self.subplot = None     # axis canvas
        self.canvas = None  # canvas
        self.button = None  # button to clear data
        self.var_dim = []  # dimensions of the variable

        #  Data
        if data is not None:
            self.data_container.add(DataLoaded(scenario, data))
            self.all_vars = self.data_container.variable_list
        else:
            self.all_vars = []

        if not config:
            # Ask user for config
            self.get_config()
        else:
            self.configure_data(config)
            self.init_window()

    def configure_data(self, config):
        """Configure metadata for the variables and default folders"""
        # Default folder and variables
        self.results_folder = config.model.out_folder
        self.default_list = config.model.out_default

        # Get model information (documentation, units, namespace)
        model = pysd.load(config.model.model_file, initialize=False)
        self.doc = model.doc()
        self.doc["Clean Name"] = self.doc["Real Name"].apply(self.clean_name)

        # setting the default folder to store saved plots
        matplotlib.rcParams['savefig.directory'] = self.results_folder

    @staticmethod
    def clean_name(name):
        """Remove outside commas from variables"""
        if name.startswith('"') and name.endswith('"'):
            return name[1:-1]
        else:
            return name

    def get_config(self):
        """Popup window for selecting configuration"""
        with open("pytools/models.json") as mod_pars:
            model_pars = json.load(mod_pars)

        self.popup = tk.Toplevel()
        self.popup.wm_title("Select configuration")

        tk.Label(self.popup, text="Select origin model to load outputs").grid(
            column=0, row=0, padx=20, pady=20)

        self.config = tk.StringVar()
        tk.OptionMenu(self.popup, self.config, *model_pars.keys()).grid(
            column=0, row=1, padx=20, pady=10)

        tk.Button(self.popup, text="Continue", command=self.set_config).grid(
            column=0, row=2, padx=20, pady=10)

        self.master.update()

    def set_config(self):
        """Set model configuration from popup results"""
        if self.config.get():
            config = read_config()
            config.region = self.config.get()
            self.popup.destroy()
            self.configure_data(read_model_config(config))
            self.init_window()
        else:
            tk.messagebox.showwarning(
                title="Select configuration",
                message="Please select a configuration in the dropdown.")

    def init_window(self):
        """Main window"""
        self.pack(fill=tk.BOTH, expand=1)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Load data", command=self.load_file)
        filemenu.add_command(
            label="Load Vensim data",
            command=lambda: self.load_file(lambda x: DataVensim(x, self.doc)))
        filemenu.add_command(label="Clear data", command=self.clear_data)
        filemenu.add_command(label="Exit", command=lambda: on_closing(self))
        menubar.add_cascade(label="File", menu=filemenu)
        # TODO add help cascade and or about the models

        # Main window
        paned_win = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_win.pack(side="left", fill=tk.BOTH, expand=1)

        left_frame = tk.LabelFrame(
            paned_win, text='Variables', width=100, height=100)
        right_frame = tk.Frame(paned_win, width=100, height=100)

        paned_win.add(left_frame)
        paned_win.add(right_frame)

        # Left frames
        self.scenarios_frame = tk.Frame(left_frame)
        self.scenarios_frame.pack(side=tk.BOTTOM)

        search_frame = tk.Frame(left_frame)
        search_frame.pack(side=tk.TOP)

        right_scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lstbox = tk.Listbox(
            left_frame, yscrollcommand=right_scrollbar.set, width=80)
        self.lstbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        right_scrollbar.config(command=self.lstbox.yview)
        self.lstbox.bind('<<ListboxSelect>>', self.on_click)

        self.populate_list()

        self.search_tit = tk.Label(search_frame, text="Search")
        self.search_tit.pack(side=tk.LEFT, expand=0)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode:
                              self.update_list(self.all_vars))

        self.entry = tk.Entry(
            search_frame, textvariable=self.search_var, width=50)
        self.entry.pack(side=tk.LEFT, expand=0)

        # Right frames
        self.dimension_frame = tk.Frame(right_frame, width=100, height=30)
        self.dimension_frame.pack(side=tk.TOP)
        lower_right_frame = tk.Frame(right_frame, width=100, height=70)
        lower_right_frame.pack(side=tk.BOTTOM)

        # Plot frame
        fig = Figure(figsize=(200, 100))
        plt.rc('legend', fontsize='medium')
        self.subplot = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=lower_right_frame)

        self.toolbar = NavigationToolbar2Tk(self.canvas, lower_right_frame)
        self.canvas.get_tk_widget().pack()

        # info buttom for variable description
        info_icon = tk.PhotoImage(file='pytools/info-logo.png')
        info_icon = info_icon.subsample(8, 8)
        self.button = tk.Button(
            self.toolbar, image=info_icon, width=25, height=20,
            text="Show variable information",
            command=self.show_description)
        self.button.image = info_icon
        self.button.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.toolbar.update()
        self.canvas.draw()

    def dimension_dropdown(self, dimensions):
        """Create dimensions dropdowns"""
        tk.Label(self.dimension_frame, text="Dimensions").grid(
            row=0, column=0)

        self.var_dim = []
        for i, dims in enumerate(dimensions):
            # create variables and dropdowns
            self.var_dim.append(tk.StringVar())
            self.var_dim[i].trace(
                "w", lambda name, index, mode: self.draw_dimensions())
            op_menu = tk.OptionMenu(
                self.dimension_frame, self.var_dim[i], *dims)
            op_menu.grid(
                row=1+i, column=0, padx=5)

    def clear_frames(self):
        """Clear plot and dimensions frames"""
        # clear the plot
        self.subplot.clear()
        self.canvas.draw()
        for widgets in self.dimension_frame.winfo_children():
            # remove dimensions widgets
            widgets.destroy()
        self.dimension_frame.config(height=0)  # update height

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

    def clear_data(self):
        """Clear plot displayed and imported data"""
        self.clear_frames()
        self.data_container.clear()
        self.lstbox.delete(0, last=len(self.all_vars))

    def load_file(self, DataType=DataFile):
        """Create Data object with columns information"""
        filename = Path(askopenfilename(
            initialdir=self.results_folder,
            title="Open file",
            filetypes=(
                ("csv, tab files", "*.csv *.tab"),
                ("csv files", "*.csv"),
                ("tab files", "*.tab"),
                ("All files", "*")
            )
        ) or "")

        if not filename.name:
            pass
        elif filename.suffix in [".csv", ".tab"]:
            self.data_container.add(DataType(filename))
            self.all_vars = self.data_container.variable_list
            self.populate_list()
            if self.column:
                # update plots when loading new data
                self.select_variable()
        else:
            tk.messagebox.showerror(
                title="Incompatible file format",
                message=f"Incompatible file format '{filename}'.\n"
                        "Compatible file formats are '.csv' and '.tab'")

    def on_click(self, event):
        """Select a variable"""
        try:
            index = event.widget.curselection()[0]
        except (IndexingError, IndexError):
            pass
        else:
            self.column = event.widget.get(index)
            self.select_variable()

    def show_description(self):
        """Show current variable description if available"""
        if not self.description:
            tk.messagebox.showwarning(
                title=self.title, message="No description available...")
        else:
            tk.messagebox.showinfo(
                title=self.title, message=self.description)

    def set_variable_info(self):
        """Set variable info from model documentation"""
        index = self.doc["Py Name"] == self.column
        if any(index):
            # set the metadata using model doc
            self.title = self.doc[index]["Clean Name"].iloc[0]
            self.units = self.doc[index]["Unit"].iloc[0]
            self.description = self.doc[index]["Comment"].iloc[0]
        else:
            # if the variable comes from another version we may not have
            # information in the doc
            self.title = self.column
            self.units = ""
            self.description = None

        self.plot_info()

    def select_variable(self):
        """Load the selected variable information and add dropdowns"""
        # Set the current var in the objects to the selected one
        self.clear_frames()
        self.data_container.set_var(self.column)
        self.set_variable_info()

        if self.data_container.dimensions is None:
            self.draw(self.data_container.get_values(None))
        else:
            self.dimension_dropdown(self.data_container.dimensions)

    def draw_dimensions(self):
        """Draw the plot when changing dimensions"""
        dimensions = tuple(var.get() for var in self.var_dim)
        if all(dimensions):
            self.draw(self.data_container.get_values(dimensions))

    def draw(self, values):
        """Draw the plot of the selected variable"""
        self.plot_info()
        historical = False
        historic_year = 2014
        markers = cycle(PlotTool.markers)
        n_sim = len(self.data_container)
        markersizes = cycle(np.linspace(7, 4, n_sim))
        k = -1

        for scenario, results in values.items():
            k += 1
            marker = next(markers)  # updates the line marker
            markersize = next(markersizes)

            if results is None:
                continue

            if not historical and any(results.index < historic_year):

                self.subplot.plot(results.loc[:historic_year],
                                  label='Historical',
                                  color='black')
                historical = True

            self.subplot.plot(results.loc[historic_year:],
                              marker=marker, markersize=markersize,
                              markevery=(k, n_sim),
                              label=scenario, alpha=0.8)

        self.subplot.legend()
        self.canvas.draw()

    def plot_info(self):
        """Include plot info, variable title and units"""
        self.subplot.clear()
        # image name will be named after the plotted variable name
        self.canvas.get_default_filename = lambda: self.column

        self.subplot.set_title(self.title)
        self.subplot.xaxis.set_minor_locator(MultipleLocator(5))
        self.subplot.set_xlabel('Year')
        self.subplot.grid(which='major')
        self.subplot.grid(which='minor', linestyle=':', alpha=0.5)

        if self.units:
            self.subplot.set_ylabel(self.units, rotation='vertical')

        self.canvas.draw()


def on_closing(root):
    """Behaviour when the window is closed"""
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    root.destroy()
    sys.exit()


def main(config=None, data=None, scenario=None):
    """
    Main loop
    """
    if __name__ == "__main__":
        root = tk.Tk()
    else:
        root = tk.Toplevel()

    root.geometry("1200x600")
    PlotTool(root, data=data, config=config, scenario=scenario)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()


if __name__ == '__main__':

    # load configuration file
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        config = read_config()
        config.region = sys.argv[1]
        main(read_model_config(config))
    else:
        raise ValueError(
            "python plot_tool.py only accepts 1 argument, corresponding"
            " to the region (e.g.: python plot_tool.py pymedeas_eu)")
