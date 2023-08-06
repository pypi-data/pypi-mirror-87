"""
This module receives event stream data and convert it into the number of operations, page-wise summary of students behavior, etc.
"""

import datetime
import warnings
import numpy as np
import pandas as pd
from .course_information import CourseInformation
from .data_extraction import select_time, select_contents, select_user
from .data_classes.event_stream import EventStream
from .data_classes.operation_count import OperationCount
from .data_classes.time_range_aggregation import TimeRangeAggregation
from .data_classes.pagewise_aggregation import PageWiseAggregation, PageTransition

def _attach_marker_type(row):
    """
    Attach marker type (important or difficult) to operation name "ADD MARKER" and "DELETE MARKER"
    :param row: The row of event stream
    :return: new row which is attached marker type
    """
    op = row['operationname']
    marker_type = row['marker']

    if op in ('ADD MARKER', 'DELETE MARKER'):
        return op + ' ' + marker_type
    else:
        return op


def convert_into_operation_count(event_stream, user_id=None, contents_id=None,
                                 operation_name=None, separate_marker_type=False):
    """
    Convert event stream into how many times each learner used each operation in each content

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param user_id: The user id(s) to aggregate.
                    If it is None, column users in the argument 'event_stream' is used.
    :type user_id: str or list[str] or None

    :param contents_id: The contents id to aggregate events.
    :type contents_id: str or List[str] or None

    :param operation_name: The operation(s) to aggregate.
                           If it is None, all operations in event stream are used.
    :type operation_name: str or list[str] or None

    :param separate_marker_type: whether to count 'MARKER' operations by separating the type "difficult" or "important"
    :type separate_marker_type: bool

    :return: Convert result which represents how many times each learner used each operation
             The DataFrame in the class has (index: row number, columns: 'user id', 'contents id', and each operation).

    :rtype: OperationCount
    """
    if user_id is not None:
        event_stream = select_user(event_stream, user_id)
    if contents_id is not None:
        event_stream = select_contents(event_stream, contents_id)
    stream_df = event_stream.df

    if stream_df.empty:
        empty_df = pd.DataFrame(columns=['userid', 'contetnsid'] + operation_name)
        return OperationCount(empty_df)

    if separate_marker_type:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            stream_df['operationname'] = stream_df.loc[:, ['operationname', 'marker']].apply(_attach_marker_type, axis=1)

    if operation_name is None:
        operation_name = event_stream.operation_name()

    operation_count_list = []
    for ids, user_df in stream_df.groupby(["userid", "contentsid"]):
        user = ids[0]
        contents = ids[1]
        operation_count = user_df["operationname"].value_counts()
        operation_count["userid"] = user
        operation_count["contentsid"] = contents
        operation_count_list.append(operation_count)

    operation_count_df = pd.DataFrame(operation_count_list, columns=["userid", "contentsid"] + operation_name)
    operation_count_df = operation_count_df.fillna(0)
    operation_count_df = operation_count_df.reset_index(drop=True)

    return OperationCount(operation_count_df)


