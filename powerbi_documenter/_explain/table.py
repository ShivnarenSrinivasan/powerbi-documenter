from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import AzureChatOpenAI


_SYS_MESSAGE = '''
You are a helpful technical assistant capable of explaining code and queries to non-technical people.

Below is the contents of powerbi tmdl file for a table.
Ignore everything other than the `partition` section
Please explain the query in the source expression in detail--the columns being selected, the table from which,
and the filter logic.
Include the extracted `partition` section in your output, and triple quote it as the query.
'''


def explain(table_definition: str, llm: AzureChatOpenAI) -> str:

    human_prompt = '''
    text: {text}
    '''

    system_prompt = _SYS_MESSAGE

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ]
    )

    messages = chat_template.format_messages(text=table_definition)
    res = llm.invoke(messages)
    return res.content
