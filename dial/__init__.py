# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""A Deep Learning GUI-based Framework"""

__author__ = "David Afonso"
__license__ = "GPL"
__maintainer__ = __author__
__url__ = "https://github.com/davafons/dial"
__version__ = "0.0.7"
__version_info__ = tuple((int(n) for n in __version__.split(".")))
__description__ = "A Deep Learning GUI-based Framework"

__requirements__ = [
    ("tensorflow", ">=2.0.0a0"),
    ("PySide2", ">=5.13.1"),
    ("Pillow", ">=6.2.1"),
    ("qimage2ndarray", "==1.8"),
]
