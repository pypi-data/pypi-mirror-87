import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tremendous-theme-selector',
    version="0.92",
    author="zeionara",
    author_email="zeionara@gmail.com",
    description="A simple app for manually annotating audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeionara/tremednous-theme-selector",
    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'pygame'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
