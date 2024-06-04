from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PyCurl',
    version='2.0.0',
    packages=find_packages(),
    url='https://github.com/CarrilloTlx/PyCurl',
    license='OSI Approved :: Open Software License ("OSL") v 3.0',
    author='José Luis Coyotzi Ipatzi',
    author_email='jlci811122@gmail.com',
    description='PyCurl: Un envoltorio flexible alrededor de la biblioteca requests para realizar solicitudes HTTP.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Open Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)