import numpy as np


def _is_str(x):
    """
    Check whether the argument is str type or not.

    :param x: The argument to be checked whether str type or not.
    :type x: any type

    :return: Whether argument "x" is string type or not
    :rtype: bool
    """
    return isinstance(x, str)


def _is_str_list(x):
    """
    Check whether the argument is list of str or not.

    :param x: The argument to be checked whether list of str or not.
    :type x: any type

    :return: Whether argument "x" is iterable and all elements have string type, or not
    :rtype: bool
    """
    is_iter = hasattr(x, "__iter__")
    if _is_str(x) or not is_iter:
        return False
    else:
        is_str_elements = all([_is_str(element) for element in x])
        return is_str_elements


def _is_int(x):
    """
    Check whether the argument is int type or not.

    :param x: The argument to be checked whether int type or not.
    :type x: any type

    :return: Whether argument "x" is integer type or not
    :rtype: bool
    """
    return isinstance(x, int) or isinstance(x, np.int64) or isinstance(x, np.int32)


def _is_int_list(x):
    """
    Check whether the argument is list of int or not.

    :param x: The argument to be checked whether list of int or not.
    :type x: any type

    :return: Whether argument "x" is iterable and all elements have integer type, or not
    :rtype: bool
    """
    is_iter = hasattr(x, "__iter__")
    if not is_iter:
        return False
    else:
        is_int_elements = all([_is_int(element) for element in x])
        return is_int_elements


def _check_contents_id_in_index(contents_id, index, file):
    """
    Check whether the argument "contents_id" is in "index" or not.

    :param contents_id: The argument to be checked whether it is included in the argument "index"
    :type contents_id: str or list of str

    :param index: Index.
    :type index: pandas.RangeIndex or any iterable

    :param file: The file which records course information.
    :type file: str

    :return: None. If argument "contents_id" is not included in "index", an exception is raised.
    """
    if _is_str(contents_id):
        assert contents_id in index, "contents id {id} does not exist in {file}".format(id=contents_id, file=file)

    elif _is_str_list(contents_id):
        for c_id in contents_id:
            assert c_id in index, "contents id {id} does not exist in {file}".format(id=c_id, file=file)


def _check_lecture_week_in_index(lecture_week, index, file):
    """
    Check whether the argument "lecture_week" is in "index" or not.

    :param lecture_week: The argument to be checked whether it is included in the argument "index"
    :type lecture_week: int or list of int

    :param index: Index.
    :type index: pandas.RangeIndex or any iterable

    :param file: The file which records course information.
    :type file: str

    :return: None. If argument "lecture_week" is not included in "index", an exception is raised.
    """
    if _is_int(lecture_week):
        assert lecture_week in index, "lecture week {id} does not exist in {file}".format(id=lecture_week, file=file)

    elif _is_int_list(lecture_week):
        for l_week in lecture_week:
            assert l_week in index, "lecture week {id} does not exist in {file}".format(id=l_week, file=file)


def _check_user_id_in_index(user_id, index, file):
    """
    Check whether the argument "user_id" is in "index" or not.

    :param user_id: The argument to be checked whether it is included in the argument "index"
    :type user_id: str or list of str

    :param index: Index.
    :type index: pandas.RangeIndex or any iterable

    :param file: The file which records course information.
    :type file: str

    :return: None. If argument "user_id" is not included in "index", an exception is raised.
    """
    if _is_str(user_id):
        assert user_id in index, "user id {id} does not exist in {file}".format(id=user_id, file=file)

    elif _is_str_list(user_id):
        for u_id in user_id:
            assert u_id in index, "user id {id} does not exist in {file}".format(id=u_id, file=file)
