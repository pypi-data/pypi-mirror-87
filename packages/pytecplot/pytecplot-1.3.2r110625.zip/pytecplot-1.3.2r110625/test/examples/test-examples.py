#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import argparse
import datetime
import fnmatch
import multiprocessing
import os
import re
import six
import subprocess
import sys
import textwrap

import multiprocessing.dummy as multithreading

# tecplot is not needed here, but we import now to catch
# an installation problem before we attempt to run
# any of the actual test scripts.
import tecplot

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, here)

from comparison import Comparator


def ostream_filter(pattern, replace='', flags=0):
    '''filter data written to an output stream using regex'''
    if isinstance(pattern, six.string_types):
        pattern = re.compile(pattern, flags=flags)
    def _wrap(ostream):
        _write_orig = ostream.write
        def _write(b):
            _write_orig(re.sub(pattern, replace, b, flags=flags))
        ostream.write = _write
        return ostream
    return _wrap


def checkout_reference(dest, url, branch):
    if not os.path.exists(dest):
        cmd = 'git clone --branch {branch} {url} {dest}'.format(**locals())
    else:
        cmd = 'git -C {dest} checkout {branch}'.format(**locals())
    proc = subprocess.Popen(cmd, shell=True)
    if proc.wait() != 0:
        raise RuntimeError


def filter_paths(dirs, files):
    IGNORE_FILES = ['README.md', 'batch.log']
    dirs[:] = [d for d in dirs if d[0] != '.']
    files = [f for f in files if f[0] != '.' and f not in IGNORE_FILES]
    files = fnmatch.filter(files, '*.py')
    return sorted(dirs), sorted(files)


class ScriptRunner:
    def __init__(self, runner, examples_dir, outdir, ports=None):
        self.pyexec = sys.executable
        self.runner = runner
        self.exdir = examples_dir
        self.outdir = outdir
        self.ports = ports
        self.env = os.environ.copy()

    def run(self, script):
        #print('>>>', script)
        print('.', end='', flush=True)

        wd = os.path.join(self.outdir, os.path.dirname(script))
        try:
            os.makedirs(wd)
        except OSError:
            pass
        script_abspath = os.path.abspath(os.path.join(self.exdir, script))
        if self.ports:
            thread = multithreading.current_process()
            port = self.ports[int(thread.name.split('-')[-1]) - 1]
            opts = '-c -p{port}'.format(**locals())
        else:
            opts = ''
        script_opts = self.script_opts(script)
        cmd = '{self.pyexec} {self.runner} {opts} {script_abspath} -- {script_opts}'.format(**locals())

        #print(cmd)
        proc = subprocess.Popen(cmd, cwd=wd, env=self.env,
                                shell=True, universal_newlines=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                bufsize=10*2**20)
        out = proc.communicate()[0]

        fname = os.path.splitext(os.path.basename(script))[0] + '.out'
        with open(os.path.join(wd, fname), 'wt') as fout:
            pattern = re.compile(r'(Tecplot version: )[\d\.]+')
            replace = r'\1[VERSION]'
            fout.write(re.sub(pattern, replace, out))

        return proc.returncode, script, out

    def run_batch(self, script):
        #print('>>>', script)
        print('.', end='', flush=True)

        wd = os.path.join(self.outdir, os.path.dirname(script))
        try:
            os.makedirs(wd)
        except OSError:
            pass
        script_abspath = os.path.abspath(os.path.join(self.exdir, script))
        script_opts = self.script_opts(script)
        cmd = '{self.pyexec} {script_abspath} {script_opts}'.format(**locals())
        proc = subprocess.Popen(cmd, cwd=wd, env=self.env,
                                shell=True, universal_newlines=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                bufsize=10*2**20)
        out = proc.communicate()[0]

        fname = os.path.splitext(os.path.basename(script))[0] + '.out'
        with open(os.path.join(wd, fname), 'wt') as fout:
            pattern = re.compile(r'(Tecplot version: )[\d\.]+')
            replace = r'\1[VERSION]'
            fout.write(re.sub(pattern, replace, out))

        return proc.returncode, script, out

    def script_opts(self, script):
        _opts = {
            'animation_mpeg4.py': '--nframes=3',
            'default': '',
        }
        return _opts.get(os.path.basename(script), _opts['default'])


