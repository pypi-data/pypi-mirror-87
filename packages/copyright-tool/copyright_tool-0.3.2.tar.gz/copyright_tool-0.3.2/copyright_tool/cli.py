"""Console script for copyright_tool."""
from typing import Dict, List
import datetime
import os
import sys
import git

from gitignore_parser import parse_gitignore


end_terminators = {
    'slash': '// inserted by copyright_tool',
    'hash': '## inserted by copyright_tool',
    'html': '<!-- inserted by copyright_tool -->'
}

language_support = {
    'c': 'slash',
    'cpp': 'slash',
    'h': 'slash',
    'hpp': 'slash',
    'ts': 'slash',
    'js': 'slash',
    'tsx': 'slash',
    'jsx': 'slash',
    'py': 'hash',
    'sh': 'hash',
    'java': 'slash',
    'tf': 'slash',
    'yaml': 'hash',
    'yml': 'hash',
    'html': 'html',
    'mdx': 'html',
    'css': 'slash',
}

file_support = {
  'Dockerfile': 'hash',
  'Makefile': 'hash'
}

def get_copyright_file(root_path, file_path):
  language = file_path.split('.')[-1]
  base_file = os.path.basename(file_path).split('.')[0]
  tpl_type = language_support.get(language)
  if not tpl_type:
    tpl_type = file_support.get(base_file)
  if not tpl_type:
    return None
  copyright_file = f'{root_path}/.copyright.{tpl_type}.tpl'
  if os.path.exists(copyright_file):
    return copyright_file
  else:
    return None



def get_all_files(path):
  copyright_ignore_path = f'{path}/.copyrightignore'
  matches = None
  if os.path.exists(copyright_ignore_path):
    matches = parse_gitignore(copyright_ignore_path)

  def get_tracked_files(trees):
    paths = []
    for tree in trees:
      for blob in tree.blobs:
        if (not matches or not matches(blob.abspath)) and get_copyright_file(path, blob.abspath):
          paths.append(blob.abspath)
      if tree.trees:
        paths.extend(get_tracked_files(tree.trees))
    return paths
  repo = git.Repo(path)

  return get_tracked_files([repo.tree()])


def main():
  if len(sys.argv) != 2:
    print("Please enter the path to the root of your Git repository")
    sys.exit(1)

  path = sys.argv[1]
  file_name: str

  for file_name in get_all_files(path):
    with open(file_name, 'r') as filed:
      language = file_name.split('.')[-1]
      end_terminator = end_terminators.get(language_support.get(language))
      if not end_terminator:
        end_terminator = end_terminators.get(file_support.get(os.path.basename(file_name).split('.')[0]))

      body_lines: List[str] = filed.readlines()
      if not body_lines:
        continue

      try:
        end_terminator_index = body_lines.index(end_terminator+'\n') + 2
      except:
        end_terminator_index = -1

      start_index = 0
      new_body_lines = []
      if body_lines[0].startswith('#!'):
        start_index = 1
        new_body_lines = [body_lines[0]]

      if end_terminator_index >= 0:
        content_lines = body_lines[end_terminator_index:]
      else:
        content_lines = body_lines[start_index:]

    copyright_file = get_copyright_file(path, file_name)
    if not copyright_file:
        continue

    with open(copyright_file) as filed:
      copyright = filed.read().format(year = datetime.datetime.now().year)

    new_body_lines += [copyright, '\n', end_terminator, '\n', '\n'] + content_lines

    with open(file_name, 'w+') as filed:
      filed.write(''.join(new_body_lines))



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
