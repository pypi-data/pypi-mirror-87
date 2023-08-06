from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pyWinActivate",
    version="1.1.0",
    author="SimeonTodorov",
    author_email="the_nexus@mail.bg",
    description="Activate and focus on any opened window by using the window title.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["pyWinActivate"],
    package_dir={"": "src"},
    url="https://github.com/InfiniteNex/pyWinActivate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)