def run_scripts(exdir, outdir, runner, maxjobs=None, ports=None):
    run_sequentially = ('26_multiprocess_job_pool.py',
                        '27_multiprocess_job_pool_advanced.py')
    fpaths_sequential = []
    fpaths = []
    for root, dirs, files in os.walk(exdir):
        dirs[:], files = filter_paths(dirs, files)
        subdir = os.path.relpath(root, exdir)
        for f in files:
            if f in run_sequentially:
                fpaths_sequential.append(os.path.join(subdir, f))
            else:
                fpaths.append(os.path.join(subdir, f))

    script_runner = ScriptRunner(runner, exdir, outdir, ports)

    results = list(map(script_runner.run_batch, fpaths_sequential))

    if ports:
        if maxjobs:
            njobs = min(len(ports), maxjobs)
        else:
            njobs = len(ports)
    elif maxjobs:
        njobs = maxjobs
    else:
        njobs = multiprocessing.cpu_count() - 1

    if njobs > 1:
        pool = multithreading.Pool(njobs)
        results.extend(pool.map(script_runner.run, fpaths))
        pool.close()
        pool.join()
    else:
        results = list(map(script_runner.run, fpaths))
    print('')

    batch_log = os.path.join(outdir, 'batch.log')
    if os.path.exists(batch_log):
        os.remove(batch_log)

    if any(r[0] != 0 for r in results):
        fmt = '>>>{1}\n{2}'
        msg = '\n'.join([fmt.format(*r) for r in results if r[0] != 0])
        raise RuntimeError(msg)


def main():
    def integer_list(s):
        ret = []
        for i in s.split(','):
            if '-' in i:
                a, b = i.split('-')
                ret.extend(range(int(a), int(b)+1))
            else:
                ret.append(int(i))
        return ret

    parser = argparse.ArgumentParser()
    parser.add_argument('scripts', metavar='SCRIPTS', nargs='?', default='scripts',
        help='''Directory containing the scripts to be tested.''')
    parser.add_argument('reference', metavar='REFERENCE', nargs='?', default='test_output/reference',
        help='''Directory which will or does contain the reference files.''')
    parser.add_argument('test', metavar='TEST', nargs='?', default='{reference}/../test',
        help='''Directory that will contain the output of the scripts under test.''')
    parser.add_argument('diff', metavar='DIFF', nargs='?', default='{test}/../diff',
        help='''Directory that will contain the diffs going from reference to
        test for those files that are different outside the set tolerance.''')
    parser.add_argument('-p', '--ports', default=None, type=integer_list,
        help='''Port(s) to use when connecting to TecUtil Server. This is a
        comma-separated list. If multiple ports are listed, scripts will be run
        in parallel. (default: %(default)s)''')
    parser.add_argument('-j', '--maxjobs', default=None, type=int,
        help='''Maximum number of scripts to run concurrently. This will default
        to one minus the number of cores on the system, or the number of ports
        given to --ports, whichever is smaller.''')
    parser.add_argument('--no-compare', action='store_true',
        help='''Just run the scripts and do not bother comparing the output.''')

    args = parser.parse_args()
    args.reference = os.path.normpath(args.reference.format(**vars(args)))
    args.test = os.path.normpath(args.test.format(**vars(args)))
    args.diff = os.path.normpath(args.diff.format(**vars(args)))

    here = os.path.dirname(os.path.realpath(__file__))
    runner = os.path.join(here, 'runner.py')

    repo_url = 'git@git.tecplot.com:tecplot/pytecplot-testref.git'
    repo_branch = 'examples'

    ret = 0

    def archive_and_makedir(dirpath):
        if os.path.exists(dirpath):
            timestamp = datetime.datetime.today().replace(microsecond=0).isoformat()
            outdir_old = dirpath + '_{timestamp}'.format(**locals())
            os.rename(dirpath, outdir_old)
        os.makedirs(dirpath)

    try:
        archive_and_makedir(args.test)
        print('running scripts', end='', flush=True)
        run_scripts(args.scripts, args.test, runner, args.maxjobs, args.ports)
    except RuntimeError as e:
        print(e)
        ret = 1

    if not args.no_compare:
        archive_and_makedir(args.diff)
        checkout_reference(args.reference, repo_url, repo_branch)
        try:
            print('comparing output')
            comparator = Comparator(args.test, args.reference, args.diff)
            success, fail = comparator.compare_files()
            if fail:
                ret = 1
        except RuntimeError as e:
            print(e)
            ret = 1

        print('{} files matched'.format(len(success)))
        print('There were {} failures'.format(len(fail)))

        for fpath, diff in fail:
            print(fpath)
            print(diff)

    return ret


if __name__ == '__main__':
    sys.exit(main())
