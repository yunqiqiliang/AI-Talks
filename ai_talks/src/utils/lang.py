from dataclasses import dataclass
from typing import List  # NOQA: UP035

from .constants import AI_ROLE_OPTIONS_EN, AI_ROLE_OPTIONS_RU, AI_TALKS_URL, README_URL


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    ai_role_postfix: str
    title: str
    language: str
    lang_code: str
    donates: str
    donates1: str
    donates2: str
    chat_placeholder: str
    chat_run_btn: str
    chat_clear_btn: str
    chat_save_btn: str
    speak_btn: str
    input_kind: str
    input_kind_1: str
    input_kind_2: str
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str
    footer_title: str
    footer_option0: str
    footer_option1: str
    footer_option2: str
    footer_chat: str
    footer_channel: str
    responsibility_denial: str
    donates_info: str
    tokens_count: str
    message_cost: str
    total_cost: str
    empty_api_handler: str


# --- LOCALE SETTINGS ---
en = Locale( 
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="你是一位女性",
    ai_role_postfix="尽可能简洁地回答。", 
    title="AI Talks To Insights",
    language="英语",
    lang_code="en", 
    donates="捐赠",
    donates1="俄罗斯", 
    donates2="世界",
    chat_placeholder="开始与AI的对话：", 
    chat_run_btn="询问",
    chat_clear_btn="清除并初始化", 
    chat_save_btn="保存", 
    speak_btn="按住说话", 
    input_kind="输入方式", 
    input_kind_1="文本", 
    input_kind_2="语音 [测试模式]", 
    select_placeholder1="选择模型", 
    select_placeholder2="选择角色", 
    select_placeholder3="创建角色", 
    radio_placeholder="角色互动", 
    radio_text1="选择", 
    radio_text2="创建", 
    stt_placeholder="要听AI的声音，请按播放键", 
    footer_title="支持与反馈", 
    footer_option0="聊天", 
    footer_option1="信息", 
    footer_option2="捐赠", 
    footer_chat="AI Talks 聊天", 
    footer_channel="AI Talks 频道", 
    responsibility_denial=""" 
        AI Talks使用Open AI API与ChatGPT交互，ChatGPT是一个能够生成信息的人工智能。 请注意，神经网络的回答可能不可靠、不准确或不相关。
        我们对使用或依赖所提供信息所造成的任何后果不承担任何责任。  支持我们共同开发和与未来的智能互动吧！ """, 
    tokens_count="令牌数：", 
    message_cost="消息费用：", 
    total_cost="对话总费用： ", 
    donates_info="donates info",
    empty_api_handler=f""" 未找到API密钥。请在.streamlit/secrets.toml中创建你的API密钥。
    """, )


ru = Locale(
    ai_role_options=AI_ROLE_OPTIONS_RU,
    ai_role_prefix="Вы девушка",
    ai_role_postfix="Отвечай максимально лаконично.",
    title="Разговорчики с ИИ",
    language="Russian",
    lang_code="ru",
    donates="Поддержать Проект",
    donates1="Россия",
    donates2="Остальной Мир",
    chat_placeholder="Начните Вашу Беседу с ИИ:",
    chat_run_btn="Спросить",
    chat_clear_btn="Очистить",
    chat_save_btn="Сохранить",
    speak_btn="Нажмите и Говорите",
    input_kind="Вид ввода",
    input_kind_1="Текст",
    input_kind_2="Голос [тестовый режим]",
    select_placeholder1="Выберите Модель",
    select_placeholder2="Выберите Роль",
    select_placeholder3="Создайте Роль",
    radio_placeholder="Взаимодествие с Ролью",
    radio_text1="Выбрать",
    radio_text2="Создать",
    stt_placeholder="Чтобы Услышать ИИ Нажми Кнопку Проигрывателя",
    footer_title="Поддержка и Обратная Связь",
    footer_option0="Чат",
    footer_option1="Инфо",
    footer_option2="Донаты",
    footer_chat="Чат Разговорчики с ИИ",
    footer_channel="Канал Разговорчики с ИИ",
    responsibility_denial="""
        `Разговорчики с ИИ` использует API `Open AI` для взаимодействия с `ChatGPT`, ИИ, генерирующим информацию.
        Пожалуйста, учтите, что ответы нейронной сети могут быть недостоверными, неточными или нерелевантными.
        Мы не несём ответственности за любые последствия,
        связанные с использованием или доверием к информации сгенерированныой нейронной сетью.
        Используйте полученные данные генераций на своё усмотрение.
    """,
    donates_info="""
        `AI Talks` собирает донаты исключительно с целью оплаты API `Open AI`.
        Это позволяет обеспечить доступ к общению с ИИ для всех желающих пользователей.
        Поддержите нас для совместного развития и взаимодействия с интеллектом будущего!
    """,
    tokens_count="Количество токенов: ",
    message_cost="Cтоимость сообщения: ",
    total_cost="Общая стоимость разговора: ",
    empty_api_handler=f"""
        Ключ API не найден. Создайте `.streamlit/secrets.toml` с вашим ключом API.
        Инструкции см. в [README.md]({README_URL}) или используйте оригинальный [AI Talks]({AI_TALKS_URL}).
    """,
)
