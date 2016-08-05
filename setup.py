from setuptools import setup

setup(
    name="fix-srt",
    version="1.0.0",
    author="Eric Reynolds",
    author_email="eric.remo.reynolds@gmail.com",
    description="A tiny Python package to fix SRT subtitle files when out of sync with audio",
    license="MIT",
    keywords="subtitle subtitles srt sync audio synchronize",
    url="https://github.com/ericremoreynolds/fix-srt",
    scripts=[
        "fix-srt.py"
    ]
)
