import setuptools

setuptools.setup(
    version="0.0.5",
    name="mcelfish",
    packages=["mcelfish"],
    install_requires=["numpy", "matplotlib", "pymc3",],
    entry_points={
        "console_scripts": [
            "mcelfish=mcelfish:main",
            "mcelfish-gen=mcelfish:generate",
            "mcelfish-cs=mcelfish:cs_z",
            "mcelfish-z=mcelfish:cs_z",
        ]
    },
)
