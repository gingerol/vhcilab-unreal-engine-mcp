# vhcilab-unreal-engine-mcp

A Model Context Protocol (MCP) server that enables natural language scene building in Unreal Engine.

Create objects, lights, and structures in Unreal Engine using simple text commands through Claude Code. 

**Built by VHCI Lab** for natural language scene building in Unreal Engine.

## 🔧 Key Features

- **Natural Language Scene Building**: Describe what you want to create
- **Object Creation**: Spawn actors, lights, and structures  
- **Guaranteed Visibility**: Light objects always appear in your scene
- **TCP Communication**: Direct connection to UnrealMCP plugin (port 55557)
- **Claude Code Integration**: Works seamlessly with Claude Code MCP
- **Real-time Feedback**: Instant response from Unreal Engine

## 🏗️ Architecture

```
Claude Code <-> MCP Protocol <-> Scene Builder <-> TCP (55557) <-> UnrealMCP Plugin <-> Unreal Engine
```

The system uses:
- **Primary**: TCP connection to UnrealMCP plugin (port 55557) 
- **Fallback**: HTTP Web Remote Control API (port 30010)
- **Optional**: Custom plugin for extended functionality

## 🚀 Quick Start

### Prerequisites
- Unreal Engine 5.1+ with UnrealMCP plugin installed
- Python 3.8+
- Claude Code CLI

### 1. Clone and Setup
```bash
git clone https://github.com/gingerol/vhcilab-unreal-engine-mcp
cd vhcilab-unreal-engine-mcp
npm install
```

### 2. Configure MCP
Add to your MCP configuration:
```json
{
  "mcpServers": {
    "vhci-object-placer": {
      "command": "python3",
      "args": ["/path/to/vhcilab-unreal-engine-mcp/vhci-object-placer.py"],
      "env": {}
    }
  }
}
```

### 3. Test the System
```bash
python3 examples/create-visible-lights.py
```
This creates a beautiful ring of 8 colored lights plus a 5-light tower - always visible!

## 🎯 Usage Examples

### Simple Commands
```
Create some lights in a circle
Place cubes in a row
Add point lights with different colors
Create basic geometric shapes
```

### Testing Visible Objects
```python
# Test with guaranteed visible lights
python3 examples/create-visible-lights.py

# Test with large-scale structures  
python3 examples/create-mega-structure.py

# Test basic shapes
python3 examples/create-visible-cube.py
```

## 🛠️ Available Tools

### Core MCP Tool
- **`create_objects`** - Create basic objects from natural language descriptions
  - Supports lights (guaranteed visible)
  - Basic actors (may need meshes assigned)
  - Simple placement and scaling

## 🔧 Development & Customization

### Extending the Object Placer
The MCP server parses natural language for object placement. To extend:

1. **Modify parsing logic** in `vhci-object-placer.py`
2. **Add new object types** that have visible meshes
3. **Focus on lights** for guaranteed visibility

### Custom Unreal Plugin Development
Located in `UnrealPlugin/VHCILabConnectedSpaces/`:
- Extend `VHCILabWebServer.cpp` for new HTTP endpoints
- Add functionality in `VHCILabSubsystem.h` for new features
- Build with Unreal Engine's build system

### Testing & Debugging
```bash
# Test MCP connection
./test-mcp.sh

# Test TCP connection directly
python3 test-direct-tcp.py

# Test with comprehensive logging
python3 vhci-universal-creator.py --debug
```

## 📍 Object Placement Examples

### Light Display
```
Create 10 colored lights in a circle
```
Creates visible point lights with different colors arranged in a circular pattern.

### Basic Structures  
```
Place 5 cubes in a row
```
Creates StaticMeshActors (note: may need mesh assignment for visibility).

## 🔍 Troubleshooting

### Connection Issues
- **Port 55557 not responding**: Ensure UnrealMCP plugin is loaded
- **Web Remote Control failing**: Check if Web Remote Control is enabled in UE
- **Objects not visible**: Use `examples/create-visible-lights.py` to test with guaranteed visible objects

### Common Fixes
```bash
# Restart Unreal Engine MCP connection
# In UE Console: py exec(open('test-tcp.py').read())

# Clear actor cache
# Search "StaticMeshActor" in World Outliner and delete test objects

# Verify plugin status  
# Check Plugins > VHCI Lab Connected Spaces is enabled
```

### Known Limitations
- **StaticMeshActors**: Created without visible meshes by default
- **Best Results**: Use light objects which are always visible
- **Performance**: Creating many objects at once may impact performance

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- Adding mesh assignment for visible objects
- More object types with guaranteed visibility
- Better natural language parsing
- Performance optimizations
- Additional MCP tools for Unreal Engine control

## 📄 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions  
- **[USE_WITH_CLAUDE.md](USE_WITH_CLAUDE.md)** - Claude-specific setup guide

## 📜 License

MIT License - Feel free to use this in your own projects!