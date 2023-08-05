
import setuptools

setuptools.setup(
    name="dbd_music",
    version="0.0.6",
    author="SilentJungle399",
    description="Simplest thing you could use for music in python.",
    packages=["dbd_music"],
    install_requires=["discord.py", "lavalink"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)