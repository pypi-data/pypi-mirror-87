from distutils.core import setup

setup(
    name="simple_avk",
    packages=["simple_avk"],
    version="1.6",
    license="unlicense",
    description="Simple asynchronous VK API client library by megahomyak",
    author="megahomyak",
    author_email="g.megahomyak@gmail.com",
    url="https://github.com/megahomyak/simple_avk",
    download_url="https://github.com/megahomyak/simple_avk/archive/v1.6.tar.gz",
    keywords=["SIMPLE", "ASYNCHRONOUS", "VK", "API"],
    install_requires=["aiohttp"]
)
