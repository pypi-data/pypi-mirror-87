import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "alps-unified-ts",
    "version": "0.0.11",
    "description": "alps-unified-ts",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/alps-unified-ts.git",
    "long_description_content_type": "text/markdown",
    "author": "Martin Mueller<damadden88@googlemail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/alps-unified-ts.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "alps_unified_ts",
        "alps_unified_ts._jsii"
    ],
    "package_data": {
        "alps_unified_ts._jsii": [
            "alps-unified-ts@0.0.11.jsii.tgz"
        ],
        "alps_unified_ts": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.15.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
