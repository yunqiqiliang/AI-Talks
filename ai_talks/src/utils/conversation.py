from random import randrange

import streamlit as st
from openai.error import InvalidRequestError, OpenAIError
from streamlit_chat import message

from .agi.chat_gpt import create_gpt_completion
from .stt import show_voice_input
from .tts import show_audio_player

from .snowflake_connector import get_queries_data
from .preparedprompts import prompts_schema,prompts_ord,prompts_sql_standard

import logging
import re
import pandas as pd

def consulting_charts(df)-> None:
    st.dataframe(df)
    col_names = ",".join(str(num) for num in df.columns.tolist())
    st.dataframe(df)
    data_types = ",".join(str(num) for num in df.dtypes.to_numpy())
    consulting_charts_prompts = "这是一个dataframe的字段名：" + col_names.str() + "。和字段类型：" + data_types.str() + "。推荐1-6个合适展现这个dataframe的可视化charts"
    try:
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        st.session_state.charts_type = ai_content
        st.text_area(label="推荐的Charts是：", value=st.session_state.charts_type, key="charts_type")
        
        calc_cost(completion.get("usage"))
        st.session_state.messages.append({"role": "system", "content": ai_content})
        if ai_content:
            show_audio_player(ai_content)
            st.divider()
            show_chat(ai_content, st.session_state.user_text)
                  
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)

def show_query_result() -> None:
    if st.session_state.query_result.find("SELECT") != -1 and st.session_state.query_result.find("FROM") != -1  and st.session_state.query_result.find("BRAZILIAN_ECOMMERCE") != -1 :
        st.session_state.query_result=st.session_state.query_result.replace("SQL","")
        qd=get_queries_data('2022-05-13','2023-05-13',st.session_state.query_result)
        st.text_area(label="执行的SQL代码", value=st.session_state.query_result, key="query_result")
        if df.shape[0]>0 :
            consulting_charts(qd.head(10))
#             st.bar_chart(data=qd,x="QUERY_TYPE",y="TOTAL_ELAPSED_TIME")
            st.table(qd.head(10))
            st.line_chart(qd)
            st.bar_chart(data=qd)

def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": prompts_schema})
    st.session_state.messages.append({"role": "assistant", "content": prompts_ord})
    st.session_state.messages.append({"role": "assistant", "content": prompts_sql_standard})
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10**8)  # noqa: S311
    st.session_state.costs = []
    st.session_state.total_tokens = []
    st.session_state.query_result = ""
    


def show_text_input() -> None:
    st.text_area(label=st.session_state.locale.chat_placeholder, value=st.session_state.user_text, key="user_text")


def get_user_input():
    match st.session_state.input_kind:
        case st.session_state.locale.input_kind_1:
            show_text_input()
        case st.session_state.locale.input_kind_2:
            show_voice_input()
        case _:
            show_text_input()


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        total_generated=len(st.session_state.generated)
        for i in range(total_generated):
            display_order=total_generated-i-1
            message(st.session_state.past[display_order], is_user=True, key=str(display_order) + "_user", seed=st.session_state.seed)
            message("", key=str(display_order), seed=st.session_state.seed)
            st.markdown(st.session_state.generated[display_order])
            st.caption(f"""
                {st.session_state.locale.tokens_count}{st.session_state.total_tokens[display_order]} |
                {st.session_state.locale.message_cost}{st.session_state.costs[display_order]:.5f}$
            """, help=f"{st.session_state.locale.total_cost}{sum(st.session_state.costs):.5f}$")


def calc_cost(usage: dict) -> None:
    total_tokens = usage.get("total_tokens")
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    st.session_state.total_tokens.append(total_tokens)
    # pricing logic: https://openai.com/pricing#language-models
    if st.session_state.model == "gpt-3.5-turbo":
        cost = total_tokens * 0.002 / 1000
    else:
        cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
    st.session_state.costs.append(cost)

def init_gpt_conversation() -> None:
    try:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": prompts_schema})
        st.session_state.messages.append({"role": "assistant", "content": prompts_ord})
        st.session_state.messages.append({"role": "assistant", "content": prompts_sql_standard})
        st.session_state.model = "gpt-3.5-turbo"
        st.session_state.locale = "en"
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")

    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
#             show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)

def show_gpt_conversation() -> None:
    try:
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        st.session_state.query_result = ai_content
        
        start = ai_content.find("```") + 3 # find the index of the first ```
        end = ai_content.rfind("```") # find the index of the last ```
        substring = ai_content[start:end].strip() # get the substring between ``` and strip the whitespace

        substring = substring.upper()
        if substring.find("SELECT") != -1 and substring.find("FROM") != -1 and substring.find("BRAZILIAN_ECOMMERCE") != -1 :
            st.session_state.query_result = substring
        substring = substring.replace("SQL", "")

        calc_cost(completion.get("usage"))
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_audio_player(ai_content)
            st.divider()
            show_chat(ai_content, st.session_state.user_text)
                  
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    show_gpt_conversation()
