#!/usr/bin/env python3
"""Append new draws and push: re-export from production (read-only), rebuild, git commit + push.

Prereqs (once the GitHub account is ready):
  - git remote add origin https://github.com/<user>/<repo>.git
  - credentials for push (gh auth login or SSH key)
Run manually or from cron after each draw (Macau nightly ~21:35, HK on draw days).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = 'Administrator@103.96.150.38'
KEY = str(Path.home() / '.ssh' / 'id_ed25519')
PHP = r'D:\BtSoft\php\83\php.exe'
EXPORT_PHP = 'C:/temp/cyq-export-draws.php'
EXPORT_JSON = 'C:/temp/cyq-draws-export.json'
RAW_LOCAL = Path('/tmp/cyq-dataset/draws-raw.json')

EXPORT_SRC = """<?php
$c = require 'D:/wwwroot/cyq369.top/config.php';
$pdo = new PDO('mysql:host='.$c['db_host'].';dbname='.$c['db_name'].';charset=utf8mb4',
    $c['db_user'], $c['db_pass'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$rows = $pdo->query('SELECT * FROM lottery_draws ORDER BY lottery_code ASC, issue_no ASC')
    ->fetchAll(PDO::FETCH_ASSOC);
file_put_contents('C:/temp/cyq-draws-export.json', json_encode($rows, JSON_UNESCAPED_UNICODE));
echo count($rows);
"""


def run(cmd, **kw):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def main():
    RAW_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    tmp_php = Path('/tmp/cyq-export-draws.php')
    tmp_php.write_text(EXPORT_SRC, encoding='utf-8')
    run(['scp', '-i', KEY, '-o', 'ConnectTimeout=15', str(tmp_php), f'{HOST}:{EXPORT_PHP}'])
    run(['ssh', '-i', KEY, '-o', 'ConnectTimeout=15', HOST, f'{PHP} {EXPORT_PHP}'])
    run(['scp', '-i', KEY, '-o', 'ConnectTimeout=15', f'{HOST}:{EXPORT_JSON}', str(RAW_LOCAL)])
    run(['ssh', '-i', KEY, '-o', 'ConnectTimeout=15', HOST,
         f'del {EXPORT_PHP.replace(chr(47), chr(92))} {EXPORT_JSON.replace(chr(47), chr(92))}'])
    run([sys.executable, str(ROOT / 'scripts' / 'build.py'), str(RAW_LOCAL)])
    run(['git', '-C', str(ROOT), 'add', 'data/'])
    diff = subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--quiet'])
    if diff.returncode == 0:
        print('No new draws; nothing to commit.')
        return
    run(['git', '-C', str(ROOT), 'commit', '-m', 'data: append latest draws'])
    run(['git', '-C', str(ROOT), 'push'])


if __name__ == '__main__':
    main()
