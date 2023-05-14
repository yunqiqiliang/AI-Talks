import datetime
from typing import Any, Dict

import pandas as pd
import streamlit as st
from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeConnection

# from utils import sql

TIME_TO_LIVE = 60 * 60 * 6  # 6 hours caching


# Share the connector across all users connected to the app
@st.experimental_singleton()
def get_connector(
    secrets_key: str = "snowflake",
    input_params: Dict[str, Any] = None,
    use_browser=True,
) -> SnowflakeConnection:
    """Get a connector to Snowflake. By default, the connector will look
    for credentials found under st.secrets["snowflake"].

    Args:
        secrets_key (str, optional): Streamlit secrets key for the credentials.
        Defaults to 'snowflake'

        params (dict, optional): Connector parameters.
        Overrides Streamlit secrets. Defaults to None.

        local_development (bool, optional): If True, this will open a
        tab in your browser to collect requirements. Defaults to True.

    Returns:
        SnowflakeConnection: Snowflake connector object.
    """

    # Default params
    params: Dict[str, Any] = {
        **st.secrets[secrets_key],
        "client_session_keep_alive": True,
        "client_store_temporary_credential": True,
    }

    # Override default params with input params
    if input_params:
        for key in input_params.keys():
            params[key] = input_params[key]

    # This will open a tab in your browser and sign you in
    if use_browser:
        params["authenticator"] = "externalbrowser"

    connector = connect(**params)
    return connector


snowflake_connector = get_connector(
    secrets_key="sf_usage_app",
    use_browser=False,
)

cur = snowflake_connector.cursor()
cur.execute(f"use warehouse {st.secrets.sf_usage_app.warehouse};")
cur.execute(f"use role {st.secrets.sf_usage_app.role};")


@st.experimental_memo(ttl=TIME_TO_LIVE)
def sql_to_dataframe(sql_query: str) -> pd.DataFrame, error_code:str, error_reason:str,:
    error_code=""
    error_reason=""
    data = pd.DataFrame()
    try:
        # 执行 SQL 查询
        data = pd.read_sql(
            sql_query,
            snowflake_connector,
        )
        # 如果查询成功，则对 DataFrame 进行进一步处理
        return data, error_code,error_reason 
    except Exception as e:
        # 如果查询失败，则打印错误代码和错误原因，并进行相应处理
        print(f"Error code: {e.args[0]}")
        print(f"Error reason: {e.args[1]}")
        error_code=e.args[0]
        error_reason=e.args[1]
        return data, error_code,error_reason 
    
    


@st.experimental_memo(ttl=TIME_TO_LIVE)
def get_queries_data(
    date_from: datetime.date,
    date_to: datetime.date,
    sql_query: str,
):
    queries_data ,error_code ,error_reason = sql_to_dataframe(
        sql_query.format(
            date_from=date_from,
            date_to=date_to,
        )
    )
#     queries_data["DURATION_SECS"] = round(
#         (queries_data.TOTAL_ELAPSED_TIME) / 1000
#     )
#     queries_data["DURATION_SECS_PP"] = queries_data.DURATION_SECS.apply(
#         gui.pretty_print_seconds
#     )
#     queries_data["QUERY_TEXT_PP"] = queries_data.QUERY_TEXT.apply(
#         gui.pretty_print_sql_query
#     )
    return queries_data,error_code ,error_reason


if __name__ == "__main__":
    pass
