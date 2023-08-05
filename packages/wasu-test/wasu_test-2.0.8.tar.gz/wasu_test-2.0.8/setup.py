import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.readlines()

setuptools.setup(
    name="wasu_test",
    version="2.0.8",
    author="XiaoDong Chen",
    author_email="chenxiaodong@wasu.com",
    description="The Wasu Auto TestFrameWork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(
        exclude=("phonenumbers", "slugify", "certifi", "chardet", "datautil", "toml", "wcwidth",
                 )),
    # install_requires=['PyMySQL==0.10.1',
    #                   'requests==2.18.4',
    #                   'xlrd==1.2.0',
    #                   'selenium==3.11.0',
    #                   'python_benedict==0.19.0',
    #                   'Appium_Python_Client==1.0.2',
    #                   'benedict==0.3.2',
    #                   'PyYAML==5.3.1'],
    py_modules=["six", "xmltodict", "MailChecker"],
    install_requires=install_requires,
    entry_points={

    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
