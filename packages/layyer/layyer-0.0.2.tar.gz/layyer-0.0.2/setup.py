import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="layyer", # Replace with your own username
    version="0.0.2",
    author="Pranpaveen Lay.",
    author_email="pranpaveen.lay@gmail.com",
    description="layyer lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy'],
    python_requires='>=3.6',
)