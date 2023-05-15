import streamlit as st

lakehouse_conn = st.experimental_connection(
  "clickzetta",
  type="sql",
  url="clickzetta://robert:xxxxxx@49d58da9.api.clickzetta.com/robert?schema=private&virtualcluster=default"
)

provs = lakehouse_conn.query("select distinct province from robert.private.geo_cn")
