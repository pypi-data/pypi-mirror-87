import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_lnd_grpc",
    version="0.0.4",
    author="Tony Sanak",
    author_email="tony@lwqd.money",
    description="grpc client for lnd python version 3.6",
    long_description=long_description,
    keywords="python grpc lnd lightning bitcoin async lightning-network rpc",
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/lightningriders/lnd_grpc",
    # packages=setuptools.find_packages(exclude=["googleapis"]),
    packages=['python_lnd_grpc', 'python_lnd_grpc.protos'],
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=["grpcio", "grpcio-tools", "googleapis-common-protos"],
    exclude_packages=['tests'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)