import os
import subprocess
import time
from esm_parser import user_note

def tar_binary_restarts(config, test_config=None):
    """
    Tar and compression of FESOM-2 binary restart files

    Parameters
    ----------
    config : dict

    Returns
    -------
    config : dict

    """

    st = time.time()
    tar_binary_restarts = config["fesom"].get("tar_binary_restarts", False)

    if tar_binary_restarts:
        workdir = config["general"]["thisrun_work_dir"]
        cpn = config["computer"]["partitions"]["compute"]["cores_per_node"]
        # Check, if workdir exists. If not, the plugin will be aborted.
        if not os.path.isdir(workdir):
            user_note(f"WARNING: Missing workdir:", f"``{workdir}`` does not exists. Will skip this plugin.")
            return config

        # The plugin will tar both of the following folders, if present.
        # This may change in the future according to changes in Fesom.
        bin_restart_dirs = ["fesom_bin_restart", "fesom_raw_restart"]
        check = False
        for restart_dir in bin_restart_dirs:
            if os.path.isdir(f"{workdir}/{restart_dir}"):
                check = True
                # Check if restart folder is not empty.
                if os.listdir(f"{workdir}/{restart_dir}"):
                    tar_name = f"{restart_dir}.tar.gz"
                    # Run tar and pigz commands for taring and parallel compression.
                    output = subprocess.run([f'tar cf - {workdir}/{restart_dir} | pigz -p {cpn} > {workdir}/{tar_name}'], shell=True)
                    if output.returncode == 0:
                        user_note(f"SUCCESS:", f"Successfully tarred ``{restart_dir}`` in {workdir}.")
                    else:
                        # Raise warning when an error during tar and pgiz command occured.
                        user_note(f"WARNING:", f"An ``ERROR`` occurred when taring binary restart files in {workdir}.")
                # Raise warning when restart folder is empty.
                else:
                    user_note(f"WARNING: No binary restart files.", f"The folder ``{restart_dir}`` in {workdir} is empty.")
        # Raise warning when no restart folders found.
        if not check:
            user_note(f"WARNING: No binary restart folder found.", f"No folder of binary restart files found in {workdir}.")

        et = time.time()
        elapsed_time = et - st

        user_note(f"Plugin tar_binary_restarts fininshed.", f"Execution time: {elapsed_time} seconds.")

    else:
        user_note(f"Plugin tar_binary_restarts fininshed, but did nothing.", f"To enable this plugin, please set ``tar_binary_restarts: true`` in the fesom section of e.g. the runstript.")

    return config


if __name__ == "__main__":
    """
        Script to use when executing externally to a simulation.
    """

    import argparse
    import yaml

    # Parse input
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", default=None, help="config file to use for testing")

    parsed_args = vars(parser.parse_args())
    config_file = parsed_args["config_file"]

    if os.path.isfile(config_file):
        with open(config_file, "r") as cf:
            config = yaml.load(cf, Loader=yaml.FullLoader)
        if "dictitems" in config:
            config = config["dictitems"]
        tar_binary_restarts(config)
    else:
        print(f"The 'config_file' specified ({config_file}) does not exist")
        sys.exit(0)
