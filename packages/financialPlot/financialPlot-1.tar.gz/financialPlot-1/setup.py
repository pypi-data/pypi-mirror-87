import setuptools

setuptools.setup(
    name="financialPlot",
    version="1",
    license='MIT',
    author="Gna",
    author_email="luckyrookie@khu.ac.kr",
    description="Visualizing tools of financial statement built on plotly.",
    long_description=open('README.md').read(),
    url="https://github.com/GyeongahNa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)