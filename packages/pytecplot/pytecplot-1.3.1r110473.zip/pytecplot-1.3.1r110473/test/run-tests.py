#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import argparse
import contextlib
import logging
import os
import platform
import subprocess
import sys
import tempfile
import textwrap


SUPPORTED_PYTHON_VERSIONS = [(2,7), (3,6), (3,7), (3,8)]


if sys.version_info[:2] < (3, 0):
    FileNotFoundError = OSError


log = logging.getLogger(os.path.basename(__file__)
                        if __name__ == '__main__'
                        else __name__)


def write_coveragerc(fname):
    fmt = textwrap.dedent("""\
        [report]
        # Regexes for lines to exclude from consideration
        exclude_lines =
            pragma: no cover
        {pyver}
        {system}
            if 0:
            if False:
            if __name__ == .__main__.:

        omit =
            tecplot/tecutil/constant.py
            tecplot/tecutil/message_pb2.py
            tecplot/tecutil/sv.py
            tecplot/tecutil/tecutil.py
            tecplot/tecutil/tecutil_rpc.py
            tecplot/tecutil/tecutil_flatbuffers/*
    """)

    opts = {}

    version = sys.version_info[:2]
    opts['pyver'] = ''
    if version in SUPPORTED_PYTHON_VERSIONS:
        def vinfo(op, v):
            s = '        if sys\.version_info {op} \({v}\n'
            return s.format(op=op, v=', '.join(str(x) for x in v))
        for v in sorted(set(x[0] for x in SUPPORTED_PYTHON_VERSIONS)):
            if v < version[0]:
                opts['pyver'] += vinfo('<=?', [v])
            elif v == version[0]:
                opts['pyver'] += vinfo('[<>]', [v])
                for vv in sorted(filter(lambda x: x[0]==v,
                                        SUPPORTED_PYTHON_VERSIONS)):
                    if vv < version:
                        opts['pyver'] += vinfo('<=?', vv)
                    elif vv == version:
                        opts['pyver'] += vinfo('[<>]', vv)
                    else:
                        opts['pyver'] += vinfo('>=?', vv)
            else:
                opts['pyver'] += vinfo('>=?', [v])

    lin = '[Ll]inux'
    win = '[Ww]indows'
    mac = '[Dd]arwin'
    if platform.system() == 'Windows':
        target = win
        others = (lin,mac)
    elif platform.system() == 'Darwin':
        target = mac
        others = (win,lin)
    else: #if platform.system() == 'Linux':
        target = lin
        others = (win,mac)

    opts['system'] = """\
    if platform\.system.*(?!{0})

    def.*{1}.*(?!{0})
    def.*(?!{0}).*{1}
    def.*{2}.*(?!{0})
    def.*(?!{0}).*{2}
""".format(target,*others)

    with open(fname, 'w+t') as fout:
        fout.write(fmt.format(**opts))
        fout.flush()


@contextlib.contextmanager
def temporary_file(*args, **kwargs):
    kwargs['delete'] = False
    with tempfile.NamedTemporaryFile(*args, **kwargs) as ftmp:
        ftmp.close()
        try:
            yield ftmp.name
        finally:
            try:
                os.remove(ftmp.name)
            except (OSError, FileNotFoundError) as e:
                log.info(e)
                log.info('could not clean up temporary file:' + ftmp.name)


if __name__ == '__main__':
    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--no-coverage', action='store_true')
    parser.add_argument('--source', default='tecplot')
    parser.add_argument('module', help='the test module')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    if not args.args:
        args.args = ['--failfast', '--buffer']

    log.debug('test module:', args.module)
    log.debug('arguments:', args.args)

    if args.no_coverage:
        cmds = [
            [sys.executable, '-m', args.module] + args.args,
            [sys.executable, '-O', '-m', args.module] + args.args,
        ]
        for cmd in cmds:
            log.debug('running command: ' + ' '.join(cmd))
            proc = subprocess.Popen(cmd, env=os.environ)
            if proc.wait() != 0:
                sys.exit(proc.returncode)
    else:
        with temporary_file(mode='w+t') as coveragerc:
            write_coveragerc(coveragerc)
            with temporary_file(mode='w+t') as coverage_results:
                cmds = [
                    [sys.executable, '-m', 'coverage', 'erase',
                     '--rcfile=' + coveragerc],
                    [sys.executable, '-m', 'coverage', 'run',
                     '--rcfile=' + coveragerc, '--module', '--branch',
                     '--source=' + args.source, args.module] + args.args,
                    [sys.executable, '-O', '-m', 'coverage', 'run',
                     '--rcfile=' + coveragerc, '--module', '--branch',
                     '--source=' + args.source, args.module] + args.args,
                    [sys.executable, '-O', '-m', 'coverage', 'report',
                     '--rcfile=' + coveragerc, '--show-missing'],
                ]
                env = os.environ.copy()
                env.update(COVERAGE_FILE=coverage_results)
                for cmd in cmds:
                    log.debug('running command: ' + ' '.join(cmd))
                    proc = subprocess.Popen(cmd, env=env)
                    if proc.wait() != 0:
                        sys.exit(proc.returncode)

    sys.exit(0)
