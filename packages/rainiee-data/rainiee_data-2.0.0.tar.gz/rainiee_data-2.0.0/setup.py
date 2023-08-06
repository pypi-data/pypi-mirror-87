import setuptools
import os
path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md'),encoding='utf8') as f:
        long_description = f.read()
except Exception as e:
    long_description = "rainiee stock"

setuptools.setup(
    name="rainiee_data",
    version="2.0.0",
    author="rainiee",
    author_email="rainiee@163.com",
    description="rainiee stock data api",
    long_description = long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Rainiee-Technology/rainiee_data",
    license='MIT',
    zip_safe=False,
    packages=setuptools.find_packages(),
    python_requires='>=3',
)