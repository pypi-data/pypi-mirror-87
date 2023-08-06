from setuptools import setup

setup(
    name='staples_detection',
    version='1.0',
    packages=['staples_detection'],
    url='https://github.com/mmunar97',
    license='mit',
    author='marcmunar',
    author_email='marc.munar@uib.es',
    description='Algorithm for staple detection and mask generation',
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "scikit-image"
    ]
)
