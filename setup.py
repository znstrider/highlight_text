import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="highlight_text",
    version="0.1",
    author="znstrider",
    author_email="mindfulstrider@gmail.com",
    description="matplotlib functions to plot text with color highlighted substrings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/znstrider/highlight_text",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.6',
)