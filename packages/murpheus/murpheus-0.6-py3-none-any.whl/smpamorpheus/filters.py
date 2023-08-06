"""
author: v2thegreat (v2thegreat@gmail.com)

Package to filter out irrelevant rows that might not be wanted for processing

TODO:
    - This package is written with the hopes to better understand what problems processing such a dataset would be
    encountered, and it is hence written with the understanding that this and other scripts will be refactored
    - Add tests
"""

from typing import Union, List, Dict, Any
import pandas as pd
from dask.dataframe import DataFrame as dask_Dataframe


class Filter:
    __instance__ = None

    def __init__(self):
        """
        Create Filter object that can filter out unneeded rows
        """
        if Filter.__instance__ is None:
            Filter.__instance__ = self

        else:
            raise RuntimeError(f"Singleton {self.__class__.__name__} class is created more than once!")

    # def __init__(self, column_name: str = None, like: Any = None):
    #     """
    #     Create Filter object that can filter out unneeded rows
    #     :param column_name: name of the column to match against
    #     :param like: what the object is supposed to look like when converted to a string
    #     """
    #
    #     self._column_name: str = column_name
    #     self._like: Any = like

    # def _set_column_name_and_like(self, column_name: str = None, like: Any = None) -> Tuple[str, Any]:
    #     """
    #     Function to set column_name and like internally.
    #     If they have not been defined in the class, `ValueError` is raised
    #
    #     :param column_name:
    #     :param like:
    #     :return:
    #     """
    #     _column_name = column_name if column_name else self._column_name
    #     _like = like if like else self._like
    #
    #     if not _column_name or not _like:
    #         raise ValueError(f'column_name or like has not been defined in this object or in this function. '
    #                          f'Please define them and try again')
    #     return _column_name, _like

    @staticmethod
    def filter(rows: Union[List[Dict], Dict[str, List], pd.DataFrame, dask_Dataframe], column_name: str = None,
               like: Any = None) -> Union[dask_Dataframe, pd.DataFrame]:
        """
        Function to filter out rows that don't match.

        :param rows: rows that need to be filtered out
        :param column_name: name of the column to match against
        :param like: what the object is supposed to look like when converted to a string
        :return:
        """

        if type(rows) == dict or type(rows) == list:
            _data = pd.DataFrame(rows)
        else:
            _data = rows

        return _data[_data[column_name] == like]


if __name__ == "__main__":
    pass
