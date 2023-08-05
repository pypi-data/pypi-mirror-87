import sys, argparse

from omg import version
from omg.cmd.use import use
from omg.cmd.project import project, projects
from omg.cmd.get_main import get_main
from omg.cmd.describe import describe
from omg.cmd.log import log
from omg.cmd.whoami import whoami
from omg.cmd.machine_config import machine_config

# Process the Arguments and call the respective functions
def main():
    # Common parser, with shared arguments for all subcommands:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-n", "--namespace", dest="namespace")
    common.add_argument("-A", "--all-namespaces", dest="all_namespaces",action='store_true')

    # Main Parser for sub commands
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # omg use </path/to/must-gather>
    p_use = subparsers.add_parser('use',
                                  help='Select the must-gather to use')
    p_use.add_argument('mg_path', metavar='</must/gather/location>', type=str, nargs='?')
    p_use.add_argument('--cwd', dest="cwd", action='store_true')
    p_use.set_defaults(func=use)

    # omg project
    p_project = subparsers.add_parser('project', parents=[common],
                                      help='Display information about the current active project and existing projects')
    p_project.add_argument('project', nargs='?', type=str)
    p_project.set_defaults(func=project)

    # omg projects
    p_projects = subparsers.add_parser('projects', parents=[common],
                                       help='Display information about the current active project and existing projects')
    p_projects.set_defaults(func=projects)

    # omg get <object(s)>
    p_get = subparsers.add_parser('get', parents=[common],
                                  help='Display one or many resources')
    p_get.add_argument('objects', nargs='*', type=str)
    p_get.add_argument("-o", "--output", dest="output",
                       choices=['yaml', 'json', 'wide'] )
    p_get.set_defaults(func=get_main)

    # omg describe <object(s)>
    p_describe = subparsers.add_parser('describe', parents=[common],
                                       help='This command joins many API calls together to form a detailed description of a given resource.')
    p_describe.add_argument('object', nargs='*', type=str)
    p_describe.set_defaults(func=describe)

    # omg log <pod>
    p_log = subparsers.add_parser('log', aliases=['logs'], parents=[common],
                                  help='Display logs')
    p_log.add_argument('resource', type=str)
    p_log.add_argument("-c", "--container", dest="container")
    p_log.add_argument("-p", "--previous", dest="previous", action='store_true')
    p_log.set_defaults(func=log)

    # omg whoami
    p_whoami = subparsers.add_parser('whoami', parents=[common],
                                  help='Display who you are')
    p_whoami.set_defaults(func=whoami)

    # omg version
    p_version = subparsers.add_parser('version', parents=[common],
                                    help='Display omg version')
    p_version.set_defaults(func=lambda x: print('omg version '+version+' (https://github.com/kxr/o-must-gather)'))

    # omg machine-config
    p_mc = subparsers.add_parser('machine-config',
                                    help='Explore Machine Configs')
    p_mc.add_argument('mc_op', metavar='operation', type=str,choices=['extract', 'show', 'compare'],
        help='Operation to be performed on the machine-config (extract/show/compare)')
    p_mc.add_argument('mc_names', metavar='name', type=str, nargs='*',
        help='Machine Config name (skip this to process all machine-configs')
    p_mc.add_argument("--show-contents", dest="show_contents", action='store_true')
    p_mc.set_defaults(func=machine_config)

    # process args and call the corresponding function
    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)
