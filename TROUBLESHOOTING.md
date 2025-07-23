# Troubleshooting - VHCI Lab Scene Builder

Common issues and solutions for Unreal Engine MCP connection.

## Check if UnrealMCP is Running in UE

1. **In Unreal Engine**, press **`** (backtick) to open the console
2. Type this command to enable verbose logging:
   ```
   log LogTemp Verbose
   ```
3. Run our test script again and watch for messages like:
   - "UnrealMCPBridge: Server started"
   - "MCPServerRunnable: Processing message"
   - "MCPServerRunnable: Client connection pending"

## Manual Test in UE Console

Try these console commands in UE to verify the plugin is loaded:
```
UnrealMCP.Status
```

## Alternative: Direct Blueprint Command

Since the TCP connection isn't responding, let's try creating actors directly:

1. In UE console, type:
   ```
   ke * spawn_actor Class=/Engine/BasicShapes/Cube.Cube
   ```

## Check Plugin Status

1. Go to **Edit → Plugins**
2. Search for "UnrealMCP"
3. Make sure it's enabled and shows no errors

## If Nothing Works

The UnrealMCP plugin might need to be:
1. Recompiled for UE 5.5
2. Started manually
3. Configured differently

Let me know what you see in the UE console!