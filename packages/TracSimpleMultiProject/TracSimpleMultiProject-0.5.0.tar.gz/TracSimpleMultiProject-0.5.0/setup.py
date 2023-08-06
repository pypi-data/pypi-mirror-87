from setuptools import setup

setup(
    name='TracSimpleMultiProject',
    version='0.5.0',
    packages=['simplemultiproject'],
    package_data={
        'simplemultiproject': [
            'templates/*.html',
            'htdocs/*.js',
            'htdocs/css/*.css'
        ]
    },
    install_requires=['Trac'],
    extras_require={
        'Trac': 'Trac >= 0.12'
    },
    author='Christopher Paredes',
    author_email='jesuchristopher@gmail.com',
    maintainer="falkb",
    license='GPL',
    url='https://trac-hacks.org/wiki/SimpleMultiProjectPlugin',
    description='Simple Multi Project plugin for managing several projects with one Trac instance.',
    long_description='Simple Multi Project',
    keywords='Simple Multi Project',
    entry_points={'trac.plugins': ['simplemultiproject = simplemultiproject']}
)
