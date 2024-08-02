import pathlib
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.language_models import chat_models


_SYS_PROMPT = pathlib.Path(__file__).parent.joinpath('_prompts', 'measure1.md')


def explain(definition: str, llm: chat_models.BaseChatModel) -> str:
    human_prompt = '''
    text: {text}
    '''
    system_prompt = _SYS_PROMPT.read_text()

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ]
    )

    messages = chat_template.format_messages(text=definition)
    res = llm.invoke(messages)
    content = res.content
    return content
