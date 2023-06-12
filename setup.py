from setuptools import setup, find_packages

setup(
    name='qsm_forward',
    version='0.2',
    packages=find_packages(),
    url='https://github.com/astewartau/qsm_forward_model',
    author='Ashley Stewart',
    author_email='a.stewart.au@gmail.com',
    description='A forward-model simulation for Quantitative Susceptibility Mapping.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'matplotlib',
        'nibabel',
        'nilearn',
        'ipykernel',
        'scikit-image',
        'dipy',
        'torch'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)