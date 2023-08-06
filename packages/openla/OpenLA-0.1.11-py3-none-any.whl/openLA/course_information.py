# -*- coding:utf-8 -*-

import os
import pandas as pd
from .data_classes.event_stream import EventStream
from .check import _is_str, _is_str_list, _is_int, _is_int_list,\
                    _check_user_id_in_index, _check_contents_id_in_index, _check_lecture_week_in_index

class _Base(object):
    """
    This class receive file path to course information and read DataFrame from the file.

    Not exposed to user.
    """
    def __init__(self, file_path):

        """
        :param file_path: file path of course information . The candidates are "Course_xxx_EventStream.csv",
                          "Course_xxx_LectureMaterial.csv", "Course_xxx_LectureTime.csv", or "Course_xxx_QuizScore.csv"
                          (xxx is course id).

        :type file_path: str
        """
        self._file = file_path
        self._df = pd.read_csv(file_path)

    @property
    def file(self):
        return self._file

    @property
    def df(self):
        return self._df


class CourseInformation(object):
    def __init__(self, course_id=None, files_dir=None,
                 event_stream_file=None, lecture_material_file=None, lecture_time_file=None, quiz_score_file=None):
        """
        :param course_id: The id of the course to process.
        :type course_id: str or None

        :param files_dir: The directory which has "Course_xxx_EventStream.csv", "Course_xxx_LectureMaterial.csv",
                          "Course_xxx_LectureTime.csv", and "Course_xxx_QuizScore.csv (xxx is course id).
        :type files_dir: str or None

        :param event_stream_file: If you want to specify the file path directly, use this argument.
        :type event_stream_file: str or None

        :param lecture_material_file: If you want to specify the file path directly, use this argument.
        :type lecture_material_file: str or None

        :param lecture_time_file: If you want to specify the file path directly, use this argument.
        :type lecture_time_file: str or None

        :param quiz_score_file: If you want to specify the file path directly, use this argument.
        :type quiz_score_file: str or None
        """
        self.files_dir = files_dir
        self.course_id = course_id

        if files_dir is not None:
            es_path, lm_path, lt_path, qs_path = self._get_file_path()
        if event_stream_file is not None:
            es_path = event_stream_file
        if lecture_material_file is not None:
            lm_path = lecture_material_file
        if lecture_time_file is not None:
            lt_path = lecture_time_file
        if quiz_score_file is not None:
            qs_path = quiz_score_file

        self._eventstream = _Base(es_path)
        self._lecturematerial = _Base(lm_path)
        self._lecturetime = _Base(lt_path)
        if os.path.exists(qs_path):
            self._quizscore = _Base(qs_path)
            self._has_quiz_score = True
        else:
            self._has_quiz_score = False


    def _get_file_path(self):
        """
        Get four file paths to "Course_xxx_EventStream.csv", "Course_xxx_LectureMaterial.csv",
        "Course_xxx_LectureTime.csv", and "Course_xxx_QuizScore.csv (xxx is course id).

        :param course_id: The string unique to course
        :type course_id: str

        :return: four csv file paths: EventStream, LectureMaterial, LectureTime, and QuizScore
        :rtype: str
        """
        event_stream_path = os.path.join(self.files_dir, "Course_{}_EventStream.csv".format(self.course_id))
        lecture_material_path = os.path.join(self.files_dir, "Course_{}_LectureMaterial.csv".format(self.course_id))
        lecture_time_path = os.path.join(self.files_dir, "Course_{}_LectureTime.csv".format(self.course_id))
        quiz_score_path = os.path.join(self.files_dir, "Course_{}_QuizScore.csv".format(self.course_id))

        return event_stream_path, lecture_material_path, lecture_time_path, quiz_score_path


    def load_eventstream(self):
        """
        Load event stream and return the instance of EventStream class.

        :return: The instance of EventStream
        :rtype: EventStream
        """
        df = self._eventstream.df
        return EventStream(df)


    def lecture_material_df(self):
        """
        Load DataFrame about contents id, lecture week using the contents, and the number of pages in the contents.

        :return: DataFrame about lecture material (contents)
        :rtype: pandas.DataFrame
        """
        return self._lecturematerial.df


    def lecture_time_df(self):
        """
        Load DataFrame about lecture week, the lecture start time, and the lecture end time.

        :return: DataFrame about lecture time
        :rtype: pandas.DataFrame
        """
        return self._lecturetime.df


    def quiz_score_df(self):
        """
        Load DataFrame about user id and quiz score.

        :return: DataFrame about quiz score
        :rtype: pandas.DataFrame
        """
        assert self._has_quiz_score, "This course does not have quiz score data."
        return self._quizscore.df


    def contents_id(self):
        """
        Get the contents ids in this course.

        :return: List of contents ids in this course
        :rtype: list[str]
        """
        return self._lecturematerial.df['contentsid'].tolist()

    def lecture_week(self):
        """
        Get the week number lectures conducted in this course

        :return: List of lecture weeks in this course
        :rtype: list[int]
        """
        return self._lecturematerial.df['lecture'].apply(int).tolist()

    def num_users(self):
        """
        Get the number of users in this course.

        :return: Number of users in this course
        :rtype: int
        """
        return self._eventstream.df['userid'].nunique()


    def user_id(self):
        """
        Get unique user ids in this course.

        :return: List of user ids in this course
        :rtype: list[str]
        """
        return self._eventstream.df['userid'].unique().tolist()


    def user_score(self, user_id=None):
        """
        Get user(s) final score in this course.

        :param user_id: user id or list of user ids to get score.
        :type user_id: str or list[str] or None

        :return: The quiz score of the user.

                 If the arguments "user_id" is given as a list, the function returns list of quiz scores.

                 Else if "user_id" is None, the function returns all users score.

        :rtype: float
        """
        assert self._has_quiz_score, "This course does not have quiz score data."
        if user_id is None:
            return self._quizscore.df['score'].tolist()
        else:
            df = self._quizscore.df.set_index('userid')
            _check_user_id_in_index(user_id=user_id, index=df.index, file=self._quizscore.file)

            if _is_str(user_id):
                return float(df.at[user_id, 'score'])

            elif _is_str_list(user_id):
                scores = df.loc[user_id, 'score'].tolist()
                return scores


    def users_in_selected_score(self, users_list=None, bottom=None, top=None):
        """
        Get user id(s) who got the score between selected scores.

        :param users_list: list of user_ids. The return users are selected from users in this list.
                           If this list is None, the return users are selected from all users in this course.
        :type users_list: list[str] or None

        :param bottom: the bottom score for extraction
        :type bottom: int or float or None

        :param top: the top score for extraction
        :type top: int or float or None

        :return: List of user ids who got the score between "bottom" and "top".

                 If the argument "bottom" is None, extract all users whose scores are under "top".

                 If the argument "top" is None, extract all users whose scores are above "bottom".

        :rtype: list[str]
        """
        assert self._has_quiz_score, "This course does not have quiz score data."
        df = self._quizscore.df

        if users_list is None:
            users_list = self.user_ids()
        else:
            _check_user_id_in_index(user_id=users_list, index=df['userid'].values, file=self._quizscore.file)

        if bottom is None and top is None:
            return users_list
        elif top is None:
            users_in_score = df[bottom <= df['score']]['userid']
        elif bottom is None:
            users_in_score = df[df['score'] <= top]['userid']
        else:
            users_in_score = df[(bottom <= df['score']) & (df['score'] <= top)]['userid']

        return list(set(users_list) & set(users_in_score))


    def contents_id_to_lecture_week(self, contents_id):
        """
        Get the week number of the lecture(s) using the content(s) of the argument "contents_id".

        :param contents_id: The contents id or list of contents ids.
        :type contents_id: str or list[str]

        :return: The lecture week corresponding to the "contents_id".

                 If the argument “contents_id” is given as a list, the function returns list of lecture weeks.

        :rtype: int or list[int]
        """
        assert _is_str(contents_id) or _is_str_list(contents_id), "please pass str-type or list[str]-type"

        df = self._lecturematerial.df.set_index('contentsid')
        _check_contents_id_in_index(contents_id=contents_id, index=df.index, file=self._lecturematerial.file)

        if _is_str(contents_id):
            return int(df.at[contents_id, 'lecture'])

        elif _is_str_list(contents_id):
            lecture_weeks = df.loc[contents_id, 'lecture'].tolist()
            return list(map(int, lecture_weeks))


    def lecture_week_to_contents_id(self, lecture_week):
        """
        Get the content(s) id used in the lecture of the argument "lecture_week".

        :param lecture_week: The lecture week or list of lecture weeks
        :type lecture_week: int or list[int]

        :return: The contents id corresponding to the lecture week.

                 If the argument “lecture_week” is given as a list, the function returns list of contents ids.

        :rtype: str or list[str]
        """
        assert _is_int(lecture_week) or _is_int_list(lecture_week), "please pass int-type or list[int]-type"

        df = self._lecturematerial.df
        df['lecture'] = df['lecture'].apply(int)  # column 'lecture' is float (e.g. 1.0), so converting to integer
        df = df.set_index('lecture')
        _check_lecture_week_in_index(lecture_week=lecture_week, index=df.index, file=self._lecturematerial.file)

        if _is_int(lecture_week):
            return df.at[lecture_week, 'contentsid']

        elif _is_int_list(lecture_week):
            contents_ids = df.loc[lecture_week, 'contentsid'].tolist()
            return contents_ids


    def num_pages_of_contents(self, contents_id):
        """
        Get the number of pages of the content(s) with the argument "contents_id".

        :param contents_id: contents id or list of contents ids
        :type contents_id: str or list[str]

        :return: The number of pages of the lecture material.

                 If the argument “contents_id” is given as a list, the function returns list of number of pages.

        :rtype: int or list[int]
        """
        assert _is_str(contents_id) or _is_str_list(contents_id), "please pass string-type or list[str]-type"

        df = self._lecturematerial.df.set_index('contentsid')
        _check_contents_id_in_index(contents_id=contents_id, index=df.index, file=self._lecturematerial.file)

        if _is_str(contents_id):
            return int(df.at[contents_id, 'pages'])

        elif _is_str_list(contents_id):
            num_pages = df.loc[contents_id, 'pages'].tolist()
            return list(map(int, num_pages))


    def lecture_start_time(self, lecture_week):
        """
        Get the start time of the lecture(s) of the argument "lecture_week".

        :param lecture_week: lecture week or list of lecture weeks to get lecture start time.
        :type lecture_week: int or list[int]

        :return: The start time of the lecture in the lecture week.

                 If the argument “lecture_week” is given as a list, the function returns list of start times.

        :rtype: pandas.Timestamp or list of pandas.Timestamp
        """
        assert _is_int(lecture_week) or _is_int_list(lecture_week), "please pass int-type or list[int]-type"

        df = self._lecturetime.df
        df['lecture'] = df['lecture'].apply(int)  # column 'lecture' is float (e.g. 1.0), so converting to integer
        df = df.set_index('lecture')
        _check_lecture_week_in_index(lecture_week=lecture_week, index=df.index, file=self._lecturetime.file)

        df['starttime'] = pd.to_datetime(df['starttime'])

        if _is_int(lecture_week):
            return df.at[lecture_week, 'starttime']

        elif _is_int_list(lecture_week):
            return df.loc[lecture_week, 'starttime'].tolist()


    def lecture_end_time(self, lecture_week):
        """
        Get the end time of the lecture(s) of the argument "lecture_week".

        :param lecture_week: lecture week or list of lecture weeks to get lecture end time.
        :type lecture_week: int or list[int]

        :return: The end time of the lecture in the lecture week.

                 If the argument “lecture_week” is given as a list, the function returns list of end times.

        :rtype: pandas.Timestamp or list of pandas.Timestamp
        """
        assert _is_int(lecture_week) or _is_int_list(lecture_week), "please pass int-type or list[int]-type"

        df = self._lecturetime.df
        df['lecture'] = df['lecture'].apply(int)  # column 'lecture' is float (e.g. 1.0), so converting to integer
        df = df.set_index('lecture')
        _check_lecture_week_in_index(lecture_week=lecture_week, index=df.index, file=self._lecturetime.file)

        df['endtime'] = pd.to_datetime(df['endtime'])

        if _is_int(lecture_week):
            return df.at[lecture_week, 'endtime']

        elif _is_int_list(lecture_week):
            return df.loc[lecture_week, 'endtime'].tolist()
