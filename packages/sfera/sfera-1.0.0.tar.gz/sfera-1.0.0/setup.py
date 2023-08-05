import json
import pathlib
import re
import setuptools


_ROOT = pathlib.Path(__file__).absolute().parent
_GITHUB_URL = 'https://github.com/sfera-institute/python'


def get_version():
    path = _ROOT / 'sfera' / '__init__.py'
    text = path.read_text()
    version = re.search(r"version = '(.*?)'", text).group(1)
    return version


def get_readme():
    path = _ROOT / 'README.md'
    return path.read_text()


def get_project_config():
    path = _ROOT / 'project.json'
    with path.open() as fp:
        return json.load(fp) or {}


def get_dependencies():
    config = get_project_config()
    return config.get('dependencies') or []


def get_package_config():
    return dict(
        name = 'sfera',
        version = get_version(),
        author = 'SFERA Institute',
        author_email = 'hello@sfera.institute',
        description = "SFERA Institute's Python codebase.",
        long_description = get_readme(),
        long_description_content_type = 'text/markdown',
        url = _GITHUB_URL,
        project_urls = {
            'Documentation': _GITHUB_URL,
            'Source': _GITHUB_URL,
            'Tracker': f'{_GITHUB_URL}/issues',
        },
        packages = setuptools.find_packages(),
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        python_requires = '>=3.6',
        install_requires = get_dependencies() + [
            'click',
            'mkdocs',
        ],
        tests_require = [
            'pytest',
            'pytest-cov',
        ],
    )


if __name__ == '__main__':
    config = get_package_config()
    setuptools.setup(**config)