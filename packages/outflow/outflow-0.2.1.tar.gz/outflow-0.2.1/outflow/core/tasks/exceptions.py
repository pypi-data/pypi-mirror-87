# -*- coding: utf-8 -*-
class TaskException(Exception):
    pass


class ContextArgumentException(TaskException):
    pass


class TaskWithKwargsException(TaskException):
    pass
