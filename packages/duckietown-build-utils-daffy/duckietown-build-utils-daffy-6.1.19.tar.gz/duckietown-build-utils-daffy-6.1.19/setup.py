from setuptools import setup


def get_version(filename: str) -> str:
    import ast

    version = None
    with open(filename) as f:
        for line_ in f:
            if line_.startswith("__version__"):
                version = ast.parse(line_).body[0].value.s
                break
        else:
            raise ValueError(f"No version found in {filename!r}.")
    if version is None:
        raise ValueError(filename)
    return version


fversion = get_version(filename="src/duckietown_build_utils/__init__.py")

install_requires = (["requirements-parser", "zuper-commons-z6", "packaging", "pytz", "whichcraft"],)

line = "daffy"

setup(
    name=f"duckietown-build-utils-{line}",
    version=fversion,
    keywords="",
    package_dir={"": "src"},
    packages=["duckietown_build_utils"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "aido-update-reqs=duckietown_build_utils.update_req_versions:update_reqs_versions_main",
            "aido-dir-status=duckietown_build_utils:aido_dir_status_main",
            "aido-check-tagged=duckietown_build_utils:aido_check_tagged_main",
            "aido-check-not-dirty=duckietown_build_utils:aido_check_not_dirty_main",
            "aido-check-need-upload=duckietown_build_utils:aido_check_need_upload_main",
            "aido-labels=duckietown_build_utils:aido_labels_main",
            "dt-update-reqs=duckietown_build_utils.update_req_versions:update_reqs_versions_main",
            "dt-dir-status=duckietown_build_utils:aido_dir_status_main",
            "dt-check-tagged=duckietown_build_utils:aido_check_tagged_main",
            "dt-check-not-dirty=duckietown_build_utils:aido_check_not_dirty_main",
            "dt-check-need-upload=duckietown_build_utils:aido_check_need_upload_main",
            "dt-labels=duckietown_build_utils:aido_labels_main",
        ],
    },
)
