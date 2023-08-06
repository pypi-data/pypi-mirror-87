# -*- coding: utf-8 -*-
"""Command line interface build (no sub-commands)."""

import json
from pathlib import Path
import os
import platform
import shutil
import sys
import sysconfig
from types import SimpleNamespace

import click
import numpy.f2py

from et_micc.project import Project, micc_version
import et_micc.logger
import et_micc.utils


def get_extension_suffix():
    """Return the extension suffix, e.g. :file:`.cpython-37m-darwin.so`."""
    return sysconfig.get_config_var('EXT_SUFFIX')


def build_f2py(module_name, args=[]):
    """
    :param Path path: to f90 source
    """
    so_file = Path(module_name+get_extension_suffix())

    src_file = module_name + '.f90'

    path_to_src_file = Path(src_file).resolve()
    if not path_to_src_file.exists():
        raise FileNotFoundError(str(path_to_src_file))

    f2py_args = [
        '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION',
        '-DF2PY_REPORT_ON_ARRAY_COPY=1',
        '--build-dir', '_f2py_build',
    ]
    f2py_args.extend(args)

    with open(str(path_to_src_file.name)) as f:
        fsource = f.read()
    returncode = numpy.f2py.compile(fsource, extension='.f90', modulename=module_name, extra_args=f2py_args,
                                    verbose=True)

    return returncode


def check_cxx_flags(cxx_flags, cli_option):
    """
    :param str cxx_flags: C++ compiler flags
    :param str cli_option: typically '--cxx-flags', or '--cxx-flags-all'.
    :raises: RunTimeError if cxx_flags starts or ends with a '"' but not both.
    """
    if cxx_flags.startswith('"') and cxx_flags.endswith('"'):
        # compile options appear between quotes
        pass
    elif not cxx_flags.startswith('"') and not cxx_flags.endswith('"'):
        # a single compile option must still be surrounded with quotes.
        cxx_flags = f'"{cxx_flags}"'
    else:
        raise RuntimeError(f"{cli_option}: unmatched quotes: {cxx_flags}")
    return cxx_flags


def path_to_cmake_tools():
    """Return the path to the folder with the CMake tools."""

    # p = (Path(__file__) / '..' / 'cmake_tools').resolve()
    p = (Path(__file__) / '..' / '..' / 'pybind11' / 'share' / 'cmake' / 'pybind11').resolve()

    return str(p)


def check_load_save(filename, loadorsave):
    """
    :param str filename: possibly empty string.
    :param str loadorsave: 'load'|'save'.
    :raises: RunTimeError if filename is actually a file path.
    """
    if filename:
        if os.sep in filename:
            raise RuntimeError(f"--{loadorsave} {filename}: only filename allowed, not path.")
        if not filename.endswith('.json'):
            filename += '.json'
    return filename


def auto_build_binary_extension(package_path, module_to_build):
    """Set options for building binary extensions, and build
    binary extension *module_to_build* in *package_path*.

    :param Path package_path:
    :param str module_to_build:
    :return: exit_code
    """
    options = SimpleNamespace(
        package_path=package_path,
        module_name=module_to_build,
        build_options=SimpleNamespace(
            clean=False,
            save="",
            load="build_options",
            soft_link=True,
        ),
        verbosity=1,
    )
    for module_prefix in ["cpp", "f2py"]:
        module_srcdir_path = package_path / f"{module_prefix}_{options.module_name}"
        if module_srcdir_path.exists():
            options.module_kind = module_prefix
            options.module_srcdir_path = module_srcdir_path
            options.build_options.build_tool_options = {}
            break
    else:
        raise ValueError(f"No binary extension source directory found for module '{module_to_build}'.")

    exit_code = build_binary_extension(options)

    msg = ("[ERROR]\n"
           "    Binary extension module 'bar{get_extension_suffix}' could not be build.\n"
           "    Any attempt to use it will raise exceptions.\n"
           ) if exit_code else ""
    return msg


