import pysd
import warnings
warnings.simplefilter('ignore')

model = pysd.load('medeas_eu.py', initialize=False)
out = model.run(progress=True)
