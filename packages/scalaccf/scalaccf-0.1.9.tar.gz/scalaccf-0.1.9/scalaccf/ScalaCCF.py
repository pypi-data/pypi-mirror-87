from scalaccf import utility
from scalaccf.ccf import CCF


def main():
    argument_parser = utility.setup_argument_parser()
    args = argument_parser.parse_args()

    path_arg = utility.get_argument(['p', 'd', 'f'], args)
    mode = utility.get_argument(['verify', 'trace'], args)

    files = utility.get_files(args, path_arg)
    ccf = CCF(files)

    if mode == 'verify':
        # verify file and dirs namings
        ccf.verify()
        pass
    elif mode == 'trace':
        # fix file and dirs namings
        ccf.fix()
        pass
