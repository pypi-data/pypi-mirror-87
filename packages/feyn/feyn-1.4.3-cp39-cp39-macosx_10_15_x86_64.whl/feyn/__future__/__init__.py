"""
If we knew you'd be over we'd have tidied up a bit.

You've found our __future__ package. This is where we keep all the experimental goodies we're working on. You're free to try it out and give feedback on what you like and don't like.

Everything here is subject to change, so don't rely on any of these interfaces in your production systems. As these experimental features stabilise, they will be ported into the main feyn package.

Usage:
 - You can use this package as any regular python package, like `paint_df_importance_heatmap`
    > from feyn.__future__.contrib.inspection import paint_df_importance_heatmap
    > paint_df_importance_heatmap(...)
"""
from . import contrib

__all__ = ["contrib"]
