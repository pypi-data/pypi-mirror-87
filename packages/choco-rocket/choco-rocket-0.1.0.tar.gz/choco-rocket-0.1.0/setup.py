import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="choco-rocket",
    version="0.1.0",
    author="Jose Augusto O. Rufino",
    author_email="joseaorufino@gmail.com",
    description="Arcade Game with an Astronaut and his Rocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joseaorufino/choco-rocket",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame'
        ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'chocorocket=ChocoRocket.main:main'
            ]
        }
)