def convert_into_page_transition(event_stream, user_id=None, contents_id=None,
                                 invalid_seconds=None, timeout_seconds=None, count_operation=True,
                                 operation_name=None, separate_marker_type=False):
    """
     Convert event stream into how many times each learner used each operation and
     how long each learner stayed in each page with consideration of page transition.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param user_id: The user id(s) to aggregate.
                      If it is None, column users in the argument 'event_stream' is used.
    :type user_id: str or list[str] or None

    :param contents_id: The contents id to aggregate events.
    :type contents_id: str or List[str] or None

    :param invalid_seconds: If reading seconds in a page do not reach "invalid seconds", the event is not aggregated.
    :type invalid_seconds: int or None

    :param timeout_seconds: If reading seconds in a page exceed "timeout_seconds", the event is not aggregated.
                            When this argument is default value 'None', all events are aggregated.
    :type timeout_seconds: int or None

    :param count_operation: Whether to count each operation in each page. If you only need reading time in each page,
                            this argument is recommended to be set False to accelerate the aggregation.
    :type count_operation: bool

    :param operation_name: The operation(s) to aggregate.
                           If it is None, all operations in event stream are used.
    :type operation_name: str or list[str] or None

    :param separate_marker_type: whether to count 'MARKER' operations by separating the type "difficult" or "important"
    :type separate_marker_type: bool

    :return: Convert result which represents how many times each learner used each operation and how long each learner
             stayed in each page with consideration of page transition.
             The DataFrame in the class has (index: row number, columns: ['user id', 'contents id', 'page no', 'reading_seconds', 'time_of_entry', 'time_of_exit,' each operations])

    :rtype: PageTransition
    """
    def make_empty_df():
        columns = ['userid', 'contentsid', 'pageno', 'reading_seconds', 'time_of_entry', 'time_of_exit']
        if count_operation:
            columns += operation_name
        return pd.DataFrame(columns=columns)

    if user_id is not None:
        event_stream = select_user(event_stream, user_id)
    if contents_id is not None:
        event_stream = select_contents(event_stream, contents_id)
    stream_df = event_stream.df

    if stream_df.empty:
        empty_df = make_empty_df()
        return PageTransition(empty_df)

    stream_df = event_stream.df

    if count_operation and separate_marker_type:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            stream_df['operationname'] = stream_df.loc[:, ['operationname', 'marker']].apply(_attach_marker_type, axis=1)

    if operation_name is None:
        operation_name = event_stream.operation_name()
    elif isinstance(operation_name, str):
        operation_name = [operation_name]

    page_info_dict_list = []
    for ids, user_contents_df in stream_df.groupby(['userid', 'contentsid'], sort=False):
        user_id = ids[0]
        contents_id = ids[1]

        # attach marker_type (difficult or important) to operations 'ADD MARKER' and 'DELETE MARKER'
        page_seq = user_contents_df['pageno'].tolist()
        operation_seq = user_contents_df['operationname'].tolist()
        time_seq = pd.to_datetime(user_contents_df['eventtime']).tolist()

        # aggregation operations in event stream
        operation_count_dict =  dict(zip(operation_name, [0]*len(operation_name)))
        time_of_entry_index = 0
        reading_seconds = 0

        for i in range(len(page_seq)):
            if count_operation:
                if operation_seq[i] in operation_count_dict:
                    operation_count_dict[operation_seq[i]] += 1

            # If (end of sequence) or (operation 'CLOSE' is executed) or (page transition will be happened),
            if (i == len(page_seq) - 1) or \
                (operation_seq[i] == 'CLOSE') or \
                (i+1 < len(page_seq)) and (page_seq[i] != page_seq[i + 1]):

                time_of_exit_index = i
                time_of_entry = time_seq[time_of_entry_index]
                time_of_exit = time_seq[time_of_exit_index]

                page_info_dict = {'userid': user_id, 'contentsid': contents_id,
                                  'pageno': page_seq[i], 'reading_seconds': reading_seconds,
                                  'time_of_entry': time_of_entry, 'time_of_exit': time_of_exit}

                # record operation counts in the page
                if count_operation:
                    page_info_dict.update(operation_count_dict)
                # reset operation count dictionary
                operation_count_dict = dict(zip(operation_name, [0]*len(operation_name)))

                # if reading seconds is more than invalid seconds, the page is recorded. else it is passed through
                if (invalid_seconds is None) or (reading_seconds > invalid_seconds):
                    page_info_dict_list.append(page_info_dict)
                else:
                    pass
                reading_seconds = 0

                # if operation is 'CLOSE', next operation 'OPEN' is i+1
                if operation_seq[i] == 'CLOSE':
                    time_of_entry_index = i + 1
                    continue
                else:
                    time_of_entry_index = i

            # if the time difference between two actions is over timeout_seconds, the event is regarded as time out.
            time_between_actions = (time_seq[i + 1] - time_seq[i]).seconds if i + 1 < len(time_seq) else None
            if time_between_actions is None:
                pass
            elif (timeout_seconds is not None) and (time_between_actions > timeout_seconds):
                time_of_entry_index = i + 1
                pass
            else:
                reading_seconds += time_between_actions

    transition_df = pd.DataFrame(page_info_dict_list)
    transition_df = transition_df.fillna(0)

    if transition_df.empty:
        empty_df = make_empty_df()
        return PageTransition(empty_df)
    else:
        return PageTransition(transition_df)



