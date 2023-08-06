import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zertoapl",
    version="0.0.3",
    author="Alex Schenck and Shaun Finn",
    author_email="linuxbeak@gmail.com, shaun_ryan_finn@yahoo.com",
    description="Zerto Automation API Library",
    long_description="zertoapl is a simple python3 API wrapper for the Zerto product by the eponymous "
                     "corporation. It is intended to simplify the deployment and management of Zerto in a code-driven "
                     "manner. Potential uses for this API wrapper are as diverse as you may wish to make it. An example "
                     "script of automatically protecting tagged virtual machines (VMs) is included in this library.",
    long_description_content_type="text/markdown",
    url="https://github.com/pilotschenck/pyzerto-unofficial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)