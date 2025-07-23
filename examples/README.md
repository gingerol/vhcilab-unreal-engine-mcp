# Examples

Working examples to demonstrate the Unreal Engine scene building functionality.

## Available Examples

### `create-visible-lights.py`
Creates a stunning display of colored lights that are guaranteed to be visible in Unreal Engine:
- 8 colored lights in a circle (red, green, blue, yellow, magenta, cyan, orange, purple)
- 5 white lights stacked vertically as a tower
- Perfect for testing visibility and connection

```bash
python3 examples/create-visible-lights.py
```

### `create-mega-structure.py`  
Demonstrates large-scale object creation with complex architectural elements:
- Giant pyramid base (2000+ units wide)
- Four massive corner towers
- Central mega spire
- Floating platform ring
- Perimeter walls
- Mega directional lighting

```bash
python3 examples/create-mega-structure.py
```

### `create-visible-cube.py`
Simple test for basic object creation:
- Single StaticMeshActor cube
- Positioned at height for visibility
- Basic connection testing

```bash
python3 examples/create-visible-cube.py
```

## Usage

All examples connect to Unreal Engine via TCP on port 55557 using the UnrealMCP plugin. Make sure:

1. Unreal Engine is running
2. UnrealMCP plugin is loaded and active
3. TCP server is listening on port 55557

## Finding Created Objects

After running any example, search in the World Outliner for:
- `Visible` - for basic objects
- `Mega` - for large structures  
- `ColorLight` or `TowerLight` - for light examples
- The timestamp in the object names

Click on any object and press 'F' to focus the viewport on it.