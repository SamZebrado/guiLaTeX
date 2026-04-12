#!/usr/bin/env python3
"""直接运行 smoke test 的脚本"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp')))

# 导入并执行
exec(open('temp/test_qt_to_core_minimal.py', encoding='utf-8').read())
