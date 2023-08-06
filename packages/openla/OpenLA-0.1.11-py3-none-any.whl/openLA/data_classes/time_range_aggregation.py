from ..check import _is_str, _is_str_list

class TimeRangeAggregation(object):
    def __init__(self, df):
        self._df = df

    @property
    def df(self):
        return self._df

    def num_users(self):
        """
        Get the number of users in the Dataframe

        :return: The number of users in the Dataframe
        :rtype: int
        """
        return self.df['userid'].nunique()

    def user_id(self):
        """
        Get the unique user ids in the Dataframe

        :return: One-dimensional array of user ids in the event_stream
        :rtype: List[str]
        """
        return list(self.df['userid'].unique())

    def contents_id(self):
        """
        Get the unique contents ids in the Dataframe

        :return: One-dimensional array of contents ids in the Dataframe
        :rtype: List[str]
        """
        return list(self.df['contentsid'].unique())

    def operation_name(self):
        """
        Get the unique operations in the Dataframe

        :return: One-dimensional array of operation names in the Dataframe
        :rtype: List[str]
        """
        for column in self.df.columns:
            if 'elapsed' in column:
                elapsed_time = column

        return self.df.columns.drop([elapsed_time, 'start_of_range', 'end_of_range', 'userid', 'contentsid', 'pageno']).values

    def operation_count(self, operation_name=None, user_id=None, contents_id=None):
        """
        Get the count of each operations in the Dataframe

        :param user_id: The user to count operation. If it is None, the total count of all users is returned.
        :type user_id: str or None

        :param contents_id: The contents to count operation. If it is None, the total count in all contents is returned.
        :type contents_id: str or None

        :param operation_name: The name of operation to count
        :type operation_name: str or None

        :return: If "operation_name" is None, return dictionary of the number of each operation in the Dataframe.
                 (Key: operation name, Value: The count of the operation)

                 else if "operation_name" is indicated, return the count of the operation
        :rtype: dict or int
        """
        df = self.df
        if user_id is not None:
            if _is_str(user_id):
                df = df[df['userid'] == user_id]
            elif _is_str_list(user_id):
                indices = [u_id in user_id for u_id in df['userid']]
                df = df[indices]

        if contents_id is not None:
             if _is_str(contents_id):
                 df = df[df['contentsid'] == contents_id]
             elif _is_str_list(contents_id):
                 indices = [c_id in contents_id for c_id in df['contentsid']]
                 df = df[indices]

        for column in df.columns:
            if 'elapsed' in column:
                elapsed_time = column
        operation_count_dict = dict(df.drop([elapsed_time, 'start_of_range', 'end_of_range', 'userid', 'contentsid', 'page no'], axis=1).sum())

        if operation_name is None:
            return operation_count_dict
        else:
            if not _is_str(operation_name) and hasattr(operation_name, "__iter__"):
                op_dict = {}
                for op_name in operation_name:
                    assert op_name in operation_count_dict, \
                        "The operation {} does not exist".format(op_name)
                    op_dict[op_name] = operation_count_dict[op_name]
                return op_dict

            else:
                assert operation_name in operation_count_dict, \
                    "The operation {} does not exist".format(operation_name)
                return operation_count_dict[operation_name]

