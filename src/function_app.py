import azure.functions as func
import logging
import json
 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
# Constants for the Azure Blob Storage container, file, and blob path
_SNIPPET_NAME_PROPERTY_NAME = "snippetname"
_SNIPPET_PROPERTY_NAME = "snippet"
_BLOB_PATH = "snippets/{mcptoolargs." + _SNIPPET_NAME_PROPERTY_NAME + "}.json"

@app.generic_trigger(arg_name="context", type="mcpToolTrigger", toolName="hello", 
                     description="Hello world.", 
                     toolProperties="[]")
def hello_mcp(context) -> None:
    """
    A simple function that returns a greeting message.

    Args:
        context: The trigger context (not used in this function).

    Returns:
        str: A greeting message.
    """
    return "Hello I am MCPTool!"


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="getsnippet",
    description="Retrieve a snippet by name.",
    toolProperties=f"[{{\"propertyName\":\"{_SNIPPET_NAME_PROPERTY_NAME}\",\"propertyType\":\"string\",\"description\":\"The name of the snippet.\"}}]"
)
@app.generic_input_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path=_BLOB_PATH
)
def get_snippet(file: func.InputStream, context) -> str:
    """
    Retrieves a snippet by name from Azure Blob Storage.
 
    Args:
        file (func.InputStream): The input binding to read the snippet from Azure Blob Storage.
        context: The trigger context containing the input arguments.
 
    Returns:
        str: The content of the snippet or an error message.
    """
    snippet_content = file.read().decode("utf-8")
    logging.info(f"Retrieved snippet: {snippet_content}")
    return snippet_content


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="savesnippet",
    description="Save a snippet with a name.",
    toolProperties=f"[{{\"propertyName\":\"{_SNIPPET_NAME_PROPERTY_NAME}\",\"propertyType\":\"string\",\"description\":\"The name of the snippet.\"}},"
                   f"{{\"propertyName\":\"{_SNIPPET_PROPERTY_NAME}\",\"propertyType\":\"string\",\"description\":\"The content of the snippet.\"}}]"
)
@app.generic_output_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path=_BLOB_PATH
)
def save_snippet(file: func.Out[str], context) -> str:
    content = json.loads(context)
    snippet_name_from_args = content["arguments"][_SNIPPET_NAME_PROPERTY_NAME]
    snippet_content_from_args = content["arguments"][_SNIPPET_PROPERTY_NAME]

    if not snippet_name_from_args:
        return "No snippet name provided"

    if not snippet_content_from_args:
        return "No snippet content provided"
 
    file.set(snippet_content_from_args)
    logging.info(f"Saved snippet: {snippet_content_from_args}")
    return f"Snippet '{snippet_content_from_args}' saved successfully"