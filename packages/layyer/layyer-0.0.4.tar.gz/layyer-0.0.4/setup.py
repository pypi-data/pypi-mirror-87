import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="layyer", # Replace with your own username
    version="0.0.4",
    author="Pranpaveen Lay.",
    author_email="pranpaveen.lay@gmail.com",
    description="layyer lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['layyer'],
    package_dir={'layyer': 'src/layyer'},
    package_data={'layyer': ['discodef/*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy'],
    python_requires='>=3.6',
)