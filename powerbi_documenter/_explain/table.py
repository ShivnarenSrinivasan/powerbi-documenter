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

Please explain the query in the source expression in detail in the following format:

## Generated Documentation
### Base Table
<name of table being selected, without schema>

### Fields Selected
<column names of passthrough columns that are simple selects>

### Filters Applied
<filters applied>

### Calculated Columns
<computed columns that are created in the query>

<Don't mention anything about data type conversion.>

## Source Code
<include the `partition` section here>
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
    content = res.content
    return content