def build_binary_extension(options):
    """Build a binary extension described by *options*.

    :param options:
    :return:
    """
    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = get_extension_suffix()

    build_options = options.build_options
    if build_options.save:
        build_options.save = build_options.save.replace(f".{platform.system()}", "").replace(".json", "")
        build_options.save += f".{platform.system()}.json"

    if build_options.load:
        build_options.load = build_options.save.replace(f".{platform.system()}", "").replace(".json", "")
        build_options.load += f".{platform.system()}.json"

    # Remove so file to avoid "RuntimeError: Symlink loop from ..."
    so_file = options.package_path / (options.module_name + extension_suffix)
    try:
        so_file.unlink() # missing_ok=True only available from 3.8 on, not in 3.7
    except FileNotFoundError:
        pass

    build_log_file = options.module_srcdir_path / "micc-build.log"
    build_logger = et_micc.logger.create_logger(build_log_file, filemode='w')
    with et_micc.logger.log(build_logger.info, f"Building {options.module_kind} module '{options.module_name}':"):
        binary_extension = options.module_name + extension_suffix
        destination = (options.package_path / binary_extension).resolve()

        # if build_options.save:
        #     with open(str(options.module_srcdir_path / build_options.save), 'w') as f:
        #         json.dump(build_options.build_tool_options, f)

        if build_options.load:
            path_to_load = options.module_srcdir_path / build_options.load
            if path_to_load.exists():
                build_logger.info(f"Loading build options from {path_to_load}")
                with open(str(path_to_load), 'r') as f:
                    build_options.build_tool_options = json.load(f)
            else:
                build_logger.info(f"Building using default build options.")

        if options.module_kind in ('cpp','f2py') and (options.module_srcdir_path / 'CMakeLists.txt').exists():
            output_dir = options.module_srcdir_path / '_cmake_build'
            build_dir = output_dir
            if build_options.clean:
                build_logger.info(f"--clean: shutil.removing('{output_dir}').")
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            with et_micc.utils.in_directory(output_dir):
                cmake_cmd = ['cmake',
                             '-D', f"PYTHON_EXECUTABLE={sys.executable}",
                             '-D', f"pybind11_DIR={path_to_cmake_tools()}",
                             ]
                for key, val in build_options.build_tool_options.items():
                    cmake_cmd.extend(['-D', f"{key}={val}"])
                cmake_cmd.append('..')
                cmds = [
                    cmake_cmd,
                    ['make'],
                    ['make', 'install']
                ]
                exit_code = et_micc.utils.execute(
                    cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy()
                )
                if build_options.cleanup:
                    build_logger.info(f"--cleanup: shutil.removing('{build_dir}').")
                    shutil.rmtree(build_dir)

        elif options.module_kind == 'f2py':
            # the old way, i.e. without CMakeLists.txt file (deprecated)
            f2py_args = []
            for arg, val in build_options.build_tool_options.items():
                if val is None:
                    # this is a flag
                    f2py_args.append(arg)
                else:
                    f2py_args.append(f"{arg}=\"{val}\"")

            with et_micc.utils.in_directory(options.module_srcdir_path):
                if build_options.clean:
                    build_logger.info(f"--clean: removing {options.module_srcdir_path}/_f2py_build")
                    shutil.rmtree('_f2py_build')
                exit_code = build_f2py(options.module_name, args=f2py_args)
            if exit_code == 0:
                output_dir = options.module_srcdir_path
                built = output_dir / binary_extension
                build_dir = output_dir / '_f2py_build'
                if build_options.cleanup:
                    shutil.rmtree(build_dir)

        if build_options.save:
            with (options.module_srcdir_path / build_options.save).open('w') as f:
                json.dump(build_options.build_tool_options, f)

    return exit_code

