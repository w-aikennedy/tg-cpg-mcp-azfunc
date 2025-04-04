import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Constants for the Azure Blob Storage container and file name
_CONTAINER_NAME = "test"
_FILE_NAME = "test.txt"

@app.generic_trigger(arg_name="context", type="mcpToolTrigger", toolName="hello", 
                     description="Gets code snippets from your snippet collection.", 
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

@app.generic_trigger(arg_name="context", type="mcpToolTrigger", toolName="savesnippets", 
                     description="Save code snippets.", 
                     toolProperties="[{\"propertyName\":\"codeSnippet\",\"propertyType\":\"string\",\"description\":\"The name of the snippet.\"}]")
@app.generic_output_binding(arg_name="file", type="blob", connection="AzureWebJobsStorage", path=f"{_CONTAINER_NAME}/{_FILE_NAME}")
def save_snippets(context, file: func.Out[str]):
    """
    Saves a code snippet to Azure Blob Storage.

    Args:
        context: The trigger context containing the input data as JSON.
        file (func.Out[str]): The output binding to write the snippet to Azure Blob Storage.

    Raises:
        KeyError: If the "codeSnippet" key is missing in the input JSON.
        json.JSONDecodeError: If the context is not valid JSON.
    """
    content = json.loads(context)
    msg = content["arguments"]["codeSnippet"]
    logging.info(msg)
    file.set(msg)  # Write the snippet to the specified blob

@app.generic_trigger(arg_name="context", type="mcpToolTrigger", toolName="getsnippets", 
                     description="Gets code snippets from your snippet collection.", 
                     toolProperties="[]")
@app.generic_input_binding(arg_name="file", type="blob", connection="AzureWebJobsStorage", path=f"{_CONTAINER_NAME}/{_FILE_NAME}")
def get_snippets(file: func.InputStream, context) -> None:
    """
    Retrieves a saved code snippet from Azure Blob Storage.

    Args:
        file (func.InputStream): The input binding to read the snippet from Azure Blob Storage.
        context: The trigger context (not used in this function).

    Returns:
        str: The content of the blob as a UTF-8 decoded string.

    Raises:
        Exception: If the blob does not exist or cannot be read.
    """
    return file.read().decode('utf-8')  # Read and decode the blob content