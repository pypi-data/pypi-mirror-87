import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mhyt',  # How you named your package folder (MyLib)
    version='3.5.5',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='download files from youtube using simple code',  # Give a short description about your library
    author='matan h',  # Type in your name
    author_email='matan.honig2@gmail.com',  # Type in your E-Mail
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matan-h/mhyt",
    packages=['mhyt'],
    install_requires=["youtube-dl","imageio_ffmpeg"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
