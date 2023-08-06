import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zbmain",
    version="0.0.8",
    author="zhaobin",
    author_email="zbmain@qq.com",
    description="public python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zbmain/py_pub",
    packages=setuptools.find_packages(),
    classifiers=[
         # 该软件包仅与Python3兼容
        "Programming Language :: Python :: 3",
        # 根据MIT许可证开源
        "License :: OSI Approved :: MIT License",
        # 与操作系统无关
        "Operating System :: OS Independent",
    ],
    #.egg
    # zip_safe = False
)