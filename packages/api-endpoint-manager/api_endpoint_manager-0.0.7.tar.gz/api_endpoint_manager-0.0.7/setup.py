import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api_endpoint_manager",
    version="0.0.7",
    author="Quaking Aspen",
    author_email="info@quakingaspen.net",
    license='MIT',
    description="This library contains classes to simplify the process of Flask API end points definition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quakingaspen-codehub/api_endpoint_manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platform=['Any'],
    python_requires='>=3.6',
    install_requires=['http_request_response==0.0.14', 'http_request_args','flask_jwt_auth','flask_restplus']
)
