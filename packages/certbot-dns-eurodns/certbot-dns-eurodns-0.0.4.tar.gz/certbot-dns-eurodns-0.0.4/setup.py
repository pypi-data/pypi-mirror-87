from setuptools import setup, find_packages

version = "0.0.4"

install_requires = [
    "acme>=0.21.1",
    "certbot>=0.21.1",
    "setuptools",
    "zope.interface",
    "requests>=2.21.0",
]

dev_extras = ["black", "mypy", "prospector"]

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name="certbot-dns-eurodns",
    version=version,
    description="EuroDNS Certbot Plugin",
    author="EuroDNS",
    url="https://github.com/mgarriga73/certbot-dns-eurodns",
    license="Apache License 2.0",
    long_description=long_description,
    python_requires="!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    author_email="miquel@entorno.es",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={"dev": dev_extras},
    entry_points={
        "certbot.plugins": [
            "dns-eurodns = certbot_dns_eurodns.dns_eurodns:Authenticator"
        ]
    },
)
