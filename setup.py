from setuptools import setup, find_packages


LIBRARY_NAME = "mooch_switcher"
PACKAGE_DIR = 'mooch'

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name=LIBRARY_NAME,
    version="0.1.0",
    # package_dir={"": PACKAGE_DIR},
    # packages=find_packages(PACKAGE_DIR),
    packages=find_packages(),
    install_requires=install_requires,
    author="kenyo3026",
    author_email="kenyo3026@gmail.com",
    description="🔄 Mooch Switch - Get the most out of your free-tier API keys with automatic switching on rate limits",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kenyo3026/moochswitcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    keywords="api, rate-limit, openai, litellm, switching, free-tier",
    project_urls={
        "Bug Reports": "https://github.com/kenyo3026/moochswitcher/issues",
        "Source": "https://github.com/kenyo3026/moochswitcher",
    },
) 