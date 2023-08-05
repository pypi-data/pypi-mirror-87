# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imucal']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0', 'pandas>=1.1.3,<2.0.0']

extras_require = \
{'calplot': ['matplotlib>=3.3.2,<4.0.0'], 'h5py': ['h5py>=2.10.0,<3.0.0']}

setup_kwargs = {
    'name': 'imucal',
    'version': '1.0.1',
    'description': 'A Python library to calibrate 6 DOF IMUs',
    'long_description': "# IMU Calibration\n\nThis package provides methods to calculate and apply calibrations for IMUs based on multiple different methods.\n\nSo far supported are:\n\n- Ferraris Calibration (Ferraris1995)\n- Ferraris Calibration using a Turntable\n\n## Installation\n\n```\npip install imucal\n```\n\nTo use the included calibration GUI you also need matplotlib (version >2.2).\nYou can install it using:\n\n```\npip install imucal[calplot]\n```\n\n## Calibrations\n\n### Ferraris\n\nThis package implements the IMU-infield calibration based on Ferraris1995.\nThis calibration methods requires the IMU data from 6 static positions (3 axis parallel and antiparallel to gravitation vector) and 3 rotations around the 3 main axis.\nIn this implementation these parts are referred to as follows `{acc,gry}_{x,y,z}_{p,a}` for the static regions and `{acc,gry}_{x,y,z}_rot` for the rotations.\nAs example, `acc_y_a` would be the 3D-acceleration data measured during a static phase, where the **y-axis** was oriented **antiparallel** to the gravitation.\n\n#### Creating a new Calibration Object\n\nIf the data of all of these sections is already available separately as numpy arrays of the shape `(n x 3)`, where `n` is the number of samples in each section, they can be directly used to initialize a Calibration object:\n\n```python\nfrom imucal import FerrarisCalibration\n\nsampling_rate = 100 #Hz \ncal = FerrarisCalibration(sampling_rate=sampling_rate,\n                          acc_x_p=data_acc_x_p,\n                          ...,\n                          gyr_z_rot=data_gyr_x_rot)\n```\nor via class variables:\n```python\nfrom imucal import FerrarisCalibration\n\nsampling_rate = 100 #Hz \ncal = FerrarisCalibration(sampling_rate=sampling_rate)\ncal.gyr_z_a = data_gyr_z_a\n...\n```\n\nIf the data was recorded as a single continuous stream, we first need to identify the different regions in the data.\nThe `from_interactive_plot` method can be used to extract them manually using a GUI.\nFor this and for most other methods, we expect the data to be a `pd.DataFrame` with the columns `'acc_x', 'acc_y', 'acc_z, 'gyr_x', 'gyr_y', 'gyr_z'`, where each column represents the datastream of one sensor axis.\n\nNote: The expected column names can be overwritten\n\n```python\nfrom imucal import FerrarisCalibration\n\nsampling_rate = 100 #Hz \n# This will open an interactive plot, where you can select the start and the stop sample of each region\ncal, section_list = FerrarisCalibration.from_interactive_plot(data, sampling_rate=sampling_rate)\n\nsection_list.to_csv('./calibration_sections.csv')  # This is optional, but recommended\n```\n\nThis method also returns the `section_list` in addition to the Calibration object.\nIt is advised to save this list, as it can be used recreate the Calibration without performing the manual selection of the regions again:\n\n```python\n# At some other day:\nfrom imucal import FerrarisCalibration\nimport pandas as pd\n\nsection_list = pd.read_csv('./calibration_sections.csv', index_col=0)\nsampling_rate = 100 #Hz \n# This will recreate the calibration\ncal = FerrarisCalibration.from_section_list(data, section_list, sampling_rate=sampling_rate)\n```\n\n#### Performing the Calibration\n\nWhen the calibration object was successful initialized, you can obtain the calibration by simply calling `compute_calibration_matrix`:\n\n```python\ncal_mat = cal.compute_calibration_matrix()\nprint(cal_mat)\n```\n\nThis will return an `FerrarisCalibrationInfo` object, which holds all required calibration information.\nThis object can be saved and loaded to and from `hdf5` and `json` using the respective methods:\n\n```python\ncal_mat.to_json_file('./calibration.json')\n# some other day:\nfrom imucal import FerrarisCalibrationInfo\n\ncal_mat = FerrarisCalibrationInfo.from_json_file('./calibration.json') \n```\n\n```python\ncal_mat.to_hdf5('./calibration.h5')\n# some other day:\nfrom imucal import FerrarisCalibrationInfo\n\ncal_mat = FerrarisCalibrationInfo.from_hdf5('./calibration.h5') \n```\n\n#### Applying the Calibration\n\nThe `FerrarisCalibrationInfo` object can be used to apply the Calibration to new data from the same sensor:\n\n```python\ncalibrated_acc, calibrated_gyro = cal_mat.calibrate(acc, gyro)\n```\n\n`acc` and `gyro` are expected to be numpy arrays in the shape (n x 3)\n\n\n### Turntable Calibration\n\nThe turntable calibration uses some sort of instumeted turntable to perform the orientation changes and rotations for the Ferraris calibration.\nIt is fundamentally identical to the simple Ferraris calibration, however to indicate the expected difference in precision, this calibration method is implemented as seperate classes.\nThe interface is identical to the Ferraris calibration and all methods shown above can be used.\n\n**Note**: By default the Turntable calibration expects 720 deg rotations instead of 360 deg\n\n```python\n# obtain the calibration\nfrom imucal import TurntableCalibration\n\nsampling_rate = 100 #Hz \n# This will open an interactive plot, where you can select the start and the stop sample of each region\ncal, section_list = TurntableCalibration.from_interactive_plot(data, sampling_rate=sampling_rate)\ncal_mat = cal.compute_calibration_matrix()\ncal_mat.to_json_file('./calibration.json')\n\n# Apply the calibration\nfrom imucal import TurntableCalibrationInfo\n\ncal_mat = TurntableCalibrationInfo.from_json_file('./calibration.json') \n\ncalibrated_acc, calibrated_gyro = cal_mat.calibrate(acc, gyro)\n```",
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/imucal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
