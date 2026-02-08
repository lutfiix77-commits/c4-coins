from setuptools import setup, find_packages

setup(
    name="c4-coins",
    version="1.0.9",
    author="C4-Coins Team",
    packages=find_packages(),
    # Hanya masukkan library yang BUKAN bawaan Python di sini
    install_requires=[
        'requests',
        'emoji',
    ],
    entry_points={
        'console_scripts': [
            'c4-coins=c4_coins.main:main',
        ],
    },
)
