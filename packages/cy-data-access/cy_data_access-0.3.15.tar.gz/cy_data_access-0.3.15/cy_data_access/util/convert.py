import json
import pytz
import pandas as pd
from cy_components.helpers.formatter import CandleFormatter


def convert_df_to_json_list(df: pd.DataFrame, primary_column_name=None):
    """DF -> JSON"""
    if primary_column_name is not None:
        df.rename({primary_column_name: '_id'}, axis=1, inplace=True)
    json_list = json.loads(df.T.to_json()).values()
    json_list = CandleFormatter.convert_json_timestamp_to_date(json_list, column_name='_id', tz=pytz.utc)
    return json_list
