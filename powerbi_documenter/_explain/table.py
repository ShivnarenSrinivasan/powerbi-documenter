from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import AzureChatOpenAI


_SYS_MESSAGE = '''
You are a helpful technical assistant capable of explaining code and queries to non-technical people.
In your entire response, use as simple english as you can.

Below is the contents of powerbi tmdl file for a table.
Ignore everything other than the `partition` section

Please explain the query in the source expression in detail in the following format:

## Generated Documentation
### Base Table
<name of table being selected, without schema>

### Fields Selected
<column names of passthrough columns that are simple selects>

### Filters Applied
<filters applied, except filters on `dbt_valid_to`. Convert SQL-like logic to simple English
Example:
    - instead of "accntg_doc_item_gl_nbr IN ('0106040104', '0106040105')", say
    "accntg_doc_item_gl_nbr is either '0106040104' OR '0106040105'
>

### Calculated Columns
<computed columns that are created in the query>
<if the query creates a literal table, display the data in a formatted table>

<Don't mention anything about data type conversion.>
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
