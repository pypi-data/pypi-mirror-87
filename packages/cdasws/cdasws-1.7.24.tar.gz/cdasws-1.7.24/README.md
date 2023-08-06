
## Synopsis

This library provides a simple python interface to the data and services of 
NASA's [Coordinated Data Analysis System](https://cdaweb.sci.gsfc.nasa.gov/)
(CDAS).  This library implements the client side of the 
[CDAS RESTful web services](https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/)
and can return data in the 
[SpacePy data model](https://pythonhosted.org/SpacePy/datamodel.html)
with all the original 
[ISTP/SPDF metadata](https://spdf.sci.gsfc.nasa.gov/sp_use_of_cdf.html).
Frequently asked questions concerning this library are at 
[FAQ](https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/py/FAQ.html).
For more general details about the CDAS web services, see
https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/.

## Code Example

This package contains example code calling most of the available web services.
To run the included example, do the following

    python -m cdasws

---

The following code demonstrates how to access magnetic field measurements
from the 
[ACE mission dataset](https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#AC_H1_MFI).

    from cdasws import CdasWs
    import matplotlib.pyplot as plt

    cdas = CdasWs()
    data = cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                         '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z')[1]
    print(data)
    {'Epoch': VarCopy([datetime.datetime(2009, 6, 1, 0, 0),
         datetime.datetime(2009, 6, 1, 0, 4),
         datetime.datetime(2009, 6, 1, 0, 8)], dtype=object), 'Magnitude': VarCopy([3.495, 3.474, 3.477], dtype=float32), 'BGSEc': VarCopy([[-0.106,  2.521, -2.391],
         [-0.412,  2.402, -2.449],
         [-0.094,  2.309, -2.587]], dtype=float32), 'cartesian': VarCopy(['x_component', 'y_component', 'z_component'], dtype='<U11'), 'metavar0': VarCopy(['Bx GSE', 'By GSE', 'Bz GSE'], dtype='<U6')}

    print(data['Magnitude'].attrs)

    {'FIELDNAM': 'B-field magnitude', 'VALIDMIN': 0.0, 'VALIDMAX': 500.0, 'SCALEMIN': 0.0, 'SCALEMAX': 10.0, 'UNITS': 'nT', 'FORMAT': 'F8.3', 'VAR_TYPE': 'data', 'DICT_KEY': 'magnetic_field>magnitude', 'FILLVAL': -1e+31, 'DEPEND_0': 'Epoch', 'CATDESC': 'B-field magnitude', 'LABLAXIS': '<|B|>', 'DISPLAY_TYPE': 'time_series', 'DIM_SIZES': 0}

    plt.plot(data['Epoch'], data['Magnitude'])
    plt.xlabel(data['Epoch'].attrs['LABLAXIS'])
    plt.ylabel(data['Magnitude'].attrs['LABLAXIS'] + ' ' +
               data['Magnitude'].attrs['UNITS'])
    plt.show()

---

To have uniformly spaced (with respect to time) values computed (with optional
spike removal), add the binData keyword paramter like this

    status, data = cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                 '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z',
                                 binData={
                                     'interval': 60.0,
                                     'interpolateMissingValues': True,
                                     'sigmaMultiplier': 4
                                 })
    print(data)

    {'Epoch_bin': VarCopy([datetime.datetime(2009, 6, 1, 0, 0, 30),
         datetime.datetime(2009, 6, 1, 0, 1, 30),
         datetime.datetime(2009, 6, 1, 0, 2, 30),
         datetime.datetime(2009, 6, 1, 0, 3, 30),
         datetime.datetime(2009, 6, 1, 0, 4, 30),
         datetime.datetime(2009, 6, 1, 0, 5, 30),
         datetime.datetime(2009, 6, 1, 0, 6, 30),
         datetime.datetime(2009, 6, 1, 0, 7, 30),
         datetime.datetime(2009, 6, 1, 0, 8, 30),
         datetime.datetime(2009, 6, 1, 0, 9, 30)], dtype=object), 'Epoch': VarCopy([datetime.datetime(2009, 6, 1, 0, 0),
         datetime.datetime(2009, 6, 1, 0, 4),
         datetime.datetime(2009, 6, 1, 0, 8)], dtype=object), 'Magnitude': VarCopy([3.495  , 3.48975, 3.4845 , 3.47925, 3.474  , 3.47475, 3.4755 ,
         3.47625, 3.477  , 3.477  ], dtype=float32), 'BGSEc': VarCopy([[-0.106    ,  2.521    , -2.391    ],
         [-0.1825   ,  2.49125  , -2.4055   ],
         [-0.259    ,  2.4615   , -2.42     ],
         [-0.3355   ,  2.4317498, -2.4345   ],
         [-0.412    ,  2.402    , -2.449    ],
         [-0.3325   ,  2.3787498, -2.4835   ],
         [-0.253    ,  2.3555   , -2.518    ],
         [-0.1735   ,  2.33225  , -2.5524998],
         [-0.094    ,  2.309    , -2.587    ],
         [-0.094    ,  2.309    , -2.587    ]], dtype=float32), 'MAGNITUDE_NBIN': VarCopy([1., 0., 0., 0., 1., 0., 0., 0., 1., 0.], dtype=float32), 'MAGNITUDE_BIN_DELTA_MINUS_VAR': VarCopy([-1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31,
         -1.e+31, -1.e+31, -1.e+31], dtype=float32), 'MAGNITUDE_BIN_DELTA_PLUS_VAR': VarCopy([-1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31, -1.e+31,
         -1.e+31, -1.e+31, -1.e+31], dtype=float32), 'BGSEC_NBIN': VarCopy([[ 1.,  1.,  1.],
         [-0., -0., -0.],
         [-0., -0., -0.],
         [-0., -0., -0.],
         [ 1.,  1.,  1.],
         [-0., -0., -0.],
         [-0., -0., -0.],
         [-0., -0., -0.],
         [ 1.,  1.,  1.],
         [-0., -0., -0.]], dtype=float32), 'BGSEC_BIN_DELTA_MINUS_VAR': VarCopy([[-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31]], dtype=float32), 'BGSEC_BIN_DELTA_PLUS_VAR': VarCopy([[-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31],
         [-1.e+31, -1.e+31, -1.e+31]], dtype=float32), 'cartesian_bin': VarCopy(['x_component', 'y_component', 'z_component'], dtype='<U11'), 'cartesian': VarCopy(['x_component', 'y_component', 'z_component'], dtype='<U11'), 'metavar0': VarCopy(['Bx GSE', 'By GSE', 'Bz GSE'], dtype='<U6'), 'metavar1': VarCopy(['# of Bx GSE', '# of By GSE', '# of Bz GSE'], dtype='<U11'), 'metavar2': VarCopy('# of ', dtype='<U5')}

## Motivation

This library hides the HTTP, JSON/XML, and CDF details of the CDAS web 
services. A python developer only has to deal with python objects and 
methods (primarily the SpacePy data model object with full ISTP/SPDF
metadata).

## Dependencies

Accept for common, fundamental depenencies like requests, the
primary dependency is
[SpacePy](https://pythonhosted.org/SpacePy/).  And SpacePy is only 
required if you call the get_data method that returns the data in the
SpacePy data model. Refer to the SpacePy
documentation for the details of SpacePy's dependencies.  In particular, 
SpacePy's data model import capability is dependent upon
[CDF](https://cdf.sci.gsfc.nasa.gov) which is
not (at the time of this writing) automatically installed with SpacePy.  

## Installation

As noted in the dependencies above, if you intend to call the get_data
method, you must install [SpacePy](https://pythonhosted.org/SpacePy/) and
the [CDF](https://cdf.sci.gsfc.nasa.gov) library (following the
procedures at the SpacePy and CDF web sites).

Then, to install this package

    $ pip install -U cdasws


## API Reference

Refer to
[cdasws package API reference](https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html)

or use the standard python help mechanism.

    from cdasws import CdasWs
    help(CdasWs)

## Tests

The tests directory contains 
[unittest](https://docs.python.org/3/library/unittest.html)
tests.

## Contributors

Bernie Harris.  
[e-mail](mailto:gsfc-spdf-support@lists.nasa.gov) for support.

## License

This code is licensed under the 
[NASA Open Source Agreement](https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt) (NOSA).
