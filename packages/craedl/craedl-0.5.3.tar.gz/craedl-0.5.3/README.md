# Craedl Python SDK

The Craedl Python SDK (Software Development Kit) enables Craedl users to access
their [Craedl](https://craedl.org) accounts using the Python programming
language. This provides a mechanism for using Craedl on computers without access
to a web browser (such as a high-performance computing cluster) and to automate
common Craedl project manipulations (such as file uploads and downloads) within
a Python script.

## Quick start

Get started with the Craedl Python SDK by obtaining it via
[PyPI](https://pypi.org/project/craedl/):

```
pip install craedl
```

Log into your Craedl account at [Craedl.org](https://craedl.org) and generate an
API access token by clicking the key icon in the `My Craedl` card. Copy your
token and paste it when prompted after running one of the following commands:

**(A) Configure your account through a system shell**
```
python -m craedl
```

**(B) Configure your account through an interactive Python interpreter**
```
import craedl
craedl.configure()
```

Now you can use Python to access your Craedl, for example:

```
import craedl
profile = craedl.auth()
for project in profile.get_projects():
    print(project.name)
```

## More information

For more information about the Craedl Python SDK, refer to
[our documentation](https://craedl-sdk-python.readthedocs.io). The source code
is hosted on [GitHub](https://github.com/craedl/craedl-sdk-python).