def build_cmd(project):
    """
    Build binary extensions, i.e. f2py modules and cpp modules.

    :param str module_to_build: name of the only module to build (the prefix
        ``cpp_`` or ``f2py_`` may be omitted). If not provided, all binrary
        extensions are built.
    :param types.SimpleNamespace options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are

        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **build_options**: all build options.
    """
    project_path = project.options.project_path
    if getattr(project, 'module', False):
        project.warning(
            f"Nothing to do. A module project ({project.project_name}) cannot have binary extension modules."
        )

    build_options = project.options.build_options

    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = get_extension_suffix()

    package_path = project.options.project_path / project.package_name
    dirs = os.listdir(package_path)
    succeeded = []
    failed = []
    for d in dirs:
        if ((package_path / d).is_dir()
                and (d.startswith("f2py_") or d.startswith("cpp_"))
        ):
            if project.options.module_to_build and not d.endswith(project.options.module_to_build):
                # build only module module_to_build.
                continue

            module_kind, module_name = d.split('_', 1)
            binary_extension = package_path / (module_name + extension_suffix)
            project.options.module_srcdir_path = package_path / d
            project.options.module_kind = module_kind
            project.options.module_name = module_name
            project.options.package_path = package_path
            project.options.build_options.build_tool_options = getattr(project.options.build_options, module_kind)
            project.exit_code = build_binary_extension(project.options)

            if project.exit_code:
                failed.append(binary_extension)
            else:
                succeeded.append(binary_extension)
    build_logger = project.logger
    if succeeded:
        build_logger.info("\n\nBinary extensions built successfully:")
        for binary_extension in succeeded:
            build_logger.info(f"  - {binary_extension}")
    if failed:
        build_logger.error("\nBinary extensions failing to build:")
        for binary_extension in failed:
            build_logger.error(f"  - {binary_extension}")
    if not succeeded and not failed:
        project.warning(
            f"No binary extensions found in package ({project.package_name})."
        )


@click.command()
@click.option('-v', '--verbosity', count=True
    , help="The verbosity of the program."
    , default=1
              )
@click.option('-p', '--project-path'
    , help="The path to the project directory. "
           "The default is the current working directory."
    , default='.'
    , type=Path
              )
@click.option('-m', '--module'
    , help="Build only this module. The module kind prefix (``cpp_`` "
           "for C++ modules, ``f2py_`` for Fortran modules) may be omitted."
    , default=''
              )
@click.option('-b', '--build-type'
    , help="build type: For f2py modules, either RELEASE or DEBUG, where the latter "
           "toggles the --debug, --noopt, and --noarch, and ignores all other "
           "f2py compile flags. For cpp modules any of the standard CMake build types: "
           "DEBUG, MINSIZEREL, RELEASE, RELWITHDEBINFO."
    , default='RELEASE'
              )
@click.option('--cleanup'
    , help="Cleanup build directory after successful build."
    , default=False, is_flag=True
              )

# F2py specific options
@click.option('--f90exec'
    , help="F2py: Specify the path to F90 compiler."
    , default=''
              )
@click.option('--f90flags'
    , help="F2py: Specify F90 compiler flags."
    , default='-O3'
              )
@click.option('--opt'
    , help="F2py: Specify optimization flags."
    , default=''
              )
@click.option('--arch'
    , help="F2py: Specify architecture specific optimization flags."
    , default=''
              )
@click.option('--debug'
    , help="F2py: Compile with debugging information."
    , default=False, is_flag=True
              )
@click.option('--noopt'
    , help="F2py: Compile without optimization."
    , default=False, is_flag=True
              )
@click.option('--noarch'
    , help="F2py: Compile without architecture specific optimization."
    , default=False, is_flag=True
              )
