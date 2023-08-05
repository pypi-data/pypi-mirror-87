# Modules
import setuptools

# Read from README
with open("README.md", "r") as f:
    description = f.read()

# Begin setup
setuptools.setup(
    name = "throwaway-keys",
    version = "0.0.6",
    author = "iiPython",
    author_email = "ben@iipython.cf",
    description = "Package to generate 'throwaway keys' for encrypting information",
    long_description = description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ii-Python/throwaway-keys",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Topic :: Security :: Cryptography"
    ],
    keywords = ["keys", "sha256", "encryption", "hashlib"],
    python_requires = ">=3.6.2"
)
