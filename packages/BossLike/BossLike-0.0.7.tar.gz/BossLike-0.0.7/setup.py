import setuptools

with open("README.md", "r", encoding="utf8") as fh:
	long_description = fh.read()

setuptools.setup(
    name="BossLike",
    version="0.0.7",
    author="Murat Mazitov",
    author_email="j.murat2020@yandex.ru",
    description="BossLike is a ready-made module for working with the api bosslike.ru (for the performer)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['BossLike'],
    python_requires='>=3.7',
    install_requires=[
    		'requests'
	]
)