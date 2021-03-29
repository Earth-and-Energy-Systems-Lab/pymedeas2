import re
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import getopt

from plotting import ROOT_DIR

#######################################

# constants
vensim_data_folder = 'vensim_data'
vensim_data_file = 'data.csv'
scenarios = ['BAU', 'SCEN1', 'SCEN2', 'SCEN3', 'SCEN4', 'User defined']
used_scenarios = ['BAU']
not_used_scenarios = set(scenarios) - set(used_scenarios)
omitted_column_substrings = ['check', 'ifthenelse']


# default plotting parameters
to_plot = True
verbose = False
ratio_year = 2020
plot_against_vensim = False
step = 0.125
debug = False

# get command line parameters: 
# -h (help), -r <year> (ratio instead of year), -v (verbose)
try:
    opts, args = getopt.getopt(sys.argv[1:],"hvdr:")

    for opt, arg in opts:
        if opt == '-h':
            print('plot.py -r <year>(ratio comparison, no plot) -v (verbose)')
            sys.exit()
        elif opt in ("-r", "--ratio"):
            to_plot = False
            ratio_year = float(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-d", "--debug"):
            debug = True
except getopt.GetoptError:
    print('default config')
if not to_plot:
    print('comparison mode at year ', ratio_year)
    print('------------------------------')


def replace_let_by_x(stri):
    for let in '\"\'-+\%?&\/=\(\)':
        stri = stri.replace(let, 'x')
    return stri
# generate funcname: (unit, legend) dictionary from file
legend_by_name = {}
try:
    with open(os.path.join(ROOT_DIR, 'legend_by_name.txt'), 'r', encoding='utf-8') as f:
        legend_by_name_list = f.readlines()
    for line in legend_by_name_list:
        funcname, unit, legend = [x.strip() for x in line.split('@@')]
        legend_by_name[funcname] = (unit, legend)
except:
    print('legend_by_name.txt cannot be read correctly\n No legends and units generated')
    raise 

#inp = input(legend_by_name)

if plot_against_vensim:
    vensim_dict = {}
    with open(os.path.join(vensim_data_folder, vensim_data_file), 'r') as f:
        vensim_data_file_text = f.read()
        lines = []
        for line in vensim_data_file_text.splitlines():
            if not any(x in line for x in not_used_scenarios):
                lines.append(line)
        vensim_data_file_text = '\n'.join(lines)

        for scenario in scenarios:
            vensim_data_file_text = vensim_data_file_text.replace(scenario + ',', '').replace(',' + scenario, '').replace('[' + scenario + ']', '')

        pattern = re.compile(r",([^-\d,])")
        vensim_data_file_text = re.sub(pattern, r";\1", vensim_data_file_text)

        for line in vensim_data_file_text.splitlines():
            elems = line.split(',')
            try:
                dummy = float(elems[1])
                elems[0] = elems[0].lower().strip()
                elems[0] = replace_let_by_x(elems[0])
                indices = elems[0].split('[')
                index = indices[0].replace(' ', '_')
                index += '[' + indices[1] if len(indices) > 1 else ''

                vensim_dict[index] = np.array([float(x) for x in elems[1:]])
            except ValueError:
                if verbose:
                    print('... line <{}> not recognized, first data element: <{}>'.format(line, elems[1]))
            except IndexError:
                if verbose:
                    print('... line <{}> gets no first element, zero data element: <{}>'.format(line, elems[0]))

py_dict = {}
scenario_info = 'no scenario info'
time_step_info = 'no time step info'
with open('results.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        if not line.startswith('#'):  
            s = line.split('\t')
            try:
                first_value = float(s[1])
                py_index = replace_let_by_x(s[0].strip().lower())
                py_index1 = py_index.split('[')
                py_index1[0] = py_index1[0].replace(' ', '_')
                py_index = '['.join(py_index1)
                py_dict[py_index] = np.array([float(x) for x in s[1:]])
            except:
                continue
        else:
            data_info = line[1:].split(',')
            scenario_info, time_step_info = data_info[0:2]
    else:
        time_points = len(py_dict[py_index])

py_dict1 = {}
scenario_info1 = 'no scenario info'
time_step_info1 = 'no time step info'
try:
    with open('results_old.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if not line.startswith('#'):  
                s = line.split('\t')
                try:
                    first_value = float(s[1])
                    py_index = replace_let_by_x(s[0].strip().lower())
                    py_index1 = py_index.split('[')
                    py_index1[0] = py_index1[0].replace(' ', '_')
                    py_index = '['.join(py_index1)
                    py_dict1[py_index] = np.array([float(x) for x in s[1:]])
                except:
                    continue
            else:
                data_info1 = line[1:].split(',')
                scenario_info1, time_step_info1 = data_info1[0:2] 

        else:
            time_points1 = len(py_dict1[py_index])
            no_2nd_dataset = False
except:
    print('Dataset results_old.txt not found')
    no_2nd_dataset = True
silent = False

stx, time_step = np.linspace(start=1995, stop=2050, endpoint=True, retstep=True, num=time_points)
if not no_2nd_dataset:
    stx1, time_step1 = np.linspace(start=1995, stop=2050, endpoint=True, retstep=True, num=time_points1)

print('Dataset0 simulation with time step=', time_step)
if not no_2nd_dataset:
    print('Dataset1 simulation with time step=', time_step1)


def criterion(a, b):
    return 0. if b == 0. else (a/b-1.)

# debugging x-set
x1 = np.linspace(1995, 2050, 40, endpoint=True)

# print ratio vector (should be around 1 in all components)
#print('Flush comparison data for vensim and python results? [y/n]')
while True:
    #inp = input('>').lower().strip()   #uncomment this to invoke 
    inp = 'n'
    if inp == 'y':
        for column, vensim_data in vensim_dict.items():
            if column.startswith('ifthenelse'):
                try:
                    py_data = py_dict[column]
                    leng = len(py_data)
                    if len(vensim_data) == 1:
                        vensim_data = np.array(list(vensim_data)*leng)
                    #ratio = np.array([y/x if x != 0 else 1 for x, y in zip(py_data, vensim_data)])
                    ratio = [int(x-y) for x, y in zip(py_data, vensim_data)]
                    if 1 in ratio and ratio.index(1) < 10:
                        print(column, '\n', ratio, '\n---------')
                    elif -1 in ratio and ratio.index(-1) < 10:
                        print(column, '\n', ratio, '\n---------')
                except KeyError:
                    continue
        else:
            break
    elif inp == 'n':
        break
    else:
        print('Command not recognized, try again...')


# plot two graphs in the same window
def two_scales(ax1, time, data1, data2, c1, c2):
    """

    Parameters
    ----------
    ax : axis
        Axis to put two scales on

    time : array-like
        x-axis values for both datasets

    data1: array-like
        Data for left hand scale

    data2 : array-like
        Data for right hand scale

    c1 : color
        Color for line 1

    c2 : color
        Color for line 2

    Returns
    -------
    ax : axis
        Original axis
    ax2 : axis
        New twin axis
    """
    ax2 = ax1.twinx()

    ax1.plot(time, data1, color=c1)
    ax1.set_xlabel('time (year)')
    ax1.set_ylabel('ratio')

    ax2.plot(time, data2, color=c2)
    ax2.set_ylabel('py data')
    return ax1, ax2


# Change color of each axis
def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None


dict_correct = {'year':'Year', 'ej':'EJ', 'tw':'TW', 'mdollar':'M Dollar', 'pj':'PJ', 'gj':'GJ', 'beTWeen':'between', 'DegreesC': u'Temperature (\u00B0C)'}


def define_units(varname):
    def adjust_format(name):
        for wrong in dict_correct:
            name = name.replace(wrong, dict_correct[wrong])
        return name.replace('Dmnl', 'Dimensionless')
    dicti = {'ej':'EJ', 'mtoe':'mtoe', 'tw':'TW', 'twh':'TWh', 'mt':'Mt', 'DegreesC': u'Temperature (\u00B0C)'}
    clean_name = varname.split('[')[0].strip(' x')
    ret = None
    for unit in dicti:
        if clean_name.endswith(unit):
            ret = dicti[unit]
            break
    else:
        for name in legend_by_name:
            if varname.startswith(name):
                ret = adjust_format(legend_by_name[name][0])
    return ret


def define_legend(varname):
    # specific update of the legend
    def adjust_format(name):
        for wrong in dict_correct:
            name = name.replace(wrong, dict_correct[wrong])
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
        for name in legend_by_name:
            if varname.startswith(name):
                ret = adjust_format(legend_by_name[name][1].split('[')[0].split('(')[0])
    return ret


if plot_against_vensim:
    inp = input('Check if vensim_data folder contains data.csv with Vensim data. Press any key to continue...')
else:
    datalogs = []
    for file in os.listdir():
        if file.startswith("results.txt"):
            datalogs.append(file)    
print('Plotting:\n---------\n 1) enter values (ex.: v1, v2) with index, if necessary (ex.: v1[its_index])\n 2) a for all\n 3) #val for exact match\n 4) e to exit:')
while True:
    inp = input('>').lower().strip()
    if inp == 'e':
        break
    elif inp == 'a':
        columns = py_dict
    elif inp == '':
        continue
    else:
        columns_input = [x.strip() for x in inp.split(',')]
        columns_input = [x.split('[')[0].replace(' ', '_') + '[' + x.split('[')[1] if len(x.split('[')) > 1 else x.replace(' ', '_') for x in columns_input]
        columns = []
        for column in columns_input:
            if column.startswith('#') and column[1:].strip() in list(py_dict.keys()):
                columns.append(column[1:].strip())
                continue
            for py_column in py_dict:
                if column in py_column:
                    columns.append(py_column)
        if len(columns) == 0:
            print('not found, try again...')
            continue
    for column in columns:
        # debug variables
        if not debug and any(substring in column for substring in omitted_column_substrings):# or column.startswith('check'):
            continue

        try:
            py_data = py_dict[column]
            if not no_2nd_dataset:
                py_data1 = py_dict1[column]            
            if plot_against_vensim:
                vensim_data = vensim_dict[column]
        except KeyError:
            if verbose:
                print('... not found: {} in py_data'.format(column))
            continue

        if to_plot:
            leng = len(py_data)
            if plot_against_vensim and len(vensim_data) == 1:
                vensim_data = np.array(list(vensim_data)*leng)
            #ratio = np.array([y/x if x != 0 else 1 for x, y in zip(py_data, vensim_data)])
                ratio = np.array([y-x for x, y in zip(py_data, vensim_data)])            
                print(column + ' : ' + str(ratio[0]))
            
            if plot_against_vensim:
                # Create axes
                fig, ax = plt.subplots()        
                ax1, ax2 = two_scales(ax, stx, py_data, vensim_data, 'r', 'b')
                color_y_axis(ax1, 'r')
                color_y_axis(ax2, 'b')
            else:
                if not no_2nd_dataset:
                    plt.plot(stx, py_data, stx1, py_data1)
                    plt.legend((scenario_info+', '+time_step_info, scenario_info1+', '+time_step_info1))
                else:
                    plt.plot(stx, py_data)
            plt.xlabel('Year')            
            ylabel = define_units(column)
            if ylabel:
                plt.ylabel(ylabel, rotation='vertical')
            print('column ', column, flush=True)
            title = define_legend(column)
            title = title + '\n' + column if title else column
            plt.title(title)
            #plt.title('sometitle\nother line')

            plt.show()
            #fig.canvas.draw()
            print('    Press any key to see the next or e to end')
            inp = input('    >>')
            plt.close()                
            if inp.strip() == 'e':
                break
        else:
            time_stamp = int((ratio_year-1995)/0.125)
            if len(vensim_data) > 2:
                ratio_0 = py_data[time_stamp] - vensim_data[time_stamp] if vensim_data[time_stamp] != 0 else 1
                if abs(ratio_0 - 1) > 4e-2:
                    inp = input('Found incorrect starting value in column : {} : {}'.format(column, ratio_0))


