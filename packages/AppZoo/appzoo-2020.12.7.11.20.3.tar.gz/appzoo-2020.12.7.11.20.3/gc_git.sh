#!/usr/bin/env bash

#1.找出大文件的前5个
   git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -g | tail -5
#2.找出大文件的文件名
   git rev-list --objects --all | grep 8f10eff91bb6aa2de1f5d096ee2e1687b0eab007
#3.根据HSA值找到对应文件名
   git rev-list --objects --all | grep 1ada5755215275b7b8c8cfad079bf1edc1322ff2
#4.清除该文件的所有历史记录并强制刷新到所有分支(慎重,需要管理员权限,否则报错)
   git stash
   git filter-branch -
   -index-filter 'git rm --cached --ignore-unmatch <your-file-name>'

   rm -rf .git/refs/original/
   git reflog expire --expire=now --all
   git fsck --full --unreachable
   git repack -A -d
   git gc --aggressive --prune=now
   git push --force --all
