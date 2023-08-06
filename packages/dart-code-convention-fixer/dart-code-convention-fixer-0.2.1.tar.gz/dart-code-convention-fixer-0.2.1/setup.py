import re
from setuptools import setup

version = re.search(
    "^__version__\\s*=\\s*\"(.*)\"",
    open('dartCCF/__init__.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    README = f.read().decode("utf-8")

# This call to setup() does all the work
setup(
    name="dart-code-convention-fixer",
    version=version,
    description="Dart code convention fixer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/marynakukhta/metaprog",
    author="Kukhta Maryna",
    author_email="mskyhta@gmail.com",
    packages=["dartCCF"],
    entry_points={
        "console_scripts": [
            "dartCCF=dartCCF.__main__:main",
        ]
    },
)
