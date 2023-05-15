import streamlit as st
import pandas as pd

lakehouse_conn = st.experimental_connection(
  "clickzetta",
  type="sql",
  url="clickzetta://robert:xxxxxx@49d58da9.api.clickzetta.com/robert?schema=private&virtualcluster=default"
)
TIME_TO_LIVE = 60 * 60 * 6  # 6 hours caching
@st.experimental_memo(ttl=TIME_TO_LIVE)
def get_lakehouse_queries_data(sql_query: str) -> (pd.DataFrame, str, str):
    data = pd.DataFrame()
    error_code = ""
    error_reason = ""
    try:
        # 执行 SQL 查询
        data = lakehouse_conn.query(sql_query)
        # 如果查询成功，则对 DataFrame 进行进一步处理
        return data, error_code, error_reason
    except Exception as e:
        # 如果查询失败，则打印错误代码和错误原因，并进行相应处理
#         print(f"Error code: {e.args[0]}")
#         print(f"Error reason: {e.args[1]}")
#         error_code = e.args[0]
#         error_reason = e.args[1]
        return data, error_code, error_reason
