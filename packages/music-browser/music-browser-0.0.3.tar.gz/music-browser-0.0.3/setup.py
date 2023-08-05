import setuptools

setuptools.setup(
    name="music-browser",
    description="Music search engine for CrossPlay web service.",
    version="0.0.3",
    packages=setuptools.find_packages(),
    install_requires=["marshmallow", "requests"],
)
