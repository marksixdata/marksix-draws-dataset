#!/usr/bin/env python3
"""Append new draws and push: re-export from production (read-only), rebuild, git commit + push.

Prereqs (once the GitHub account is ready):
  - git remote add origin https://github.com/<user>/<repo>.git
  - credentials for push (gh auth login or SSH key)
Run manually or from cron after each draw (Macau nightly ~21:35, HK on draw days).

切站后（2026-11-26）：生产机是新机 root@79.109.37.29（端口 64835），走
~/workspace/sshnew.sh、~/workspace/scpnew.sh（内含密钥、端口、出口代理）。
"""
import os
import subprocess
import sys
from pathlib import Path

# GitHub push 用固定 GIT_SSH_COMMAND：hatch-git 每次 git 调用会剥离 .git/config 里的
# core.sshCommand，且 exec 容器以 root 运行、ssh 默认找 /root/.ssh/known_hosts，
# 而 github.com 的 host key 在 /home/hatch/.ssh/known_hosts。写死绝对路径，不依赖 config。
os.environ['GIT_SSH_COMMAND'] = (
    "ssh -i /home/hatch/.ssh/github_marksix -o IdentitiesOnly=yes "
    "-o UserKnownHostsFile=/home/hatch/.ssh/known_hosts"
)

ROOT = Path(__file__).resolve().parent.parent
HOST = 'root@79.109.37.29'
SSH = '/home/hatch/workspace/sshnew.sh'
SCP = '/home/hatch/workspace/scpnew.sh'
PHP = '/www/server/php/83/bin/php'
EXPORT_PHP = '/tmp/cyq-export-draws.php'
EXPORT_JSON = '/tmp/cyq-draws-export.json'
RAW_LOCAL = Path('/tmp/cyq-dataset/draws-raw.json')

EXPORT_SRC = """<?php
$c = require '/www/wwwroot/cyq369.top/config.php';
$pdo = new PDO('mysql:host='.$c['db_host'].';dbname='.$c['db_name'].';charset=utf8mb4',
    $c['db_user'], $c['db_pass'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$rows = $pdo->query('SELECT * FROM lottery_draws ORDER BY lottery_code ASC, issue_no ASC')
    ->fetchAll(PDO::FETCH_ASSOC);
file_put_contents('/tmp/cyq-draws-export.json', json_encode($rows, JSON_UNESCAPED_UNICODE));
echo count($rows);
"""


def run(cmd, **kw):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def main():
    RAW_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    tmp_php = Path('/tmp/cyq-export-draws.php')
    tmp_php.write_text(EXPORT_SRC, encoding='utf-8')
    run([SCP, str(tmp_php), f'{HOST}:{EXPORT_PHP}'])
    run([SSH, f'{PHP} {EXPORT_PHP}'])
    run([SCP, f'{HOST}:{EXPORT_JSON}', str(RAW_LOCAL)])
    run([SSH, f'rm {EXPORT_PHP} {EXPORT_JSON}'])
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
