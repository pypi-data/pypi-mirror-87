from setuptools import setup



with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="riskcontrol",
    version="0.1.32",
    author="SimaShanhe",
    author_email="hsliu_em@126.com",
    description="Added the report of score ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['riskcontrol'],
    install_requires=[
        'scikit-learn>=0.21.3',
        'scipy',
        'numpy',
        'matplotlib',
        'seaborn',
        'prettytable',
        'tqdm'
    ]
)