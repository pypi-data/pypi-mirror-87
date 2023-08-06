import setuptools



with open("README.md", "r") as fh:
    long_description = fh.read()

with open("cli/_version_.py","r") as f:
    _version = f.read().split('=')[1].strip(" \'\"")


setuptools.setup(
    name="huik-module", # Replace with your own username this is for PIP install, not the real python package name. the real name will be example_pkg
    version=_version,
    author="Hui Kang",
    author_email="rocksnow1942@gmail.com",
    description="Modules for my scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rocksnow1942/mymodule",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests","conf"]), # or can manually enter.
    # package_data = {'cli':['plugins/*.py']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = """
        [console_scripts]
        ok=cli:menu
        tl=cli:toollist
        fd=cli:folder
    """,
    install_requires=['psutil','click','colorama','terminaltables'],
    python_requires='>=3.6',
)

