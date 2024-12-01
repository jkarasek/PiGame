from setuptools import setup, find_packages

setup(
    name='PiGame',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pygame_gui',
    ],
    description='A game for learning Pi digits through various modes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jkarasek/PiGame',  # Repository (np. GitHub)
    include_package_data=True,
    package_data={
        'PiGame': ['*.txt', 'images/*.png'],
    },

    python_requires='>=3.12',  # Minimal python version
)
