import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "aiops-scania-pressure-brakes-prediction"
AUTHOR_USER_NAME = "imkushwaha"
SRC_REPO = "src"
AUTHOR_EMAIL = "datascienceworks455@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    author_email=AUTHOR_EMAIL,
    description="A small python package",
    long_description=long_description,
    url=f"https://github.com/{AUTHOR_USER_NAME}/{SRC_REPO}",
    project_url = {
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    package_dir={"": "src"}, 
    packages=setuptools.find_packages(where="src")
)