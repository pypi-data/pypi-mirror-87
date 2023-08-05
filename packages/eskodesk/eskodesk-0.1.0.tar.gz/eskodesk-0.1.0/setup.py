import setuptools

version = __import__("eskodesk").__version__

setuptools.setup(
    name="eskodesk",
    version=version,
    description="Python client for the Eskodesk API",
    author="Eskolare Negócios Digitais Ltda",
    author_email="vitor.f@eskolare.com.br",
    packages=["eskodesk"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
    python_requires=">=3.5",
    install_requires=["requests>=2.14.0,<2.26"],
)
