import os
import yaml
import os
import subprocess
import time

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

    workdir = config["general"]["work_dir"]
    nproc = config["fesom"]["nproc"]
    nproc_on_node = config["computer"]["partition_cpn"]
    os.chdir(workdir)
    bin_restart_dir = "fesom_raw_restart"
    #bin_restart_dir = "fesom_bin_restart"
    os.chdir(bin_restart_dir)
    tar_name = f"np{nproc}.tar.gz"
    output = subprocess.run([f'tar cf - *{nproc}* | pigz -p {nproc_on_node} > {tar_name}'], shell=True)

    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


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
