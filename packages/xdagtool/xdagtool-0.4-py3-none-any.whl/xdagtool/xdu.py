import click
from dateutil import parser
from pathlib import Path
import shutil


g_verbose: bool = False

def time_slice(time_start, time_end):
    time_start_ts = int(time_start.timestamp())
    time_end_ts = int(time_end.timestamp())

    time_start_slice = time_start_ts >> 6
    time_end_slice = time_end_ts >> 6

    if g_verbose:
        print('time_start_ts={0}, time_start_hex={0:X}, time_start_slice={1:X}, time_end_ts={2}, '
              'time_end_hex={2:X}, time_end_slice={3:X}'.format(
            time_start_ts, time_start_slice, time_end_ts, time_end_slice))

    start_level_4 = time_start_slice & 0xFF
    start_level_3 = (time_start_slice >> 8) & 0xFF
    start_level_2 = (time_start_slice >> 16) & 0xFF
    start_level_1 = (time_start_slice >> 24) & 0xFF

    end_level_4 = time_end_slice & 0xFF
    end_level_3 = (time_end_slice >> 8) & 0xFF
    end_level_2 = (time_end_slice >> 16) & 0xFF
    end_level_1 = (time_end_slice >> 24) & 0xFF

    if g_verbose:
        print('start_level={:x}-{:x}-{:x}-{:x}, end_level={:x}-{:x}-{:x}-{:x}'.format(
            start_level_1, start_level_2, start_level_3, start_level_4,
            end_level_1, end_level_2, end_level_3, end_level_4))
        print('start_level={}-{}-{}-{}, end_level={}-{}-{}-{}'.format(
            start_level_1, start_level_2, start_level_3, start_level_4,
            end_level_1, end_level_2, end_level_3, end_level_4))

    return time_start_slice, time_end_slice


class SlicePath:
    def __init__(self, time_start_slice, time_end_slice, debug=False):
        self.__time_start_slice = time_start_slice
        self.__time_end_slice = time_end_slice
        self.__debug = debug
        self.__paths = []

    def paths(self):
        self.__iter_level1()
        return self.__paths

    def __iter_level1(self):
        for x in range(0, 0xFF + 1):
            xv_min = x << 24
            xv_max = xv_min + 0xFFFFFF
            level_path = '{}'.format(x) if self.__debug else '{:0>2x}'.format(x)

            if xv_max < self.__time_start_slice or xv_min > self.__time_end_slice:
                continue

            if xv_min > self.__time_start_slice and xv_max < self.__time_end_slice:
                self.__paths.append('{}/'.format(level_path))
            else:
                self.__iter_level2(xv_min, level_path)

    def __iter_level2(self, level_start, parent_path):
        for x in range(0, 0xFF + 1):
            xv_min = x << 16
            xv_max = xv_min + 0xFFFF
            level_path = '{}/{}'.format(parent_path, x) if self.__debug else '{}/{:0>2x}'.format(parent_path, x)

            if level_start + xv_max < self.__time_start_slice or level_start + xv_min > self.__time_end_slice:
                continue

            if level_start + xv_min > self.__time_start_slice and level_start + xv_max < self.__time_end_slice:
                self.__paths.append('{}/'.format(level_path))
            else:
                self.__iter_level3(level_start + xv_min, level_path)

    def __iter_level3(self, level_start, parent_path):
        for x in range(0, 0xFF + 1):
            xv_min = x << 8
            xv_max = xv_min + 0xFF
            level_path = '{}/{}'.format(parent_path, x) if self.__debug else '{}/{:0>2x}'.format(parent_path, x)

            if level_start + xv_max < self.__time_start_slice or level_start + xv_min > self.__time_end_slice:
                continue

            if level_start + xv_min > self.__time_start_slice and level_start + xv_max < self.__time_end_slice:
                self.__paths.append('{}/'.format(level_path))
            else:
                self.__iter_level4(level_start + xv_min, level_path)

    def __iter_level4(self, level_start, parent_path):
        for x in range(0, 0xFF + 1):
            level_path = '{}/{}.dat'.format(parent_path, x) if self.__debug else '{}/{:0>2x}.dat'.format(parent_path, x)

            if level_start + x >= self.__time_start_slice and level_start + x <= self.__time_end_slice:
                self.__paths.append('{}'.format(level_path))


def path_copy(src_path: Path, dest_path: Path):
    # mkdir -p
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # copy go
    src_path_name, dest_path_name = str(src_path), str(dest_path)
    if src_path.is_dir():
        if g_verbose:
            print('copy dir from {} to {}'.format(src_path_name, dest_path_name))
        shutil.copytree(src_path_name, dest_path_name)
    else:
        if g_verbose:
            print('copy file from {} to {}'.format(src_path_name, dest_path_name))
        shutil.copy2(src_path_name, dest_path_name)


def paths_copy(srcdir: str, destdir: str, paths):
    srcdir_path = Path(srcdir).resolve()
    destdir_path = Path(destdir).resolve() if Path(destdir).is_absolute() else (Path.cwd() / Path(destdir)).resolve()
    print('copy go, srcdir_p={}, destdir_p={}'.format(srcdir_path, destdir_path))

    for path_v in paths:
        file_path = Path(path_v)
        src_path = srcdir_path / file_path
        dest_path = destdir_path / file_path

        # skip no-exist file/dir
        if not src_path.exists():
            continue

        # copy go
        path_copy(src_path, dest_path)



@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--src-dir', 'srcdir', default='.', show_default=True,
              help='source directory copy from, default to current directory.',
              type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True), )
@click.option('-d', '--dst-dir', 'dstdir', default=None, show_default=True,
              help='dest directory copy to, default to dryrun mode if not supplied.',
              type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True))
@click.option('-r', '--dryrun', is_flag=True,
              help='dryrun mode, show all files and directories prepare to process, but do not really run.',
              default=False, show_default=True)
@click.option('-v', '--verbose', is_flag=True,
              help='verbose mode',
              default=False, show_default=True)
@click.argument('time-start', type=str)
@click.argument('time-end', type=str, required=False, default=None)
def cmd_go(srcdir, dstdir, dryrun, time_start, time_end, verbose):
    """xdag blocks slicing.

    <command> start-time end-time

        show all files and directories prepare to process between start-time and end-time.

        star-time, end-time, iso8601 format.

    <command> time

        find target block filename for specific time slice. (start-time=end-time=time.)

        time iso8601 format.

    <command> -s srcdir -d dstdir start-time end-time

        copy all files and directories between start-time and end-time from srcdir to dstdir.

    notes:

        xdag main-net era time: 2018-01-05T22:45:00

        lack of sums.dat for some directorys.

        iso8601 time format examples (https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse):

            2018-01-05T22:45:00Z, 2018-01-05T22:45:00+08:00, always use utc time or timezone suffix

    """

    # command parameters
    # print(srcdir, dstdir, dryrun, time_start, time_end)
    global g_verbose
    g_verbose = verbose

    if not dstdir:
        dryrun = True
    time_start_dt = parser.isoparse(time_start)
    time_end_dt = parser.isoparse(time_end) if time_end else time_start_dt
    print('time_start={}, time_end={}'.format(time_start_dt, time_end_dt))

    # get slices
    time_start_slice, time_end_slice = time_slice(time_start_dt, time_end_dt)

    # get paths
    paths = SlicePath(time_start_slice, time_end_slice, debug=False).paths()

    # dryrun or really run
    if dryrun:      # only print paths list
        print('Dryrun mode')
        for x in paths:
            print(x)
    else:           # copy
        paths_copy(srcdir, dstdir, paths)

    return 0


if __name__ == '__main__':
    cmd_go()
