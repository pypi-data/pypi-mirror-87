from typing import NewType

__all__ = [
    "DockerRegistryName",
    "DockerOrganizationName",
    "DockerRepositoryName",
    "DockerTag",
    "DockerImageDigest",
    "DockerCompleteImageName",
]

DockerRegistryName = NewType("DockerCompleteImageName", str)

DockerOrganizationName = NewType("DockerOrganizationName", str)
DockerRepositoryName = NewType("DockerRepositoryName", str)
DockerTag = NewType("DockerTag", str)
DockerImageDigest = NewType("DockerImageDigest", str)

DockerCompleteImageName = NewType("DockerCompleteImageName", str)
