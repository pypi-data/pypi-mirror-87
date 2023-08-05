from setuptools import setup

VERSION = '2.6.0'
NAME = 'enos_subscribe'

install_requires = ["six", 'protobuf', 'websocket_client']
tests_require = []

insecure_pythons = '2.6, ' + ', '.join("2.7.{pv}".format(pv=pv) for pv in range(10))

extras_require = {
    ':python_version in "{ips}"'.format(ips=insecure_pythons):
        ['backports.ssl_match_hostname'],
    ':python_version in "2.6"': ['argparse'],
}

setup(
    name=NAME,
    version=VERSION,
    description="Enos subscribe client for python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="EnvisionIot",
    author_email="sw.tc@envision-digital.com",
    license="BSD",
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    keywords='enos subscribe client',
    install_requires=install_requires,
    packages=["enos_subscribe", "enos_subscribe.proto", "enos_subscribe.vendor", "enos_subscribe.test"]
)
