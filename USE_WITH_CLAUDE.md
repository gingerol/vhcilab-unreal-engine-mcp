# Using VHCI Lab Scene Builder with Claude Code

Natural language scene building in Unreal Engine through Claude Code.

## Prerequisites
1. Unreal Engine with your project open
2. The UnrealMCP plugin enabled in your project
3. This MCP server installed

## Setup Instructions

### 1. Configure Claude Desktop (if using Claude Desktop app)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "unreal-engine": {
      "command": "node",
      "args": ["/Volumes/HDD2/uemcp/unreal-engine-mcp/dist/index.js"]
    }
  }
}
```

### 2. For Claude Code (Terminal Users)

The configuration is already set up in `~/.config/claude-code/settings.json`

### 3. Start Claude and Use It!

In a new terminal:
```bash
cd /Volumes/HDD2/uemcp/unreal-engine-mcp
claude
```

Then you can use natural language commands like:
- "Create a cube at position 0,0,100"
- "Add a point light to the scene"
- "Get project information"
- "List all actors"

## Testing Without Claude

To test the connection directly:

```bash
cd /Volumes/HDD2/uemcp/unreal-engine-mcp
node dist/test-connection.js
```

## Troubleshooting

1. **"Connection refused"**: Make sure Unreal Engine is running with your project open
2. **"Unknown command"**: Check that the UnrealMCP plugin is enabled
3. **No response**: The UnrealMCP server runs on port 55557 - make sure it's not blocked

## Available Commands

The MCP server translates natural language to UnrealMCP commands:
- `create_actor` → `spawn_blueprint_actor`
- `project_info` → `get_project_info`
- And many more!