# Cpp specific options: none (must use the module's CMakeLists.txt file)
# @click.option('--cxx-compiler'
#     , help="CMake: specify the C++ compiler (sets CMAKE_CXX_COMPILER)."
#     , default=''
#               )
# @click.option('--cxx-flags'
#     , help="CMake: set CMAKE_CXX_FLAGS_<built_type> to <cxx_flags>."
#     , default=''
#               )
# @click.option('--cxx-flags-all'
#     , help="CMake: set CMAKE_CXX_FLAGS_<built_type> to <cxx_flags>."
#     , default=''
#               )
# Other options
@click.option('--clean'
    , help="Perform a clean build."
    , default=False, is_flag=True
              )
@click.option('--load'
    , help="Load the build options from a f'.{platform.system()}.json' file in the module directory. "
           "All other compile options are ignored."
    , default=''
              )
@click.option('--save'
    , help="Save the build options to a f'.{platform.system()}.json' file in the module directory."
    , default=''
              )
@click.option('-s', '--soft-link'
    , help="Create a soft link rather than a copy of the binary extension module."
    , default=False, is_flag=True
              )
@click.version_option(version=micc_version())
def main(
        verbosity,
        project_path,
        module,
        build_type,
        cleanup,
        # F2py specific options
        f90exec,
        f90flags, opt, arch,
        debug, noopt, noarch,
        # Cpp specific options
        # cxx_compiler,
        # cxx_flags, cxx_flags_all,
        # Other options
        clean,
        soft_link,
        load, save,
):
    """Build binary extension libraries (f2py and cpp modules)."""
    if save:
        if os.sep in save:
            # TODO replace exception with error message and exit
            raise RuntimeError(f"--save {save}: only filename allowed, not path.")
        if not save.endswith('.json'):
            save += '.json'
    if load:
        if os.sep in load:
            # TODO replace exception with error message and exit
            raise RuntimeError(f"--load {load}: only filename allowed, not path.")
        if not load.endswith('.json'):
            load += '.json'

    options = SimpleNamespace(
        verbosity=verbosity,
        project_path=project_path.resolve(),
        clear_log=False,
    )
    project = Project(options)
    with et_micc.logger.logtime(options):
        build_options = SimpleNamespace(build_type=build_type.upper())
        build_options.cleanup = cleanup
        build_options.clean = clean
        build_options.soft_link = soft_link
        build_options.save = check_load_save(save, "save")
        build_options.load = check_load_save(load, "load")
        if not load:
            # collect build options from command line:
            if build_type == 'DEBUG':
                f2py = {'--debug': None
                    , '--noopt': None
                    , '--noarch': None
                        }
            else:
                f2py = {}
                if f90exec:
                    f2py['--f90exec'] = f90exec
                if f90flags:
                    f2py['--f90flags'] = f90flags
                if opt:
                    f2py['--opt'] = opt
                if arch:
                    f2py['--arch'] = arch
                if noopt:
                    f2py['--noopt'] = None
                if noarch:
                    f2py['--noarch'] = None
                if debug:
                    f2py['--debug'] = None
            build_options.f2py = f2py

            cpp = {}
            cpp['CMAKE_BUILD_TYPE'] = build_type
            # if cxx_compiler:
            #     path_to_cxx_compiler = Path(cxx_compiler).resolve()
            #     if not path_to_cxx_compiler.exists():
            #         raise FileNotFoundError(f"C++ compiler {path_to_cxx_compiler} not found.")
            #     cpp['CMAKE_CXX_COMPILER'] = str(path_to_cxx_compiler)
            # if cxx_flags:
            #     cpp[f"CMAKE_CXX_FLAGS_{build_type}"] = check_cxx_flags(cxx_flags, "--cxx-flags")
            # if cxx_flags_all:
            #     cpp["CMAKE_CXX_FLAGS"] = check_cxx_flags(cxx_flags_all, "--cxx-flags-all")
            build_options.cpp = cpp

        project.options.module_to_build = module
        project.options.build_options = build_options

        build_cmd(project)

    sys.exit(project.exit_code)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
# eodf
