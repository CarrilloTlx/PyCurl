from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PyCurlify',
    version='2.0.0',
    packages=find_packages(),
    url='https://github.com/CarrilloTlx/PyCurlify',
    license='MIT',
    author='José Luis Coyotzi Ipatzi',
    author_email='jlci811122@gmail.com',
    description='PyCurl: Un envoltorio flexible alrededor de la biblioteca requests para realizar solicitudes HTTP.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
