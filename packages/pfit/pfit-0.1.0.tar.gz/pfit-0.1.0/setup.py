from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pfit',
    version='0.1.0',
    description='Tools to support interoperability and the adoption of standards for permafrost data files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/permafrostnet/pfit',
    author='PermafrostNet',
    author_email='nick.brown@carleton.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='ground, temperature, sensor, permafrost, earth, science, soil, data',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['numpy', 'pandas', 'netcdf4', 'xlrd'],
    project_urls={
        'Bug Reports': 'https://gitlab.com/permafrostnet/pfit/-/issues',
        'Source': 'https://gitlab.com/permafrostnet/pfit',
    },
)