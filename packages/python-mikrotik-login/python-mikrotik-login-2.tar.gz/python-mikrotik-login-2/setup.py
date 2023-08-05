import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-mikrotik-login",
    version="2",
    author="Ihsan Fajar Ramadhan",
    author_email="castrix.ihsan@gmail.com",
    description="Python code to login to Mikrotik WebClient without GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/castrix/PythonWebclientWifiLogin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)