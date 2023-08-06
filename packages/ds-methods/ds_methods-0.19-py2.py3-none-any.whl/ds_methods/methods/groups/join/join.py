from pandas import DataFrame

from ds_methods.common.decorators import catch_method_error
from ds_methods.common.validators import check_keys
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema, JoinHows


class Join(BaseMethod):
    options_schema = options_schema

    @catch_method_error()
    def make(self, lhs: DataFrame, rhs: DataFrame) -> MethodOutput:
        if lhs.empty or rhs.empty:
            return MethodOutput(error='empty input')
        if not self.validate_input_(lhs, rhs):
            return MethodOutput(error='wrong input format')

        return self.make_(lhs, rhs)

    def make_(self, lhs: DataFrame, rhs: DataFrame) -> MethodOutput:
        data = lhs.copy() \
            .merge(
                rhs.copy(),
                on=self.options['on'],
                left_on=self.options['left_on'],
                right_on=self.options['right_on'],
                how=self.options['how'],
                suffixes=('', '_merged')
            ) \
            .dropna(axis='columns', how='all') \
            .dropna(axis='index', how='all')
        if self.options['is_drop_merged']:
            data.drop(data.filter(regex='_merged$').columns.tolist(), axis=1, inplace=True)

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, lhs: DataFrame, rhs: DataFrame) -> bool:
        if self.options['on']:
            return check_keys(lhs, self.options['on']) and check_keys(rhs, self.options['on'])

        if self.options['left_on'] and self.options['right_on']:
            return check_keys(lhs, self.options['left_on']) and check_keys(rhs, self.options['right_on'])

        return False
