import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotify-album-art",
    version="0.0.3.1",
    author="Orion Crocker",
    author_email="orion@orionc.dev",
    description="Download album artwork from Spotify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orioncrocker/spotify_images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
