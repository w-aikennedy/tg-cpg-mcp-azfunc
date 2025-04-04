# Python App with MCP Integration

This guide walks you through setting up and connecting your Python application with the Model Context Protocol (MCP) Inspector.

---

## 📦 Installation & Setup

### 1. Install Azure Functions Extensions

Ensure you're inside your Python working directory and have the Azure Functions Core Tools installed. Then, run:

```bash
func extensions install
```

### 2. Activate Virtual Environment

Make sure your Python virtual environment is activated before proceeding.

```bash
# Example (Linux/macOS)
source venv/bin/activate

# Example (Windows)
.\venv\Scripts\activate
```

### 3. Start the Functions Host

Run the following command to start the Azure Functions host:

```bash
func host start
```

## 🔗 Installation & Setup

### 4. Start MCP Inspector

Open a new terminal and run the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### 5. Configure Connection

Transport Type: SSE (Server-Sent Events)\
URL: <http://0.0.0.0:7071/runtime/webhooks/mcp/sse>

### 6. Connect to Server

Click Connect within the MCP Inspector UI.

## 🧰 Explore Tools

Once generated:

- You can list all generated tools
- Select any tool to begin interacting with your Python function through MCP

## ✅ Verification

To verify the setup is working:

- Confirm the MCP Inspector shows the connection is active
- Tools appear in the inspector panel after connection
- Selecting a tool returns the expected behavior or response