def convert_into_page_wise(event_stream, user_id=None, contents_id=None,
                           invalid_seconds=None, timeout_seconds=None, count_operation=True,
                           operation_name=None, separate_marker_type=False):
    """
    Convert event stream into how many times each learner used each operation and how long each learner stayed in each page.
    The result is equivalent to the page-wise aggregation of “convert_into_page_transition” function.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param user_id: The user id(s) to aggregate.
                      If it is None, column users in the argument 'event_stream' is used.
    :type user_id: str or list[str] or None

    :param contents_id: The contents id to aggregate events.
    :type contents_id: str or List[str] or None

    :param invalid_seconds: If reading seconds in a page do not reach "invalid seconds", the event is not aggregated.
    :type invalid_seconds: int or None

    :param timeout_seconds: If reading seconds in a page exceed "timeout_seconds", the event is not aggregated.
                            When this argument is default value 'None', all events are aggregated.
    :type timeout_seconds: int or None

    :param count_operation: Whether to count each operation in each page. If you only need reading time in each page,
                            this argument is recommended to be set False to accelerate.
    :type count_operation: bool

    :param operation_name: Operation(s) to aggregate.
                           If it is None, all operations in event stream are used.
    :type operation_name: str or list[str] or None

    :param separate_marker_type: whether to count 'MARKER' operations by separating the type "difficult" or "important"
    :type separate_marker_type: bool

    :return: Convert result which represents how many times each learner used each operation and
             how long each learner stayed in each page.
             The DataFrame in the class has
             (index: row number, columns:['user id', 'contents id', 'page no', 'reading_seconds', each operation])

    :rtype: PageWiseAggregation
    """
    # convert into page transition
    page_transition = convert_into_page_transition(event_stream=event_stream, user_id=user_id, contents_id=contents_id,
                                                   invalid_seconds=invalid_seconds, timeout_seconds=timeout_seconds,
                                                   count_operation=count_operation, operation_name=operation_name,
                                                   separate_marker_type=separate_marker_type)

    if page_transition.df.empty:
        columns = list(page_transition.df.columns)
        columns.remove('time_of_entry')
        columns.remove('time_of_exit')
        empty_df = pd.DataFrame(columns=columns)
        return PageWiseAggregation(empty_df)

    # page-wise aggregation
    page_info_dict_list = []
    for ids, page_df in page_transition.df.groupby(['userid', 'contentsid', 'pageno'], sort=False):
        behavior_df = page_df.drop(['userid', 'contentsid', 'pageno', 'time_of_entry', 'time_of_exit'], axis=1)
        behavior_array = np.array(behavior_df)
        page_info_dict = {'userid': ids[0], 'contentsid': ids[1], 'pageno': ids[2]}
        behavior_dict = dict(zip(behavior_df.columns, np.sum(behavior_array, axis=0)))
        page_info_dict.update(behavior_dict)
        page_info_dict_list.append(page_info_dict)

    page_behavior_df = pd.DataFrame(page_info_dict_list)
    page_behavior_df = page_behavior_df.fillna(0)
    page_behavior_df = page_behavior_df.sort_values(['userid', 'contentsid', 'pageno']).reset_index(drop=True)
    return PageWiseAggregation(page_behavior_df)


