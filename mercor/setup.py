import setuptools

description="'Mercor's hiring project Github Automated Analysis"
__version__ = "0.0.0"

AUTHOR_USER_NAME = "Tejpal"
SRC_REPO = "GitHub Automated Analysis"
AUTHOR_EMAIL = "tej@gmail.com"



setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    long_description=description,
    packages=setuptools.find_packages()
)