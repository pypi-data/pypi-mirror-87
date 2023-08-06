import argparse, io, os, sys

import warnings
warnings.filterwarnings('error', module='tecplot.*')

import tecplot

parser = argparse.ArgumentParser()
parser.add_argument('script', metavar='SCRIPT', help='''Script to run.''')
parser.add_argument('-c', '--connected', action='store_true',
    help='''Connect to TecUtil Server''')
parser.add_argument('-p', '--port', type=int, default=7600,
    help='''Port to use when connecting to TecUtil Server''')
parser.add_argument('args', nargs='*')

args = parser.parse_args()
#print('args:', args)
sys.argv = [args.script] + args.args

if args.connected:
    tecplot.session.connect(port=args.port, quiet=True)
    tecplot.new_layout()

assert tecplot.tecutil._tecutil.WorkAreaGetDimensions() == (800, 600)

interface = tecplot.session.style.Style('Interface')
interface._set_style(96.52, 'IDotsPerInch')
interface._set_style(96.52, 'JDotsPerInch')

tecplot.macro.execute_command('''
$!Interface OpenGLConfig { ImageRenderingStrategy = Mesa }
$!Interface Data { UseStableSortForConnectivity = Yes }
$!Internal "SuppressDynamicVersionInImage = Yes"
''')

#print('script:', args.script)
with open(args.script, 'rt') as fin:
    src = fin.read()

exec(src)

tecplot.session.stop()

import time
time.sleep(0.1)
