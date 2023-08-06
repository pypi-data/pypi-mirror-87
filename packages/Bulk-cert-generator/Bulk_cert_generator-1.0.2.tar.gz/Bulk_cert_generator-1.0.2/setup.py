from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='Bulk_cert_generator',
    version='1.0.2',
    description='Easy to Make Multiple Certificate',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Alfiankan',
    author_email='alfiankan19@gmail.com',
    keywords=['Certificate Generator Python', 'Multi Certificate Generator', 'Make Certificate With Python'],
    url='https://github.com/alfiankan/bulk-cert-generator',
    download_url='https://pypi.org/project/bulk-cert-generator/'
)

install_requires = [
    'opencv-python',
    'openpyxl',
    'img2pdf',
    'Pillow'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)