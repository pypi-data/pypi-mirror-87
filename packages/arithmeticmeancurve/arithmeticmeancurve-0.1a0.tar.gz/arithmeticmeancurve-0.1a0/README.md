# arithmeticmeancurve

Calculates arithmetic mean curves for a sample of curves. Speciality of this
module is the extrapolation of the sample curves by the algorithm described in
"David Scheliga: Experimentelle Untersuchung des Rissausbreitungsverhaltens von
 nanopartikelverstärktem Polyamid 6. 2013"

![arithmeticmeancurve-icon](https://arithmeticmeancurve.readthedocs.io/en/latest/_images/arithmeticmeancurve-icon.svg)

## Installation

```` shell script
    $ pip install arithmeticmeancurve
````

If available the latest development state can be installed from gitlab.

```` shell script
    $ pip install git+https://gitlab.com/david.scheliga/arithmeticmeancurve.git@dev
````

## Alpha Development Status

The current development state of this project is *alpha*. Towards the beta

- naming of modules, classes and methods will change, since the final wording is not
  done.
- Code inspections are not finished.
- The documentation is broad or incomplete.
- Testing is not complete, as it is added during the first test phase. At this
  state mostly doctests are applied at class or function level.


## Basic Usage

[Read-the-docs](https://arithmeticmeancurve.readthedocs.io/en/latest/index.html) for a more detailed documentation.

A curve within `armithmeticmeancurves` is defined by a pandas.DataFrame. Curves
for arithmetic mean curve calculation needs to provide equal column names.

```` python

# Creation of 3 random curves
# ===========================

import numpy as np
from pandas import DataFrame, Index
from scipy.interpolate import CubicSpline

cubic_spline = CubicSpline(x=[0.0, 0.2, 0.8, 1.0], y=[0.0, 0.3, 0.9, 1.0])
x_values = np.linspace(0.0, 1, num=11)
curvature = cubic_spline(x_values)
base_curve = np.stack((x_values, curvature), axis=1)

three_seeds = np.random.standard_normal(6).reshape(3, 2)
three_random_points = np.array([1.0, 10.0]) + np.array([0.09, 1]) * three_seeds

curves = []
for random_point in three_random_points:
    raw_curve = base_curve * random_point
    sample_curve = DataFrame(
        raw_curve[:, 1], columns=["sample"], index=Index(raw_curve[:, 0], name="x")
    )
    curves.append(sample_curve)

# The mean curve calculation
# ==========================

from arithmeticmeancurve import ArithmeticMeanCurve
a_mean_curve = ArithmeticMeanCurve(curves=curves)


# Plotting
# ========

import matplotlib.pyplot as plt

plt.plot(a_mean_curve.mean_curve, "-ko", label="arithmetic mean curve")
for label, curve in a_mean_curve.family_of_curves.iteritems():
    plt.plot(curve, "-", label="label")
plt.plot(a_mean_curve.scatter_curve, "--k", label="scatter curve")
plt.plot(a_mean_curve.std_circle, "--r", label="std circle")
plt.legend()
plt.show()

````

![basic_usage_example](https://arithmeticmeancurve.readthedocs.io/en/latest/_images/basic_usage_example_01.png)

## Contribution

Any contribution by reporting a bug or desired changes are welcomed. The preferred 
way is to create an issue on the gitlab's project page, to keep track of everything 
regarding this project.

### Contribution of Source Code
#### Code style
This project follows the recommendations of [PEP8](https://www.python.org/dev/peps/pep-0008/).
The project is using [black](https://github.com/psf/black) as the code formatter.

#### Workflow

1. Fork the project on Gitlab.
2. Commit changes to your own branch.
3. Submit a **pull request** from your fork's branch to our branch *'dev'*.

## Authors

* **David Scheliga** 
    [@gitlab](https://gitlab.com/david.scheliga)
    [@Linkedin](https://www.linkedin.com/in/david-scheliga-576984171/)
    - Initial work
    - Maintainer

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the
[LICENSE](LICENSE) file for details

## Acknowledge

[Code style: black](https://github.com/psf/black)
