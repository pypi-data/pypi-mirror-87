import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf",
    "version": "0.0.19",
    "description": "Cloud Development Kit for Terraform",
    "license": "MPL-2.0",
    "url": "https://github.com/hashicorp/terraform-cdk",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hashicorp/terraform-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf",
        "cdktf._jsii"
    ],
    "package_data": {
        "cdktf._jsii": [
            "cdktf@0.0.19.jsii.tgz"
        ],
        "cdktf": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "constructs>=3.0.0, <4.0.0",
        "jsii>=1.14.0, <2.0.0",
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
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
