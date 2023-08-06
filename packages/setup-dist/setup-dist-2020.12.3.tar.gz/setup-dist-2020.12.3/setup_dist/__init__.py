import os
import setuptools


def get_name():
    return os.getenv('SETUP_NAME', os.path.basename(os.getcwd()).split(".")[0].lower())


def get_packages():
    if 'SETUP_PACKAGES' in os.environ:
        return os.getenv('SETUP_PACKAGES').replace(',', '\n').splitlines()
    return setuptools.find_packages()


def get_install_requires():
    if 'SETUP_INSTALL_REQUIRES' in os.environ:
        return os.getenv('SETUP_INSTALL_REQUIRES').replace(',', '\n').splitlines()
    if 'SETUP_INSTALL_REQUIRES_FILE' in os.environ:
        return open(os.getenv('SETUP_INSTALL_REQUIRES_FILE')).read().splitlines()
    if os.path.exists('requirements.txt'):
        return open('requirements.txt').read().splitlines()
    return []


def get_keywords():
    if 'SETUP_KEYWORDS' in os.environ:
        return os.environ.get('SETUP_KEYWORDS').strip()
    if 'SETUP_KEYWORDS_FILE' in os.environ:
        return open(os.environ.get('SETUP_KEYWORDS_FILE')).read().strip()


def get_description():
    if 'SETUP_DESCRIPTION' in os.environ:
        return os.environ.get('SETUP_DESCRIPTION').strip()
    if 'SETUP_DESCRIPTION_FILE' in os.environ:
        return open(os.environ.get('SETUP_DESCRIPTION_FILE')).read().strip()


def get_long_description():
    if 'SETUP_LONG_DESCRIPTION' in os.environ:
        return os.environ.get('SETUP_LONG_DESCRIPTION').strip()
    if 'SETUP_LONG_DESCRIPTION_FILE' in os.environ:
        return open(os.environ.get('SETUP_LONG_DESCRIPTION_FILE')).read().strip()
    for path in ['README.md', 'README.rst']:
        if os.path.exists(path):
            return open(path).read()


def get_long_description_content_type():
    if '.md' in os.getenv('SETUP_LONG_DESCRIPTION_FILE', '') or os.path.exists('README.md'):
        return "text/markdown"


def get_classifiers():
    if 'SETUP_CLASSIFIERS' in os.environ:
        return list(filter(None, os.getenv('SETUP_CLASSIFIERS').splitlines()))
    if 'SETUP_CLASSIFIERS_FILE' in os.environ:
        return list(filter(None, open(os.getenv('SETUP_CLASSIFIERS_FILE')).read().splitlines()))
    if os.path.exists('classifiers.txt'):
        return open('classifiers.txt').read().splitlines()
    return []


def get_scripts():
    """return `scripts` list. `bin/`, `scripts/` files"""
    if 'SETUP_SCRIPTS' in os.environ:
        return os.getenv('SETUP_SCRIPTS').replace(',', '\n').splitlines()
    result = []
    exclude = ['.DS_Store', 'Icon\r']
    for path in ["scripts"]:
        if os.path.exists(path) and os.path.isdir(path):
            files = list(
                filter(lambda f: f not in exclude, os.listdir(path)))
            result += list(map(lambda f: os.path.join(path, f), files))
    return result


def get_kwargs():
    return dict(
        name=get_name(),
        version=os.getenv('SETUP_VERSION', None),
        keywords=get_keywords(),
        description=get_description(),
        long_description=get_long_description(),
        long_description_content_type=get_long_description_content_type(),
        license=os.getenv('SETUP_LICENSE'),
        url=os.environ.get('SETUP_URL', None),
        install_requires=get_install_requires(),
        classifiers=get_classifiers(),
        packages=get_packages(),
        scripts=get_scripts()
    )
