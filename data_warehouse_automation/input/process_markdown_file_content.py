"""
This module takes the content of the markdown file as input and returns a dictionary
where the keys are the names of the documentation blocks (i.e., the strings between 
{% docs %} and {% enddocs %}) and the values are the content of the blocks.

"""

import re

def extract_documentation(markdown_content):
    # Pattern that matches {% docs %} blocks
    pattern = r"\{% docs ([^%]*) %\}(.*?)\{% enddocs %\}"

    # Find all matches and create a dictionary where
    # the key is the name of the docs block and the value is the content
    documentation = {}
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    for match in matches:
        doc_name = match[0].strip()
        doc_content = match[1].strip()
        documentation[doc_name] = doc_content

    return documentation