def convert_into_time_range(course_info, event_stream, interval_seconds, user_id=None, contents_id=None, lecture_week=None,
                            start_time='start_of_lecture', end_time='end_of_lecture', time_range_basis='minutes',
                            count_operation=True, operation_name=None, separate_marker_type=False):
    """
    Convert event stream into what page read longest and how many times each learner used each operation in specific time intervals.

    :param course_info: CourseInformation instance.
    :type course_info: CourseInformation

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param interval_seconds: The interval to aggregate events.
    :type interval_seconds: int

    :param user_id: The user id(s) to aggregate.
                      If it is None, column users in the argument 'event_stream' is used.
    :type user_id: str or list[str] or None

    :param contents_id: The contents id to aggregate events.
    :type contents_id: str or List[str] or None

    :param lecture_week: The lecture week to aggregate events.
    :type lecture_week: int

    :param start_time: The start time to aggregate. The available arguments is following:

                       'start_of_lecture' ... use lecture start time

                       'start_of_stream'  ... use the oldest event time of 'event_stream'

                       (y, m, d, H, M, S) ... use the time (year, month, day, hours, minutes, seconds). Each element is int type value.

                       pandas.Timestamp or datetime.datetiime object.
    :type start_time: str, tuple, pandas.Timestamp, or datetime.datetime

    :param end_time: The start time to aggregate. The available arguments is following:

                       'end_of_lecture' ... use lecture end time

                       'end_of_stream'  ... use the latest event time of 'event_stream'

                       (y, m, d, H, M, S) ... use the time (year, month, day, hours, minutes, seconds). Each element is int type value.

                       pandas.Timestamp or datetime.datetiime object.
    :type end_time: str, tuple, pandas.Timestamp, or datetime.datetime

    :param time_range_basis: 'seconds', 'minutes', or 'hours'.
    :type time_range_basis: str

    :param count_operation: Whether to count each operation in each page. If you only need page transition,
                            this argument is recommended to be set False to accelerate.
    :type count_operation: bool

    :param operation_name: The operation(s) to aggregate.
                           If it is None, all operations in event stream are used.
    :type operation_name: str or list[str] or None

    :param separate_marker_type: whether to count 'MARKER' operations by separating the type "difficult" or "important"
    :type separate_marker_type: bool

    :return: Convert result which represents how many times each learner used each operation and what page each learner read in each time range.
             The DataFrame in the class has
             (index: row number, columns:['elapsed_time', 'start_of_range', 'end_of_range', 'user id', 'contents id', 'page no', each operation])
            　pageno: 0 means the user did not open a contents.

    :rtype: TimeRangeAggregation
    """
    if user_id is not None:
        event_stream = select_user(event_stream, user_id)

    if contents_id is None:
        contents_id = event_stream.contents_id()

    if lecture_week is None:
        lecture_weeks = course_info.lecture_weeks()
    else:
        if hasattr(lecture_week, "__iter__"):
            lecture_weeks = lecture_week
        else:
            lecture_weeks = [lecture_week]

    range_list = []
    lecture_weeks.sort()
    for lecture in lecture_weeks:
        contents_in_lecture = course_info.lecture_week_to_contents_id(lecture)
        if isinstance(contents_in_lecture, str):
            contents_in_lecture = [contents_in_lecture]

        for content in contents_in_lecture:
            lecture_stream = select_contents(event_stream, content)

            page_transition = convert_into_page_transition(lecture_stream, invalid_seconds=0, count_operation=False)
            transition_df = page_transition.df.loc[:, ['userid', 'contentsid', 'pageno', 'time_of_entry', 'time_of_exit']]

            # start time of conversion
            if start_time == 'start_of_lecture':
                start = course_info.lecture_start_time(lecture)
            elif start_time == 'start_of_stream':
                start = min(pd.to_datetime(lecture_stream.df['eventtime']))
            elif (type(start_time) is pd.Timestamp) or (type(start_time) is datetime.datetime):
                start = start_time
            elif isinstance(start_time, tuple) and len(start_time) == 6:
                start = datetime.datetime(year=start_time[0], month=start_time[1], day=start_time[2],
                                          hour=start_time[3], minute=start_time[4], second=start_time[5])
            else:
                raise ValueError("Invalid start time")

            # end time of conversion
            if end_time == 'end_of_lecture':
                end = course_info.lecture_end_time(lecture)
            elif end_time == 'end_of_stream':
                end = max(pd.to_datetime(lecture_stream.df['eventtime']))
            elif (type(end_time) is pd.Timestamp) or (type(end_time) is datetime.datetime):
                end = end_time
            elif isinstance(start_time, tuple) and len(start_time) == 6:
                end = datetime.datetime(year=end_time[0], month=end_time[1], day=end_time[2],
                                        hour=end_time[3], minute=end_time[4], second=end_time[5])
            else:
                raise ValueError("Invalid end time")

            difference = int((end - start).total_seconds())
            if difference % interval_seconds == 0:
                end_of_range = difference
            else:
                end_of_range = difference + (interval_seconds - (difference % interval_seconds))

            seconds = [sec for sec in range(0, end_of_range, interval_seconds)]
            for sec in seconds:
                start_of_range = start + datetime.timedelta(seconds=sec)
                end_of_range = start_of_range + datetime.timedelta(seconds=interval_seconds)
                transition_df_in_range = transition_df[(transition_df['time_of_entry'] < end_of_range) &
                                                       (start_of_range < transition_df['time_of_exit'])]
                if count_operation:
                    stream_in_range = select_time(lecture_stream, start_of_range, end_of_range)

                for user in event_stream.user_id():
                    if time_range_basis == 'seconds':
                        range_info = {'elapsed_seconds': sec+interval_seconds}
                    elif time_range_basis == 'minutes':
                        range_info = {'elapsed_minutes': (sec+interval_seconds)/60.0}
                    elif time_range_basis == 'hours':
                        range_info = {'elapsed_hours': (sec+interval_seconds)/3600.0}
                    else:
                        raise ValueError("Invalid time range basis")

                    def _time_in_pages(time_of_entry_list, time_of_exit_list):
                        time_in_page_list = []
                        for enter, leave in zip(time_of_entry_list, time_of_exit_list):
                            time_of_entry = max(enter, start_of_range)
                            time_of_exit = min(leave, end_of_range)
                            time_in_page_ = time_of_exit - time_of_entry
                            time_in_page_list.append(time_in_page_)
                        return np.array(time_in_page_list)

                    user_df = transition_df_in_range[transition_df_in_range['userid'] == user]
                    if user_df.empty:
                        range_info.update({'start_of_range': start_of_range, 'end_of_range': end_of_range,
                                           'userid': user, 'contentsid': content, 'pageno': 0})
                    else:
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            time_in_pages = _time_in_pages(user_df['time_of_entry'], user_df['time_of_exit'])
                        longest_staying_page = user_df.iloc[np.argmax(time_in_pages)]['pageno']

                        range_info.update({'start_of_range': start_of_range, 'end_of_range': end_of_range,
                                           'userid': user, 'contentsid': content, 'pageno': longest_staying_page})

                    if count_operation:
                        user_stream = select_user(stream_in_range, user)
                        operation_in_range = list(set(user_stream.operation_name()) & set(operation_name))
                        operation_count = user_stream.operation_count(operation_name=operation_in_range,
                                                                      separate_marker_type=separate_marker_type)
                        range_info.update(operation_count)
                    range_list.append(range_info)

    record_df = pd.DataFrame(range_list)
    record_df = record_df.fillna(0)
    record_df = record_df.sort_values(['contentsid', 'userid']).reset_index(drop=True)
    return TimeRangeAggregation(record_df)
