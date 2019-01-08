#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['qtt.py', '-w', '--onefile']
    #opts = ['douyin.py', '-F']
    #opts = ['douyin.py', '-F', '-w']
    #opts = ['douyin.py', '-F', '-w', '--icon=TargetOpinionMain.ico','--upx-dir','upx391w']
    run(opts)
