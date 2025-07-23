# Quick Start Guide - VHCI Lab Scene Builder

Get started with natural language scene building in Unreal Engine.

## 1. Test the MCP Server (Right Now!)

From your terminal, run:
```bash
cd /path/to/vhcilab-unreal-engine-mcp
claude --mcp
```

Once Claude starts, try typing:
```
What tools do you have available?
```

## 2. Install Unreal Engine Plugin

### If you DON'T have Unreal Engine:
You need to install it first from Epic Games Launcher

### If you HAVE Unreal Engine:

1. First, create a new project (or use existing):
   - Open Unreal Engine
   - Create New Project → Games → Third Person Template
   - Name it something like "MCPTest"
   - Note where you save it!

2. Copy our plugin:
   ```bash
   # Replace YOUR_PROJECT_PATH with your actual project location
   cp -r UnrealPlugin/VHCILabConnectedSpaces YOUR_PROJECT_PATH/Plugins/
   ```

3. In Unreal Engine:
   - Close your project
   - Right-click your .uproject file → "Generate Xcode Project" (on Mac)
   - Open the project again
   - It will ask to rebuild the plugin - click Yes

## 3. Start Using It!

1. Make sure Unreal Engine is running with your project open
2. In terminal: `claude --mcp`
3. Try commands like:
   - "Create a cube in the scene"
   - "Add a point light"
   - "List all actors"

## Troubleshooting

- **"Can't connect to Unreal"**: Make sure UE is running
- **"Plugin not found"**: Check if plugin is enabled in UE (Edit → Plugins → search "VHCI")
- **"Command failed"**: The plugin might need to be compiled first