from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='ezblockreal',
    version='0.1.1',
    description="Sunfounder utility block to use real components",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author="gpspelle",
    author_email="gpsunicamp016@gmail.com",
    keywords=['Raspberrypi', 'Sunfounder', 'Ezblock'],
    url="https://github.com/gpspelle/ezblock-real-modules/"
)

if __name__ == '__main__':
    setup(**setup_args)
