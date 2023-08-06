"""
This module receives event stream data and extracts information required.
"""

import warnings
import pandas as pd
from .course_information import CourseInformation
from .data_classes.event_stream import EventStream
from .check import _is_int, _is_int_list, _is_str, _is_str_list


def select_user(data, user_id):
    """
    Extract the log data of the selected user.

    If the argument “user_id” is given as a list, the function extracts all users in the list.

    :param data: The instance of EventStream or converted class
    :type data: EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation

    :param user_id: a user id or list of user ids
    :type user_id: str or list[str]

    :return: Extracted result.
    :rtype: The same type with input.

    """
    assert _is_str(user_id) or _is_str_list(user_id),\
        "please pass string-type or list of str-type for \"user_id\""

    df = data.df
    if _is_str(user_id):
        selected_user_df = df[df['userid'] == user_id]

    elif _is_str_list(user_id):
        indices = [u_id in user_id for u_id in df['userid']]
        selected_user_df = df[indices]

    return_class = type(data)
    return return_class(selected_user_df)


def select_contents(data, contents_id):
    """
    Extract the log data of the selected contents.

    If the argument “contents_id” is given as a list, the function extracts all contents in the list.

    :param data: The instance of EventStream or converted class
    :type data: EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation

    :param contents_id: A contents id or list of contents ids
    :type contents_id: str or list[str]

    :return: Extracted result.
    :rtype: The same type with input.
    """
    assert _is_str(contents_id) or _is_str_list(contents_id), \
        "please pass string-type or list of str-type for \"contents_id\""

    df = data.df
    if _is_str(contents_id):
        selected_contents_df = df[df['contentsid'] == contents_id]

    elif _is_str_list(contents_id):
        indices = [c_id in contents_id for c_id in df['contentsid']]
        selected_contents_df = df[indices]

    return_class = type(data)
    return return_class(selected_contents_df)


def select_operation(event_stream, operation_name):
    """
    Extract the event stream of the selected operation.

    If the argument “operation_name” is given as a list, the function extracts all operation names in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param operation_name: An operation name or list of operation names
    :type operation_name: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    assert _is_str(operation_name) or _is_str_list(operation_name), \
        "please pass string-type or list of str-type for \"operation_name\""

    df = event_stream.df
    if _is_str(operation_name):
        selected_operation_df = df[df['operationname'] == operation_name]

    elif _is_str_list(operation_name):
        indices = [op in operation_name for op in df['operationname']]
        selected_operation_df = df[indices]

    return EventStream(selected_operation_df)


def select_marker_type(event_stream, marker_type):
    """
    Extract the event stream of the selected type of marker operation.

    If the argument “marker_type” is given as a list, the function extracts all marker types in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param marker_type: A marker type or list of marker types
    :type marker_type: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    assert _is_str(marker_type) or _is_str_list(marker_type), \
        "please pass string-type or list of str-type for \"marker_type\""

    df = event_stream.df
    if _is_str(marker_type):
        selected_marker_df = df[df['marker'] == marker_type]

    elif _is_str_list(marker_type):
        indices = [m_type in marker_type for m_type in df['marker']]
        selected_marker_df = df[indices]

    return EventStream(selected_marker_df)


