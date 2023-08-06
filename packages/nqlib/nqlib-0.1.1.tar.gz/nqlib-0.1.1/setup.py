from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='nqlib',
    version='0.1.1',  # '0.0.1-pre.1' or '0.0.1'
    packages=find_packages(
        exclude=[
            'tests',
            'nqlib_dev',
        ],
    ),

    install_requires=[
        'numpy',
        'control',
        'cvxpy',
        'slycot',
    ],
    # extras_require={
    #     # ここにはオプション機能に必要な外部パッケージを辞書形式で記載
    #     'minreal':  ["slycot"],
    # },

    # author
    author='kenta tanaka',
    author_email='kenta.tanaka@eom.mech.eng.osaka-u.ac.jp',

    # プロジェクトホームーページのURL
    url='https://github.com/knttnk/NQLib',
    description='NQLib: Library to design noise shaping quantizer for discrete-valued input control.',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=(
        # str: PyPI 検索対象にしたいキーワードをスペース区切りで
        # PyPI上での検索，閲覧のために利用される
        'discrete-valued input control, '
        'control theory, '
        'quantizer, '
        'control system design, '
        'quantization, '
        'simulation, '
    ),

    # Pythonバージョンは3.6以上4未満
    python_requires='>=3.6',

    # ライセンス，Pythonバージョン，OSを含める
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
