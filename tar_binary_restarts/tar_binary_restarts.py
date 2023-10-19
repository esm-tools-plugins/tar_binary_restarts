import os
import yaml
import os
import subprocess
import time
import pdb
from esm_parser import user_note

def tar_binary_restarts(config, test_config=None):
    """
    Tar binary restart files.

    Parameters
    ----------
    config : dict

    Returns
    -------
    None

    """

    st = time.time()
    tar_binary_restarts = config["fesom"].get("tar_binary_restarts", False)

    if tar_binary_restarts:
        workdir = config["general"]["thisrun_work_dir"]
        cpn = config["computer"]["partitions"]["compute"]["cores_per_node"]
        if not os.path.isdir(workdir):
            user_note(f"WARNING: Missing workdir:", f"``{workdir}`` does not exists. Will skip this plugin.")
            return config

        bin_restart_dirs = ["fesom_bin_restart", "fesom_raw_restart"]
        check = False
        for restart_dir in bin_restart_dirs:
            if os.path.isdir(f"{workdir}/{restart_dir}"):
                # Check if restart folder is not empty
                if os.listdir(f"{workdir}/{restart_dir}"):
                    check = True
                    tar_name = f"{restart_dir}.tar.gz"
                    output = subprocess.run([f'tar cf - {workdir}/{restart_dir} | pigz -p {cpn} > {workdir}/{tar_name}'], shell=True)
                    if output.returncode == 0:
                        user_note(f"SUCCESS:", f"Successfully tarred {restart_dir}.")
                    else:
                        user_note(f"WARNING:", f"There has been an error occuring during taring of binary restart files.")
                else:
                    user_note(f"WARNING: No binary restart files:", f"{restart_dir} is empty.")
        if not check:
            user_note(f"WARNING: No binary restart folder:", "No folder of binary restart files found.")

        et = time.time()
        elapsed_time = et - st

        user_note(f"Plugin tar_binary_restarts fininshed.", f"Execution time: {elapsed_time} seconds.")

        return config


if __name__ == "__main__":
    """
        Script to use when executing externally to a simulation.
    """

    import argparse

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
