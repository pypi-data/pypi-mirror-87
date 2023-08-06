
import setuptools

setuptools.setup(
    name="dbdmusic",
    version="0.0.1",
    author="SilentJungle399",
    description="Simplest thing you could use for music in python.",
    packages=["dbdmusic"],
    install_requires=["discord.py", "lavalink"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)