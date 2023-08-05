import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name="CapiPy", 
    version="0.1.0",
    author="David Roura Padrosa",
    author_email="davidrourap@gmail.com",
    description="CapiPy (Computer Assistance for Protein Immobilisation – Python) ",
    long_description= README,
    url="https://github.com/drou0302/CapiPy",
    packages=['CapiPy'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"]
)
