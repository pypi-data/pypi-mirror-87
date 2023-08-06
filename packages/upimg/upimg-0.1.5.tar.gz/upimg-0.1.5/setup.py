import io
from setuptools import setup, find_packages

with io.open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="upimg",
    version="0.1.5",
    description="A CLI tool to genarate Markdown links from clipboard",
    url="https://github.com/mocobk/upimg",
    long_description=README,
    long_description_content_type="text/markdown",
    author="mocobk",
    author_email="mailmzb@163.com",
    license="MIT",
    install_requires=["notify-py; sys_platform == 'darwin'",
                      "pillow",
                      "plyer; sys_platform == 'win32'",
                      "pynput",
                      "pyobjc; sys_platform == 'darwin'",
                      "pyperclip",
                      "upyun"],
    packages=find_packages('.'),
    package_data={'upimg.sys_platform': ['notification.ico']},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["upimg = upimg.cli:main"]},
)


