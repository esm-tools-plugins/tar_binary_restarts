import os
import yaml
import os
import subprocess
import time
import pdb
import glob

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
    tar_binary_restarts = config["fesom"]["tar_binary_restarts"]

    if tar_binary_restarts:
        workdir = config["general"]["thisrun_work_dir"]
        nproc = config["fesom"]["nproc"]
        cpn = config["computer"]["partitions"]["compute"]["cores_per_node"]
        if os.path.isdir(workdir):
            os.chdir(workdir)
        else:
            Print(f"Warning: {workdir} does not exists. Will skip this plugin.")
            return

        bin_restart_dirs = ["fesom_bin_restart", "fesom_raw_restart"]
        for restart_dir in bin_restart_dirs:
            if os.path.isdir(f"{workdir}{restart_dir}"):
                # Check if restart folder is not empty
                if os.listdir(restart_dir):
                    tar_name = f"{restart_dir}.tar.gz"
                    output = subprocess.run([f'tar cf - {restart_dir} | pigz -p {cpn} > {tar_name}'], shell=True)
#                  if output:
#                        print(f"Successfully tarred {restart_dir}")
                else:
                    print(f"Warning: {restart_dir} is empty.")
            #else:
            #    print(f"Warning: No {restart_dir} to tar.")

        et = time.time()
        elapsed_time = et - st

        print(f"Plugin tar_binary_restarts fininshed. Execution time: {elapsed_time} seconds.")


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
