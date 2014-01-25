from setuptools import setup, find_packages

setup(
    name='Celebrate Good Times',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask',
                      'Flask-SQLAlchemy',
                      'uwsgi',
                      'python-dateutil',
                      'foursquare',
                     ],
    entry_points = {
        "distutils.commands": [
            "create_db = celebrate.csv2db:main",
        ],
        "console_scripts": [
            "celebrate = celebrate.main:main"
        ]
    },

)
