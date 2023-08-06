import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ['pyaliyun']

setup_args = dict(
    name="pyaliyunsdk",
    version="0.0.5",
    author="Maliao",
    author_email="maliaotw@gmail.com",
    description="Aliyun SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maliaotw/pyaliyun.git",
    package_dir={'pyaliyun': 'pyaliyun'},
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'aliyun-python-sdk-core==2.13.26',
    'aliyun-python-sdk-ecs==4.19.12',
    'aliyun-python-sdk-rds==2.5.1',
    'aliyun-python-sdk-slb==3.2.18'

]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
