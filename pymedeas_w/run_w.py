import pysd
from pysd import test_utils
import pandas as pd
import warnings
warnings.simplefilter('ignore')

canon = test_utils.load_canon('default_out.tab')

model = pysd.load('medeas_w.py', initialize=False)
out = model.run(progress=True, return_columns=canon.columns)
out.to_csv("python_out.tab", sep="\t")

#out = pd.read_table('python_out.tab', index_col=0)
test_utils.assert_frames_close(out, canon, precision=4, assertion="warn")
