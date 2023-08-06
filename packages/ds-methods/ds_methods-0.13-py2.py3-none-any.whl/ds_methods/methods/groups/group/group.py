from pandas import DataFrame, Grouper

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import GroupMethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class Group(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> GroupMethodOutput:
        groups = []
        if 'keys' in self.options:
            groups += self.options['keys']
        if 'time' in self.options:
            groups.append(Grouper(freq=f"{self.options['time']}H", key='date'))

        return GroupMethodOutput(
            data=input_data.groupby(groups, sort=False),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        if 'keys' in self.options:
            if not check_keys(input_data, self.options['keys']):
                return False

        if 'time' in self.options:
            return check_keys(input_data, 'date') and check_datetime(input_data['date'])

        return True
