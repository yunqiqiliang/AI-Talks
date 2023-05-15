from pathlib import Path
from random import randrange

import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation, show_query_result,init_gpt_conversation
from src.utils.preparedprompts import prompts_schema,prompts_ord,prompts_sql_standard

from src.utils.footer import show_donates, show_info
from src.utils.helpers import get_files_in_dir, get_random_img
from src.utils.lang import en, ru
from streamlit_option_menu import option_menu

from src.utils.lakehouse_connector import get_queries_data


# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "欢迎来到Click Zetata Data To Insight"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
]
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# selected_lang = option_menu(
#     menu_title=None,
#     options=[LANG_EN, LANG_RU, ],
#     icons=["globe2", "translate"],
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal",
#     styles=HEADER_STYLES
# )

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": prompts_schema})
    st.session_state.messages.append({"role": "assistant", "content": prompts_ord})
    st.session_state.messages.append({"role": "assistant", "content": prompts_sql_standard})
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []
if "query_result" not in st.session_state:
    st.session_state.query_result = ""
if "charts_type" not in st.session_state:
    st.session_state.charts_type = ""   
    


def main() -> None:
    c1, c2, c3= st.columns([2,3, 5])

    with c1:
        c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
        st.session_state.input_kind = c1.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                c1.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case st.session_state.locale.radio_text2:
                c1.text_input(label=st.session_state.locale.select_placeholder3, key="role")
    with c2:
        df = get_lakehouse_queries_data("select 1+2;")
        st.table(df.head(10))
        if st.session_state.user_text:
            show_conversation()
            st.session_state.user_text = ""
    with c1:
        get_user_input()
        show_chat_buttons()
    with c3:
        show_query_result()


def run_agi():
#     match selected_lang:
#         case "En":
#             st.session_state.locale = en
#         case "Ru":
#             st.session_state.locale = ru
#         case _:
#             st.session_state.locale = en
    st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    selected_footer = option_menu(
        menu_title=None,
        options=[
            st.session_state.locale.footer_option1,
            st.session_state.locale.footer_option0,
#             st.session_state.locale.footer_option2,
        ],
        icons=["info-circle", "chat-square-text", "piggy-bank"],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    match selected_footer:
        case st.session_state.locale.footer_option0:
            main()
        case st.session_state.locale.footer_option1:
            c1, c2, c3= st.columns(3)
            with c2:
                st.image(f"{img_dir}/{get_random_img(get_files_in_dir(img_dir))}")
                show_info(tg_svg)
#         case st.session_state.locale.footer_option2:
#             show_donates()
        case _:
            show_info(tg_svg)


if __name__ == "__main__":
    run_agi()