def select_device(event_stream, device_name):
    """
    Extract the event stream recorded by the selected device.

    If the argument “device_name” is given as a list, the function extracts all device names in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param device_name: A device name or list of davice names
    :type device_name: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    assert _is_str(device_name) or _is_str_list(device_name), \
        "please pass string-type or list of str-type for \"target_id\""

    df = event_stream.df
    if _is_str(device_name):
        selected_device_df = df[df['devicecode'] == device_name]

    elif _is_str_list(device_name):
        indices = [device in device_name for device in df['devicecode']]
        selected_device_df = df[indices]

    return EventStream(selected_device_df)


def select_page(event_stream, bottom=None, top=None):
    """
    Extract the event stream recorded in the page between "bottom" number and "top" number.

    If the argument "bottom" is None, extract all pages under the "top".

    If the argument "top" is None, extract all pages above the "bottom".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param bottom: The bottom number of page for extraction
    :type bottom: int or None

    :param top: The top number of page for extraction
    :type top: int or None

    :return: Extracted result.
    :rtype: EventStream
    """
    df = event_stream.df
    if bottom is None and top is None:
        return event_stream
    elif top is None:
        selected_page_df = df[bottom <= df['pageno']]
    elif bottom is None:
        selected_page_df = df[df['pageno'] <= top]
    else:
        selected_page_df = df[(bottom <= df['pageno']) & (df['pageno'] <= top)]
    return EventStream(selected_page_df)


def select_memo_length(event_stream, bottom=None, top=None):
    """
    Extract the event stream of memo (note) operation with the length between bottom number and top number.

    If the argument "bottom" is None, extract all memo length under the "top".

    If the argument "top" is None, extract all memo length above the "bottom".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param bottom: The bottom length of memo for extraction
    :type bottom: int or None

    :param top: The top length of memo for extraction
    :type top: int or None

    :return: Extracted result.
    :rtype: EventStream
    """

    df = event_stream.df
    if bottom is None and top is None:
        return event_stream
    elif top is None:
        selected_memo_df = df[bottom <= df['memo_length']]
    elif bottom is None:
        selected_memo_df = df[df['memo_length'] <= top]
    else:
        selected_memo_df = df[(bottom <= df['memo_length']) & (df['memo_length'] <= top)]
    return EventStream(selected_memo_df)


def select_time(event_stream, start_time=None, end_time=None):
    """
    Extract the event stream recorded between "start_time" and "end_time".

    If the argument "start_time" is None, extract all event stream before "end_time".

    If the argument "end_time" is None, extract all event stream after "start_time".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param start_time: The start time of event stream for extraction
    :type start_time: pandas.Timestamp or datetime.datetime or None

    :param end_time: The end time of event stream for extraction
    :type end_time: pandas.Timestamp or datetime.datetime or None

    :return: Extracted result.
    :rtype: EventStream
    """

    df = event_stream.df
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        df["timestamp"] = pd.to_datetime(df["eventtime"])

    if start_time is None and end_time is None:
        return event_stream
    elif start_time is None:
        selected_time_df = df[df["timestamp"] < end_time]
    elif end_time is None:
        selected_time_df = df[start_time <= df["timestamp"]]
    else:
        selected_time_df = df[(start_time <= df["timestamp"]) & (df["timestamp"] < end_time)]

    del selected_time_df["timestamp"]
    return EventStream(selected_time_df)


def select_by_lecture_time(course_info, event_stream, contents_id=None, timing='during'):
    """
    Extract the event stream recorded after, before, or during lecture.

    :param course_info: CourseInformation instance.
                       (See course_information module to know about class CourseInformation)
    :type course_info: CourseInformation

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param contents_id: contents id or list of contents ids.

                        If the argument “contents_id” is given as a list, the function extracts all contents ids in the list.

                        Else if the argument "contents_id" is None, the function extracts all contents ids in the "event_stream".
    :type contents_id: str or list[str] or None

    :param timing: The timing to extract the event stream. Choose from "after", "before", or "during".
    :type timing: str

    :return: Extracted result.
    :rtype: EventStream
    """
    if contents_id is None:
        contents_id = event_stream.contents_id()

    lecture_week = course_info.contents_id_to_lecture_week(contents_id)
    lecture_start = course_info.lecture_start_time(lecture_week)
    lecture_end = course_info.lecture_end_time(lecture_week)

    assert timing in ['during', 'before', 'after'], \
        "invalid timing was inputted. please pass 'during' or 'before' or 'after' for timing."

    if timing == 'during':
        start_time = lecture_start
        end_time = lecture_end
    elif timing == 'before':
        start_time = None
        end_time = lecture_start
    elif timing == 'after':
        start_time = lecture_end
        end_time = None

    if _is_str(contents_id) or not hasattr(contents_id, "__iter__"):
        selected_contents_stream = select_contents(data=event_stream, contents_id=contents_id)
        return select_time(event_stream=selected_contents_stream, start_time=start_time, end_time=end_time)
    else:
        df = pd.DataFrame()
        for i, id in enumerate(contents_id):
            start = start_time[i] if start_time is not None else None
            end = end_time[i] if end_time is not None else None
            selected_contents_stream = select_contents(data=event_stream, contents_id=id)
            selected_time_stream = select_time(event_stream=selected_contents_stream, start_time=start, end_time=end)
            df = pd.concat([df, selected_time_stream.df], axis=0, sort=False, ignore_index=True)
        return EventStream(df)
