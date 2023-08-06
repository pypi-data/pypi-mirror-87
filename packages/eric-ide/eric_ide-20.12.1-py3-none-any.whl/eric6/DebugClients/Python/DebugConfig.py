# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module defining type strings for the different Python types.
"""

#
# Keep this list in sync with Debugger.Config.ConfigVarTypeFilters
#
ConfigVarTypeStrings = [
    '__', 'NoneType', 'type',
    'bool', 'int', 'long', 'float', 'complex',
    'str', 'unicode', 'tuple', 'list',
    'dict', 'dict-proxy', 'set', 'file', 'xrange',
    'slice', 'buffer', 'class', 'instance',
    'method', 'property', 'generator',
    'function', 'builtin_function_or_method', 'code', 'module',
    'ellipsis', 'traceback', 'frame', 'other', 'frozenset', 'bytes',
]

BatchSize = 200
ConfigQtNames = (
    'PyQt5.', 'PySide2.', 'Shiboken.EnumType'
)
ConfigKnownQtTypes = (
    '.QChar', '.QByteArray', '.QString', '.QStringList', '.QPoint', '.QPointF',
    '.QRect', '.QRectF', '.QSize', '.QSizeF', '.QColor', '.QDate', '.QTime',
    '.QDateTime', '.QDir', '.QFile', '.QFont', '.QUrl', '.QModelIndex',
    '.QRegExp', '.QRegularExpression', '.QAction', '.QKeySequence',
    '.QDomAttr', '.QDomCharacterData', '.QDomComment', '.QDomDocument',
    '.QDomElement', '.QDomText', '.QHostAddress', '.EnumType'
)
