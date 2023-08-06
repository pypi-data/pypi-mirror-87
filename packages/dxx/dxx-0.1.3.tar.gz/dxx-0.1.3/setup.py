from setuptools import setup

setup(
    name="dxx",
    version="0.1.3",
    description="dxx is a library for io and converting audio files with a .DXX extension.",
    packages=["dxx"],
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "dxxconv = dxx.dxxconv:main",
            "len_file_dxx = dxx.len_file_dxx:main"
        ]
    },
    author="Tetsu Takizawa",
    author_email="tetsu.varmos@gmail.com",
    url="https://github.com/tetsuzawa/dxx-py"
)
