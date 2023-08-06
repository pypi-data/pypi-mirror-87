import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

# dependencies
INSTALL_REQUIRES = [
    "click",
    "pyyaml",
    "setproctitle"
]

setuptools.setup(
    name="idiary",
    version="0.0.1",
    author="Junbo Zhao",
    author_email="zhaojb17@mails.tsinghua.edu.cn",
    description="Personal Diary Software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaojb17/idiary",
    packages=setuptools.find_packages(),
    package_data={'': ['*.yaml']},
    install_requires=INSTALL_REQUIRES,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "idiary=idiary.main:main"
        ]
    },
)
