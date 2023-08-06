from setuptools import find_packages, setup

long_description = open('README.md').read()
version_identifier = '0.2.1'

setup(
    name='airium',
    version=version_identifier,
    author='Michał Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michał Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT license',
    url='https://gitlab.com/kamichal/airium',
    description='Easy and quick html builder with natural syntax correspondence (python->html). '
                'No templates needed. Serves pure pythonic library with no dependencies.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    requires=[],
    install_requires=[],
    keywords='natural html generator compiler template-less',
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'airium = airium.__main__:entry_main'
        ],
    },
)
