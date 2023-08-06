"""
Documentation
-------------
source code from : https://github.com/matusnovak/doxybook

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="GxDoxybook",
        description="Convert C annotation to gitbook",
        keywords="c annotation gitbook",
        long_description=long_description,
        version="1.0.7",
        author="zhaobk",
        author_email="zhaobk@nationalchip.com",
        packages=['doxybook', 'doxybook.templates'],
        install_requires=['Jinja2'],
        package_data={},
        entry_points={
            'console_scripts':[
                'doxybook=doxybook:main',
                'genbook=doxybook.genbook:main',
                'docupdate=doxybook.update:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
