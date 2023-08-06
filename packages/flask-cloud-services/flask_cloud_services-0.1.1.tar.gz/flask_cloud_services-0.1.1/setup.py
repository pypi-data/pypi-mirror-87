import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_cloud_services",
    version="0.1.1",
    author="Terminus",
    author_email="david.tabla@zinobe.com",
    description="Cloud Services in Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/terminus-zinobe/flask-cloud-services",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'boto3>=1.12',
        'flask>=1.0',
        'requests>=2.23',
    ]
)
