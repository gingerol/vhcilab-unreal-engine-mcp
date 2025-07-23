#!/usr/bin/env python3
"""
Create a simple visible cube that you can definitely see
"""

import socket
import json
import time

def create_visible_cube():
    print("🎯 Creating Visible Test Cube")
    print("=" * 30)
    
    try:
        # Connect to UE
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect(("127.0.0.1", 55557))
        
        # Create a cube with a unique name
        timestamp = str(int(time.time()))
        cube_name = f"VisibleCube_{timestamp}"
        
        message = json.dumps({
            "type": "spawn_actor",
            "params": {
                "type": "StaticMeshActor",
                "name": cube_name,
                "location": [0, 0, 200]  # Higher up so you can see it
            }
        })
        
        print(f"📤 Creating: {cube_name} at [0, 0, 200]")
        sock.send(message.encode('utf-8'))
        
        # Get response
        response_data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            try:
                json.loads(response_data.decode('utf-8'))
                break
            except:
                continue
                
        sock.close()
        
        response = json.loads(response_data.decode('utf-8'))
        
        if response.get('status') == 'success':
            print("✅ SUCCESS: Visible cube created!")
            print(f"   Name: {cube_name}")
            print(f"   Location: {response.get('result', {}).get('location', [0, 0, 200])}")
            print("")
            print("🔍 Now in Unreal Engine:")
            print(f"1. Search for 'VisibleCube' in World Outliner")
            print(f"2. Click on {cube_name}")
            print("3. Press 'F' to focus on it")
            print("4. You should see a cube floating above the ground!")
        else:
            print(f"❌ Failed: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_visible_cube()