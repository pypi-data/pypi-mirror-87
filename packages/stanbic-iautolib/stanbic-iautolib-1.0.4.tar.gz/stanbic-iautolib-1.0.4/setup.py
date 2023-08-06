import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="stanbic-iautolib",
    version="1.0.4",
    description="This is an Intelligent Automation Library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/redkad/iautolib",
    author="Patrick Adu-Amankwah",
    author_email="p.a.amankwah@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["iautolib", "iautolib/themes"],
    include_package_data=True,
    install_requires=['numpy', 'selenium', 'opencv-python', 'pyautogui', 'keyboard', 'pandas', 'requests', 'clipboard', 'tk', 'pywin32', 'PyQt5', 'pyqt5-tools', 'pytesseract'],
    entry_points={
        "console_scripts": [
            "iautolib=iautolib.ilib:ilib",
        ]
    },
)