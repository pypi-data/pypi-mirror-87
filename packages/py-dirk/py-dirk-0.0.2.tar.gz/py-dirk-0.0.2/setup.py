from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='py-dirk',
    version='0.0.2',
    description='dirk exports KUBECONFIG via direnv',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/grothesk/py-dirk',
    author='Malte Groth',
    author_email='malte.groth@gmx.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='cli, kubernetes, direnv',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'dirk=dirk.cli:main'
        ],
    }
)
