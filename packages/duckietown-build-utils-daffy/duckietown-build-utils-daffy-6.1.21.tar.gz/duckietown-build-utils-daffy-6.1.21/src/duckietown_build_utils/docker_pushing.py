import os
import sys
import time
import traceback
from dataclasses import replace
from typing import Optional

import yaml
from docker import DockerClient
from zuper_commons.fs import write_ustring_to_utf8_file
from zuper_commons.types import ZException

from . import logger
from .buildresult import get_complete_tag, parse_complete_tag
from .types import DockerCompleteImageName, DockerImageDigest


__all__ = ["docker_push_optimized", "docker_push_retry", "DockerPushFailure"]


def docker_push_retry(client: DockerClient, image_name: DockerCompleteImageName) -> DockerImageDigest:
    while True:
        # noinspection PyBroadException
        try:
            # logger.info(f"Pushing {image_name}")
            return push_image(client, image_name, progress=True)
        except:
            logger.error(traceback.format_exc())
            logger.error("retrying in 5 seconds")
            time.sleep(5)


class DockerPushFailure(ZException):
    pass


def docker_push_optimized(image_name: DockerCompleteImageName) -> DockerCompleteImageName:
    """ Returns the *complete tag* for the image  "a/b:@sha256:...". Without tags. """
    client = DockerClient.from_env()

    image = client.images.get(image_name)
    image_name_no_tag, _, _ = image_name.partition(":")
    # XXX: apparently docker does not store 'docker.io'
    image_name_no_tag = image_name_no_tag.replace("docker.io/", "")
    # RepoTags = image.attrs["RepoTags"]
    # RepoTags = [_ for _ in RepoTags if _.startswith(image_name_no_tag)]
    RepoDigests = image.attrs["RepoDigests"]
    RepoDigests = [_ for _ in RepoDigests if _.startswith(image_name_no_tag)]
    # logger.debug(f"RepoTags {RepoTags}")
    # logger.debug(f"RepoDigests {RepoDigests}")

    if RepoDigests and ("DT_PUSH_OPT" in os.environ):
        logger.debug(f"RepoDigests already present; skipping pushing: {RepoDigests}")
        return RepoDigests[0]
    digest_from_push = docker_push_retry(client, image_name)

    f = parse_complete_tag(image_name)
    f = replace(f, tag=None, digest=digest_from_push)
    return get_complete_tag(f)
    #
    # S = 4
    # logger.info(f"Now waiting {S} seconds for reg to update.")
    # time.sleep(S)
    # client = DockerClient.from_env()
    #
    # image = client.images.get(image_name)
    # RepoTags = image.attrs["RepoTags"]
    # # RepoTags = [_ for _ in RepoTags if _.startswith(image_name_no_tag)]
    #
    # RepoDigests = image.attrs["RepoDigests"]
    # RepoDigests = [_ for _ in RepoDigests if _.startswith(image_name_no_tag)]
    #
    # if not RepoDigests:
    #     msg = f"cannot find compatible digests (starts with {image_name_no_tag})"
    #     raise DockerPushFailure(msg, attrs=dict(image.attrs))
    # # logger.debug(f"Updated RepoTags {RepoTags}")
    # # logger.debug(f"Updated RepoDigests {RepoDigests}")
    #
    # res = RepoDigests[0]
    # logger.debug(f"from client {res} from push {digest_from_push}")
    # return res
    # # for line in client.images.push(image_name, stream=True):
    # #     process_docker_api_line(line.decode())


def push_image(
    client: DockerClient, image_name: DockerCompleteImageName, progress: bool
) -> DockerImageDigest:
    layers = set()
    pushed = set()
    logger.info(f"Pushing image {image_name}.")
    tag = parse_complete_tag(image_name)
    image_name_short = f"{tag.repository}"

    layer2size = {}
    layer2done = {}

    update_interval = 2
    last_update = 0.0
    # last_ps = ''
    last_progress = ""
    nlines = 0
    spinner = list("◐◓◑◒")
    all_lines = []
    final_digest: Optional[DockerImageDigest] = None
    for line in client.images.push(image_name, stream=True, decode=True):
        all_lines.append(line)
        nlines += 1
        # logger.info(line=line)
        # percentage = max(0.0, min(1.0, len(pushed) / max(1.0, len(layers)))) * 100.0
        if "error" in line:
            raise DockerPushFailure(str(line["error"]))

        if "aux" in line:
            if "Digest" in line["aux"]:
                final_digest = DockerImageDigest(line["aux"]["Digest"])

        # aux:
        # Tag: daffy - amd64
        # Digest: sha256:a4c1b0756713ad2201d1b5588ea527ebd69e01cddf8df1d81a36885d4dad67cc
        # Size: 5984
        if "progress" in line:
            last_progress = line["progress"]
        if "id" in line:
            layer_id = line["id"]
            layers.add(layer_id)
            if "progressDetail" in line:
                progd = line["progressDetail"]
                if progd:
                    if "current" in progd:
                        current = progd["current"]
                    else:
                        current = 0
                    if "total" in progd:
                        total = progd["total"]
                    else:
                        total = 1
                    # total = line['progressDetail']['total']
                    layer2size[layer_id] = total
                    layer2done[layer_id] = current
            if "status" in line:
                if line["status"] in ["Layer already exists", "Pushed"]:
                    pushed.add(layer_id)

        if layers:
            fraction_layers_done = float(len(pushed)) / len(layers)
        else:
            fraction_layers_done = 0.0
        # total_bytes = sum(layer2size.values())
        # bytes_done = sum(layer2done.values())
        # if total_bytes:
        #     fraction_bytes_done = float(bytes_done) / total_bytes
        # else:
        #     fraction_bytes_done = 0.0

        now = time.time()

        # def fancy(x):
        #     y = x / (1000 * 1000.0)
        #     return f"{int(y)} MB"

        lprogress = f"{fraction_layers_done * 100:4.1f}% ({len(pushed):3}/{len(layers):3})"
        # bprogress = f"{fraction_bytes_done * 100:4.1f}% ({fancy(bytes_done)}/{fancy(total_bytes)})"

        spinneri = spinner[nlines % len(spinner)]
        ps = f"%[pushing {image_name_short}] {lprogress} {spinneri} {last_progress}"

        if progress:
            if now - last_update >= update_interval:  # or last_ps != ps:
                last_update = now
                # last_ps = ps

                sys.stderr.write(ps + "\n")
                sys.stderr.flush()

    logger.debug(f"Push successful.", image_name=image_name, final_digest=final_digest)

    fn = "/tmp/duckietown/dt-build-utils/" + tag.repository + ".push_history.yaml"
    write_ustring_to_utf8_file(yaml.dump(all_lines), fn)
    return final_digest
