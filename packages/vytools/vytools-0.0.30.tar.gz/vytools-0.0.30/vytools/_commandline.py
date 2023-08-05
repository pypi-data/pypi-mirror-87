#!/usr/bin/env python3
import argparse, sys, os, json, argcomplete
import vytools

import logging
logging.basicConfig(level=logging.INFO)

TLIST = '(definition, object, ui, stage, compose, episode)'
def add_default_arguments(parser, choices):
  parser.add_argument('--name','-n', action='append', 
    help='Name of thing '+TLIST+' to find episodes for', choices=choices)

def add_build_args(parser):
  parser.add_argument('--build_arg','-b',
                      metavar='KEY=VALUE',
                      action = 'append',
                      help="Set a key-value pairs "
                            "(do not put spaces before or after the = sign). "
                            "If a value contains spaces, you should define "
                            "it with double quotes: "
                            'foo="this is a sentence". Note that '
                            "values are always treated as strings.")      
  parser.add_argument('--all', 
                      action='store_true', 
                      help='If present, rebuild all dependent stages.'
                            'Otherwise only rebuild top level and missing stages')

def make_parser():
  parser = argparse.ArgumentParser(prog='vytools', description='tools for working with vy')
  parser.add_argument('--version','-v', action='store_true', 
    help='Print vytools version')
  parser.add_argument('--contexts', type=str, default='',
    help='Comma delimited list of paths to context folders')
  parser.add_argument('--secrets', type=str, required=False, help='Path to secrets files')
  parser.add_argument('--jobs', type=str, required=False, help='Path to jobs folder. All jobs will be written to this folder.')

  subparsers = parser.add_subparsers(help='specify action', dest='action')
  choices = vytools.CONFIG.get('items')
  build_sub_parser = subparsers.add_parser('build',help='Build docker images that are dependent on named items')
  add_default_arguments(build_sub_parser, choices)
  add_build_args(build_sub_parser)

  info_sub_parser = subparsers.add_parser('info',help='Print things '+TLIST)
  add_default_arguments(info_sub_parser, choices)
  info_sub_parser.add_argument('--dependencies','-d', action='store_true', 
    help='List dependencies of items')
  info_sub_parser.add_argument('--expand','-e', action='store_true', 
    help='Expand items')

  server_sub_parser = subparsers.add_parser('server',help='Run ui server')

  # version_sub_parser = subparsers.add_parser('version',help='Get vytools version')

  run_sub_parser = subparsers.add_parser('run',help='Run specified episodes')
  add_default_arguments(run_sub_parser, choices)
  run_sub_parser.add_argument('--build', action='store_true', 
    help='If present, build dependent stages (also note --all flag).')
  run_sub_parser.add_argument('--save', action='store_true', 
    help='Save episodes')
  run_sub_parser.add_argument('--clean', action='store_true', 
    help='Clean episode folders before running')
  add_build_args(run_sub_parser)

  return parser

def parse_key_value(kv,typ):
  args = {}
  success = True
  if kv:
    for arg in kv:
      if '=' not in arg:
        success = False
        logging.error('A {s} ({a}) failed to be in the form KEY=VALUE'.format(s=typ,a=arg))
      else:
        (k,v) = arg.split('=',1)
        args[k] = v
  return (success, args)

def parse_build_args(ba):
  return parse_key_value(ba,'build argument (--build_arg, -b)')

def main():
  parser = make_parser()
  argcomplete.autocomplete(parser)
  args = parser.parse_args()
  if args.version:
    print(vytools.__version__)
    return

  if args.secrets: vytools.CONFIG.set('secrets',args.secrets)
  if args.jobs: vytools.CONFIG.set('jobs',args.jobs)
  if args.contexts: vytools.CONFIG.set('contexts',args.contexts)
  if not vytools.CONFIG.get('contexts'):
    logging.error('The vy context(s) has not been initialized. Please provide a --contexts')
    return
  ignore_success = vytools.scan()

  lst = [n for n in args.name] if 'name' in dir(args) and args.name else []
  ba = None if 'build_arg' not in dir(args) else args.build_arg
  success, build_args = parse_build_args(ba)
  if not success: return
  build_level = 1 if 'all' in dir(args) and args.all else 0

  if args.action == 'build':
    return bool(vytools.build(lst, build_args=build_args, build_level=build_level))
  elif args.action == 'run':
    if args.build:
      br = vytools.build(lst, build_args=build_args, build_level=build_level)
      if br == False: return False
    return bool(vytools.run(lst, build_args=build_args, save=args.save, clean=args.clean))
  elif args.action == 'info':
    vytools.info(lst, list_dependencies=args.dependencies, expand=args.expand)
  elif args.action == 'server':
    vytools.server()
  else:
    return False
