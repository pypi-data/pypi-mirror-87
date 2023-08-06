![LF Logo](lf_logo.png)

# LF Data

This project provides a set of useful tools for interacting with data taken from
the LF AWESOME receivers maintained by the LF Radio Lab at Georgia Tech. This
data is available publicly at [Waldo World](https://waldo.world/). 

## Installation

Run the following to install:

```python
pip install lf
```

## Example Usage

```python
import lf

# Load an entire .mat file
data = lf.data.rx.load_rx_data("path_to_mat_file")

# Load a specific variable or set of variables
variables = ["station_name", "call_sign", "data"]
data = lf.data.rx.load_rx_data("path_to_mat_file", variables)

# Create an LFData object from two mat files or dictionaries
mat_files = ["amplitudeNS.mat", "phaseNS.mat", "amplitudeEW.mat", "phaseEW.mat"]
data = lf.data.rx.LFData(mat_files)

# Evaluate the quality of your data with the EvalLF object
data_eval = lf.data.rxquality.EvalLF(data)
```
