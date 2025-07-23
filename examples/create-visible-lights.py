#!/usr/bin/env python3
"""
Create VISIBLE objects using lights - these are always visible in UE!
"""

import socket
import json
import time
import math

def send_command(command_type, params):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect(("127.0.0.1", 55557))
        
        message = json.dumps({"type": command_type, "params": params})
        sock.send(message.encode('utf-8'))
        
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
        return json.loads(response_data.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "error": str(e)}

def create_visible_light_structure():
    print("💡 CREATING VISIBLE LIGHT STRUCTURE")
    print("=" * 40)
    print("Using PointLights - these are ALWAYS visible!")
    print()
    
    timestamp = str(int(time.time()))
    lights_created = []
    
    # Create a ring of colorful point lights
    print("🌈 Creating Ring of Colored Lights...")
    
    num_lights = 8
    radius = 500
    height = 300
    
    colors = [
        [1.0, 0.0, 0.0],  # Red
        [0.0, 1.0, 0.0],  # Green  
        [0.0, 0.0, 1.0],  # Blue
        [1.0, 1.0, 0.0],  # Yellow
        [1.0, 0.0, 1.0],  # Magenta
        [0.0, 1.0, 1.0],  # Cyan
        [1.0, 0.5, 0.0],  # Orange
        [0.5, 0.0, 1.0]   # Purple
    ]
    
    for i in range(num_lights):
        angle = (i / num_lights) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = height
        
        color = colors[i % len(colors)]
        
        light_result = send_command("spawn_actor", {
            "type": "PointLight",
            "name": f"ColorLight_{i}_{timestamp}",
            "location": [x, y, z],
            "intensity": 5000,  # Bright!
            "color": color
        })
        
        if light_result.get('status') == 'success':
            print(f"   ✅ Light {i+1}: {light_result['result']['name']} - {['Red','Green','Blue','Yellow','Magenta','Cyan','Orange','Purple'][i]}")
            lights_created.append(f"Light {i+1} ({['Red','Green','Blue','Yellow','Magenta','Cyan','Orange','Purple'][i]})")
        else:
            print(f"   ❌ Light {i+1} failed: {light_result.get('error', 'Unknown')}")
    
    # Central tower of lights
    print("\n🗼 Creating Central Light Tower...")
    
    for level in range(5):  # 5 levels high
        tower_light = send_command("spawn_actor", {
            "type": "PointLight", 
            "name": f"TowerLight_{level}_{timestamp}",
            "location": [0, 0, 200 + (level * 100)],  # Stack vertically
            "intensity": 8000,
            "color": [1.0, 1.0, 1.0]  # White
        })
        
        if tower_light.get('status') == 'success':
            print(f"   ✅ Tower Level {level+1}: {tower_light['result']['name']}")
            lights_created.append(f"Tower Light Level {level+1}")
    
    print("\n" + "=" * 40)
    print("💡 LIGHT STRUCTURE COMPLETE!")
    print("=" * 40)
    print(f"📊 Total Lights Created: {len(lights_created)}")
    
    for light in lights_created:
        print(f"   💡 {light}")
    
    print(f"\n🔍 TO SEE YOUR LIGHT STRUCTURE:")
    print(f"1. Search for: 'ColorLight' or 'TowerLight' or '{timestamp}'")
    print("2. Click on any light")
    print("3. Press 'F' to focus")
    print("4. Look around - you should see GLOWING COLORED ORBS!")
    print("5. These lights will illuminate the environment!")
    
    print(f"\n🌈 You should see:")
    print("   - 8 colored lights in a circle")
    print("   - 5 white lights stacked vertically in center")
    print("   - All lights glowing and casting light!")
    
    print(f"\n🎯 Search: '{timestamp}' to find all lights")

if __name__ == "__main__":
    create_visible_light_structure()