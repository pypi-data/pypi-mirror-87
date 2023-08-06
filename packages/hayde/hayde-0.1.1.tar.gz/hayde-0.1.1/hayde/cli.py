import argparse
import os
import sys

from . import __version__
from .config import get_configuration_and_validate
from .outputs import load_output_config, generate_files
from .inputs import get_all_proper_k8s_services


def main():
    parser = argparse.ArgumentParser(prog="Hayde", description="Hayde")
    parser.add_argument("--config-file", required=True)
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    args = parser.parse_args()

    config_file = args.config_file
    config = get_configuration_and_validate(config_file)

    loaded_output_config = load_output_config(config=config["output"])

    input_name = config["input"]["name"]
    if input_name == "k8s":
        all_proper_k8s_services = get_all_proper_k8s_services(
            k8s_configs=config["input"]
        )
        generate_files(
            output_config=loaded_output_config, k8s_services=all_proper_k8s_services
        )
    else:
        sys.exit(f"We only support k8s as input for now!")
