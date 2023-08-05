import setuptools

with open('README.md') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    author="Raeveen Pasupathy",
    author_email="raeveen@staffemail.apu.edu.my",
    name='apu_cas',
    description="apu_cas is a python package for authentication with "
                "Asia Pacific University's Central Authentication Service",
    version='0.4.1',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ctiteam/apu-cas-pip/',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['requests', 'Flask'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ]
)
