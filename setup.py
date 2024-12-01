from setuptools import setup, find_packages

setup(
    name='PiMemorizeGame',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pygame-ce>=2.5.2',
        'pygame_gui>=0.6.12'
    ],
    extras_require={
        'pygame': [],
    },
    description='A game for learning Pi digits through various modes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jkarasek/PiGame',  # Repository (np. GitHub)
    package_data={
        'PiGame': ['*.txt', 'images/*.png'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pimemorize = PiGame.main:PiGame',
        ],
    },

)
