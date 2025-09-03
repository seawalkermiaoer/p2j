"""
fonts.py

提供统一的 Matplotlib 中文/自定义字体初始化工具，避免各页面重复代码。
遵循 Google Python 风格指南：
- 函数命名使用小写加下划线
- 文档字符串使用三引号，描述目的、参数、返回值
- 代码保持简单，异常可预期时尽量捕获并给出清晰信息
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
from matplotlib.font_manager import FontProperties


def setup_custom_font(font_path: str | Path,
                      fallback_families: Optional[list[str]] = None) -> str:
    """Initialize Matplotlib to use a project-bundled custom TTF font if available.

    This registers the TTF file (e.g., font/SimHei.ttf) at runtime and sets it as
    the default sans-serif family. If the file is missing, it falls back to the
    provided font families or to 'sans-serif'. Also ensures unicode minus display.

    Args:
      font_path: Path to the custom TTF font file relative to project root or
          absolute path. Typical value: "font/SimHei.ttf".
      fallback_families: Optional list of font family names to try when the
          custom font is unavailable. Example: ["Source Han Sans SC", "Noto Sans CJK SC", "Microsoft YaHei"].

    Returns:
      The font family name that Matplotlib will use.
    """
    try:
        path = Path(font_path)
        if path.exists():
            # Register and set custom font as default
            matplotlib.font_manager.fontManager.addfont(str(path))
            prop = FontProperties(fname=str(path))
            family = prop.get_name()
            matplotlib.rcParams["font.sans-serif"] = [family]
        else:
            # Fall back to caller-provided families, then to generic sans-serif
            families = fallback_families or [
                "Source Han Sans SC", "Noto Sans CJK SC", "Microsoft YaHei",
                "SimHei", "SimSun", "Arial Unicode MS", "STSong", "sans-serif",
            ]
            # Find the first available family
            chosen = None
            for name in families:
                try:
                    fp = FontProperties(family=name)
                    matplotlib.font_manager.findfont(fp, fallback_to_default=False)
                    chosen = name
                    break
                except Exception:
                    continue
            matplotlib.rcParams["font.sans-serif"] = [chosen or "sans-serif"]
        # Proper display for minus sign
        matplotlib.rcParams["axes.unicode_minus"] = False
        return matplotlib.rcParams["font.sans-serif"][0]
    except Exception:
        # Hard fallback: generic sans-serif, keep UI working even if font init fails
        matplotlib.rcParams["font.sans-serif"] = ["sans-serif"]
        matplotlib.rcParams["axes.unicode_minus"] = False
        return "sans-serif"