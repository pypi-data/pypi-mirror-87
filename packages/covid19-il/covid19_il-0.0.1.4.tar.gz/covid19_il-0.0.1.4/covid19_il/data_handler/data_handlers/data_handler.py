from abc import ABC
from random import randint, seed
import math
from collections import defaultdict
import pandas as pd
import re

from typing import Dict, DefaultDict, Tuple, AnyStr, Generator

from covid19_il.logger.logger import Logger


class DataHandler(ABC):
    """ Covid19_IL Data Handler Abstract Base Class.

    Attributes:
        _logger(Logger.logger): package's logger.
        _main_data(Dict): received data from api.
        _df(DataFrame): converted data's json to pandas data frame.
        _total_number = total amount from api.

    Methods:
        _convert_json_to_data_frame(self): try returning the data frame's data as json, otherwise returns None.
        _get_clean_copy_df_data(self): return a clean copy of class's data frame attribute.
        _string_parser(self, string: str): returns clean & non null string.
        _convert_string_to_int(self, input_string: str): parsing string to int.
        _get_data_by_column(self, column_name: str): Returns a generator of dictionary which include top total amount
            of given column name via data frame.
        _get_data_by_columns(self, columns_names: Tuple[AnyStr], grouped_by_column: str): Returns data as a generator
            by given amount of columns from a data frame.
        _get_statistics_by_columns_names(self, columns_names: Tuple[AnyStr]): Returns a generator which includes
            statistics from data manipulation of given columns via data frame columns.

    """

    def __init__(self, logger: Logger.logger, json_data: Dict) -> None:
        """ Class Initialization """
        self._logger = logger
        self._main_data = json_data
        self._df = self._convert_json_to_data_frame()
        self._total_number = None

    def __repr__(self) -> str:
        """ Class Representation """
        return f"{self.__class__.__name__}({self._logger}, {self._main_data})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}'s state:\nlogger: {self._logger.__class__}" \
               f"\nmain data: {self._main_data.__class__}"\
               f"\ndf data: {self._df.__class__}" \
               f"\ntotal number: {self._total_number}"

    def __bool__(self) -> bool:
        """ Truth Value of the class """
        return self._main_data is not None

    @property
    def logger(self) -> Logger.logger:
        """ Logger.logger: Returns the Logger object """
        return self._logger

    @logger.setter
    def logger(self, new_logger) -> None:
        self._logger = new_logger

    @property
    def main_data(self) -> dict:
        """ dict: Returns the original data as is """
        return self._main_data

    @property
    def df(self) -> pd.DataFrame:
        """ DataFrame: Returns the actual data as pandas data frame """
        return self._df

    @df.setter
    def df(self, input_df) -> None:
        if isinstance(input_df, pd.DataFrame):
            self._df = input_df
        else:
            self._logger.exception(f"the input value: {input_df} isn't pandas data frame")
            raise TypeError(f"the input value: {input_df} isn't pandas data frame")

    @property
    def total_number(self) -> int:
        """ int: Returns the total number up to the http get request's query if key exist in the dictionary.
                 if not: raise KeyError an mark the value with -1.

                 if the input type isn't valid(None or not int typed) then raise TypeError.
        """
        if self._total_number is None:
            try:
                self._total_number = self._main_data["result"]["total"]
            except KeyError:
                self._total_number = -1
                self._logger.exception(f"Json's Key does not Exists")

        return self._total_number

    @total_number.setter
    def total_number(self, new_value_of_total_number: int) -> None:
        if new_value_of_total_number and isinstance(new_value_of_total_number, int):
            self._total_number = new_value_of_total_number
        else:
            self._logger.exception(f"the input value: {new_value_of_total_number} isn't int")
            raise TypeError(f"the input value: {new_value_of_total_number} isn't int")

    def _convert_json_to_data_frame(self) -> pd.DataFrame or None:
        """ Try returning the data frame's data as json, otherwise returns None.

        Args:
            None.

        Returns:
            df_data(DataFrame or none): converted json data to pandas data frame.

        """

        df_data = None
        try:
            df_data = pd.json_normalize(data=self._main_data["result"]["records"])
        except TypeError as te:
            self.logger.exception(te)
        finally:
            return df_data

    def _get_clean_copy_df_data(self) -> pd.DataFrame:
        """ Return a clean copy of class's data frame attribute.

        Note:
            private method which get called other methods at the beginning before computation.

        Args:
            None.

        Returns:
            df(DataFrame): cleaned copy pandas data frame

        """

        df = self._df.copy()
        del df['_id']
        return df

    def _string_parser(self, string: str) -> str:
        """ Returns clean & non null string.

        Note:
            private method which get called other methods when a string need to be parsed.

        Args:
            string(str): given string for parsing.

        Returns:
            string(str): cleaned & ready to use string.

        """

        return string.strip() if (string != "NULL" and string) else "Unknown"

    def _convert_string_to_int(self, input_string: str) -> int:
        """ Parsing string to int.

        Note:
            private method which get called other methods when a string need to be converted to int before computation.

        Args:
            input_string(str): given string for conversion.

        Returns:
            _(int): integer value.

        """
        seed(0)
        return randint(1, 15) if (input_string == "<15" or
                                  input_string == "NULL" or
                                  input_string == "N" or
                                  input_string == math.isnan(float(input_string))) \
            else int(input_string.split('.')[0])

    def _date_validation(self, pattern: str, date: str):
        """ Validate date as input regular expression.

        Note:
            private method which get called other methods when a date need to be validate.

        Args:
            pattern(str): regular expression pattern for testing date input.
            date(str): inpute date string.

        Returns:
            None

        Raises:
            ValueError: wrong input pattern as date.

        """

        re_result = re.search(pattern, date)
        if re_result is None:
            self._logger.exception(f"Wrong Date Format, the format should be like: '2020-10-03'. input was: {date}")
            raise ValueError("Wrong Date Format, the format should be like: '2020-10-03'.")

    def _get_data_by_column(self, group_by_column: str, ascending_order: bool = False) \
            -> Generator[Dict, None, None] or Generator[str, None, None]:
        """ Returns a generator of dictionary which include top total amount of given column name via data frame.

        Note:
            private method which get called other methods when a string need to be converted to int before computation.

        Args:
            group_by_column(str): given column name for pandas series group by.
            ascending_order(bool): result's ordering.

        Returns:
            data_dict(Generator[Dict, None, None] or Generator[str, None, None]): desired data as generator or
                "No Data" as bad result.

        """

        data_dict = None
        try:
            df = self._get_clean_copy_df_data()
            df = df[['date', group_by_column]]
            ser = df.groupby('date')[group_by_column].unique()
            data_dict = {key: value[0] for (key, value) in
                         sorted(ser.items(), key=lambda item: item[0], reverse=ascending_order)}
        except KeyError as ke:
            self._logger.exception(ke, "No DataFrame's key exists according to the api client's query results")
        finally:
            if bool(data_dict):
                yield from data_dict.items()
            else:
                yield "No Data", ""

    def _get_data_by_columns(self, columns_names: Tuple, grouped_by_column: str) -> \
            Generator[DefaultDict[str, DefaultDict[str, DefaultDict[str, int]]], None, None] or \
            Generator[Tuple[str, str], None, None]:
        """ Yields data by given amount of columns from a data frame.

        Note:
            private method which get called other methods for data manipulation by columns.

        Args:
            columns_names(Tuple): given required df's columns names as a tuple.
            grouped_by_column(str): specific column for pandas series group by operation.

        Yields:
            Tuple[str, DefaultDict[str, DefaultDict[str, int]]] or Tuple[str, str]): desired data or "No Data" as
                bad result.

        """

        data_dict = None
        try:
            df = self.df[[*columns_names]]
            ser = df.groupby([*columns_names])[grouped_by_column]
            data = ser.count()
            data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

            for key, value in data.items():
                data_dict[key[0]][key[1]][key[2]] = value

        except KeyError as ke:
            self._logger.exception(ke, "No DataFrame's key exists according to the api client's query results")
        finally:
            if bool(data_dict):
                yield from data_dict.items()
            else:
                yield "No Data", ""

    def _get_statistics_by_columns_names(self, columns_names: Tuple[AnyStr, AnyStr, AnyStr]) \
            -> Generator[Dict[str, Dict[str, int or float]], None, None] or Generator[Tuple[str, str], None, None]:
        """ Yields statistics from data manipulation of given columns via data frame columns.

        Note:
            private method which get called other methods for data manipulation by columns.

        Args:
            columns_names(Tuple): given required df's columns names as a tuple.

        Yields:
            Tuple[str, Dict[str, int or float]] or Tuple[str, str]): desired data or "No Data" as bad result.

        """

        data_dict = None
        try:
            df = self._get_clean_copy_df_data()
            for column_name in columns_names:
                df[column_name] = [self._convert_string_to_int(item) for item in df[column_name]]

            data_dict = {}
            for column_name in columns_names:
                data_dict[column_name] = {"min": df[column_name].min(),
                                          "max": df[column_name].max(),
                                          "mean": df[column_name].mean(),
                                          "sum": df[column_name].sum()
                                          }

        except KeyError as ke:
            self._logger.exception(ke, "No DataFrame's key exists according to the api client's query results")
        finally:
            if bool(data_dict):
                yield from data_dict.items()
            else:
                yield "No Data", ""


