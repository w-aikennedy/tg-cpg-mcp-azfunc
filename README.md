# Getting Started with Remote MCP Servers using Azure Functions (Python)

This is a quickstart template to easily build and deploy a custom remote MCP server to the cloud using Azure Functions with Python. You can clone/restore/run on your local machine with debugging, and `azd up` to have it in the cloud in a couple minutes. The MCP server is secured by design using keys and HTTPS, and allows more options for OAuth using EasyAuth and/or API Management as well as network isolation using VNET.

If you're looking for this sample in more languages check out the [.NET/C#](https://github.com/Azure-Samples/remote-mcp-functions-dotnet) and [Node.js/TypeScript](https://github.com/Azure-Samples/remote-mcp-functions-typescript) versions.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=836901178)

Below is the architecture diagram for the Remote MCP Server using Azure Functions:

![Architecture Diagram](architecture-diagram.png)

## Prerequisites

+ [Python](https://www.python.org/downloads/) version 3.11 or higher
+ [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local?pivots=programming-language-python#install-the-azure-functions-core-tools)
+ [Azure Developer CLI](https://aka.ms/azd)
+ To use Visual Studio Code to run and debug locally:
  + [Visual Studio Code](https://code.visualstudio.com/)
  + [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)

## Prepare your local environment

An Azure Storage Emulator is needed for this particular sample because we will save and get snippets from blob storage.

1. Start Azurite

    ```shell
    docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 \
        mcr.microsoft.com/azure-storage/azurite
    ```

>**Note** if you use Azurite coming from VS Code extension you need to run `Azurite: Start` now or you will see errors.

## Run your MCP Server locally from the terminal

1. Change to the src folder in a new terminal window
   ```shell
   cd src
   ```

1. Install required extensions
   ```shell
   func extensions install
   ```
> **Note** if you miss this step the function will not start

1. Install Python dependencies
   ```shell
   pip install -r requirements.txt
   ```

1. Start the Functions host locally:
   ```shell
   func start
   ```

> **Note** by default this will use the webhooks route: `/runtime/webhooks/mcp/sse`.  Later we will use this in Azure to set the key on client/host calls: `/runtime/webhooks/mcp/sse?code=<system_key>`

## Use the MCP server from within a client/host

### VS Code - Copilot Edits

1. **Add MCP Server** from command palette and add URL to your running Function app's SSE endpoint:
    ```shell
    http://0.0.0.0:7071/runtime/webhooks/mcp/sse
    ```
1. **List MCP Servers** from command palette and start the server
1. In Copilot chat agent mode enter a prompt to trigger the tool, e.g., select some code and enter this prompt

    ```plaintext
    Say Hello
    ```

    ```plaintext
    Save this snippet as snippet1 
    ```

    ```plaintext
    Retrieve snippet1 and apply to newFile.py
    ```
1. When prompted to run the tool, consent by clicking **Continue**

1. When you're done, press Ctrl+C in the terminal window to stop the Functions host process.

### MCP Inspector

1. In a **new terminal window**, install and run MCP Inspector

    ```shell
    npx @modelcontextprotocol/inspector
    ```

2. CTRL click to load the MCP Inspector web app from the URL displayed by the app (e.g. http://0.0.0.0:5173/#resources)
3. Set the transport type to `SSE` 
4. Set the URL to your running Function app's SSE endpoint and **Connect**:
    ```shell
    http://0.0.0.0:7071/runtime/webhooks/mcp/sse
    ```
5. **List Tools**.  Click on a tool and **Run Tool**.  

## Deploy to Azure for Remote MCP

Run this [azd](https://aka.ms/azd) command to provision the function app, with any required Azure resources, and deploy your code:

```shell
azd up
```

>**Using key based auth**
> This function requires a system key by default which can be obtained from the [portal](https://learn.microsoft.com/en-us/azure/azure-functions/function-keys-how-to?tabs=azure-portal), and then update the URL in your host/client to be:
> `https://<funcappname>.azurewebsites.net/runtime/webhooks/mcp/sse?code=<systemkey_for_mcp_extension>`
> 
> Via command line you can retrieve the function key with:
> ```shell
> # After azd up has completed at least once
> FUNCTION_APP_NAME=$(cat .azure/$(cat .azure/config.json | jq -r '.defaultEnvironment')/env.json | jq -r '.FUNCTION_APP_NAME')
> RESOURCE_GROUP=$(cat .azure/$(cat .azure/config.json | jq -r '.defaultEnvironment')/env.json | jq -r '.AZURE_RESOURCE_GROUP')
> az functionapp keys list --resource-group $RESOURCE_GROUP --name $FUNCTION_APP_NAME
> ```
> 
> Additionally, [API Management](https://learn.microsoft.com/azure/api-management/api-management-key-concepts) can be used for improved security and policies over your MCP Server, and [EasyAuth](https://learn.microsoft.com/azure/app-service/overview-authentication-authorization) can be used to set up your favorite OAuth provider including Entra.  

You can opt-in to a VNet being used in the sample. To do so, do this before `azd up`:

```bash
azd env set VNET_ENABLED true
```

After publish completes successfully, `azd` provides you with the URL endpoints of your new functions, but without the function key values required to access the endpoints. To obtain these same endpoints along with the **required function keys**, use the command shown above or see [Invoke the function on Azure](https://learn.microsoft.com/azure/azure-functions/create-first-function-azure-developer-cli?pivots=programming-language-python#invoke-the-function-on-azure).

## Redeploy your code

You can run the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app.

>[!NOTE]
>Deployed code files are always overwritten by the latest deployment package.

## Clean up resources

When you're done working with your function app and related resources, you can use this command to delete the function app and its related resources from Azure and avoid incurring any further costs:

```shell
azd down
```

## Helpful Azure Commands

Once your application is deployed, you can use these commands to manage and monitor your application:

```bash
# Get your function app name from the environment file
FUNCTION_APP_NAME=$(cat .azure/$(cat .azure/config.json | jq -r '.defaultEnvironment')/env.json | jq -r '.FUNCTION_APP_NAME')
echo $FUNCTION_APP_NAME

# Get resource group 
RESOURCE_GROUP=$(cat .azure/$(cat .azure/config.json | jq -r '.defaultEnvironment')/env.json | jq -r '.AZURE_RESOURCE_GROUP')
echo $RESOURCE_GROUP

# View function app logs
az webapp log tail --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP

# Redeploy the application without provisioning new resources
azd deploy
```

## Source Code

The function code for the `get_snippet` and `save_snippet` endpoints are defined in the Python files in the `src` directory. The MCP function annotations expose these functions as MCP Server tools.

This shows the code for a few MCP server examples (get string, get object, save object) in Python:

```python
# Import statements
import azure.functions as func
import logging
import json

# Initialize the Azure Functions app with Python v2 model
app = func.FunctionApp()

# Hello function - responds with hello message
@app.mcp_tool('hello', description="Simple hello world MCP Tool that responses with a hello message.")
def hello_tool(req: func.McpRequest) -> str:
    logging.info('Python MCP HTTP trigger hello_tool function processed a request.')
    return "Hello I am MCP Tool!"

# Blob storage binding for snippets
@app.mcp_tool(
    name='get_snippets',
    description="Gets code snippets from your snippet collection.",
    properties=[func.McpProperty(name="snippetname", description="The name of the snippet.")])
@app.blob_input(arg_name="snippet", 
                path="snippets/{snippetname}", 
                connection="AzureWebJobsStorage")
def get_snippet(req: func.McpRequest, snippet: str) -> str:
    logging.info('Python MCP HTTP trigger get_snippet function processed a request.')
    
    # Get snippet name from the tool arguments
    snippet_name = req.params.get('snippetname')
    logging.info(f"Snippet name: {snippet_name}")
    
    if not snippet_name:
        return "No snippet name provided"
    
    if not snippet:
        return f"Snippet '{snippet_name}' not found"
    
    logging.info(f"Retrieved snippet: {snippet_name}")
    return snippet

# Save snippet function
@app.mcp_tool(
    name='save_snippet',
    description="Saves a code snippet into your snippet collection.",
    properties=[
        func.McpProperty(name="snippetname", description="The name of the snippet."),
        func.McpProperty(name="snippet", description="The code snippet."),
    ])
@app.blob_output(arg_name="output_blob", 
                 path="snippets/{snippetname}", 
                 connection="AzureWebJobsStorage")
def save_snippet(req: func.McpRequest) -> str:
    logging.info('Python MCP HTTP trigger save_snippet function processed a request.')
    
    # Get snippet name and content from the tool arguments
    snippet_name = req.params.get('snippetname')
    snippet_content = req.params.get('snippet')
    
    if not snippet_name:
        return "No snippet name provided"
    
    if not snippet_content:
        return "No snippet content provided"
    
    # Return the snippet content to be saved via the blob output binding
    return snippet_content
```

## Next Steps

- Add [API Management](https://learn.microsoft.com/azure/api-management/api-management-key-concepts) to your MCP server
- Add [EasyAuth](https://learn.microsoft.com/azure/app-service/overview-authentication-authorization) to your MCP server
- Enable VNET using VNET_ENABLED=true flag
- Learn more about [related MCP efforts from Microsoft](https://github.com/modelcontextprotocol)
