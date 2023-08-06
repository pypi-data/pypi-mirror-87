import os
import sys
import time
import traceback

from docker import DockerClient
from docker.errors import APIError
from zuper_commons.types import ZException

from . import logger

__all__ = ["run_build", "BuildFailed"]


class BuildFailed(ZException):
    pass


def run_build(client: DockerClient, rm=True, **kwargs):
    """

    """
    while True:
        try:
            run_build_(client, rm=rm, **kwargs)
        except BuildFailed as e:
            s = str(e)
            if "net/http" in s or "i/o" in s:
                logger.error("looks like it failed because of network; retrying.")
                time.sleep(2)
            else:
                raise
        else:
            break


def run_build_(client: DockerClient, **kwargs):
    """ Raises BuildFailed """
    logger.info("now running build", cwd=os.getcwd(), kwargs=kwargs)
    try:
        for line in client.api.build(**kwargs, decode=True):
            # logger.debug(line=line)
            line = _build_line(line)
            if line is not None:
                sys.stderr.write(line)
            sys.stderr.flush()

    except APIError as e:
        logger.error(traceback.format_exc())
        msg = "An error occurred while building the project image."
        raise BuildFailed(msg, kwargs=kwargs) from e
    except ProjectBuildError as e:
        logger.error(traceback.format_exc())
        se = str(e)
        timeout = "Client.Timeout" in se or "i/o timeout" in se
        if timeout:
            msg = f"Docker timeout while building the image:\n{e}"
            raise BuildFailed(msg) from None

        msg = f"An error occurred while building the project image."
        raise BuildFailed(msg, kwargs=kwargs) from e
    except:
        logger.error(traceback.format_exc())
        raise
    finally:
        sys.stderr.flush()


class ProjectBuildError(ZException):
    pass


def _build_line(line: dict):
    # logger.info(line=line)
    if "error" in line and "errorDetail" in line:
        msg = line["errorDetail"]["message"]
        logger.error(msg)
        raise ProjectBuildError(msg)
    if "status" in line:
        # logger.info(line['status'])
        return line["status"]
    if "stream" not in line:
        return None
    line = line["stream"].strip("\n")
    if not line:
        return None
    # this allows apps inside docker build to clear lines
    if not line.endswith("\r"):
        line += "\n"
    # ---
    return line
