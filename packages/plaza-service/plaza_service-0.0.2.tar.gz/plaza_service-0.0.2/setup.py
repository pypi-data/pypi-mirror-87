from setuptools import setup

setup(
    name="plaza_service",
    version="0.0.2",
    description="Helper to build plaza services.",
    author="kenkeiras",
    author_email="kenkeiras@codigoparallevar.com",
    url="https://gitlab.com/plaza-project/bridges/python-plaza-lib",
    license="Apache License 2.0",
    packages=["plaza_service"],
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
    install_requires=["websockets"],
    zip_safe=False,
)
