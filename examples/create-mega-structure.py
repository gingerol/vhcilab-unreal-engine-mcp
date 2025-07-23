#!/usr/bin/env python3
"""
Create a MASSIVE, DISTINCT, and VISIBLE structure using basic UE shapes
"""

import socket
import json
import time
import asyncio

class MegaStructureBuilder:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 55557
        
    def send_command(self, command_type, params):
        """Send command to UE and get response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((self.host, self.port))
            
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
    
    def create_mega_structure(self):
        print("🏗️  CREATING MEGA STRUCTURE")
        print("=" * 50)
        print("Building: Giant Pyramid Complex with Towers!")
        print("Size: EXTRA LARGE - 2000 units wide!")
        print("")
        
        timestamp = str(int(time.time()))
        structures_created = []
        
        # 1. MASSIVE BASE PYRAMID (2000x2000 units!)
        print("🔺 Creating GIANT BASE PYRAMID...")
        base_result = self.send_command("spawn_actor", {
            "type": "StaticMeshActor",
            "name": f"MegaPyramid_{timestamp}",
            "location": [0, 0, 0],
            "scale": [40, 40, 20]  # MASSIVE scale
        })
        if base_result.get('status') == 'success':
            print(f"   ✅ Giant Pyramid: {base_result['result']['name']}")
            structures_created.append("Giant Base Pyramid")
        
        # 2. FOUR CORNER TOWERS (Super tall)
        print("\n🗼 Creating FOUR MASSIVE CORNER TOWERS...")
        tower_positions = [
            [1000, 1000, 0],   # Northeast 
            [1000, -1000, 0],  # Southeast
            [-1000, 1000, 0],  # Northwest
            [-1000, -1000, 0]  # Southwest
        ]
        
        for i, pos in enumerate(tower_positions):
            tower_result = self.send_command("spawn_actor", {
                "type": "StaticMeshActor", 
                "name": f"MegaTower_{i}_{timestamp}",
                "location": pos,
                "scale": [8, 8, 50]  # Super tall towers
            })
            if tower_result.get('status') == 'success':
                print(f"   ✅ Tower {i+1}: {tower_result['result']['name']}")
                structures_created.append(f"Tower {i+1}")
        
        # 3. CENTRAL SPIRE (Goes way up)
        print("\n🏛️  Creating CENTRAL MEGA SPIRE...")
        spire_result = self.send_command("spawn_actor", {
            "type": "StaticMeshActor",
            "name": f"CentralSpire_{timestamp}",
            "location": [0, 0, 500],  # High up
            "scale": [6, 6, 60]  # Super tall spire
        })
        if spire_result.get('status') == 'success':
            print(f"   ✅ Central Spire: {spire_result['result']['name']}")
            structures_created.append("Central Mega Spire")
            
        # 4. FLOATING PLATFORMS (Ring around the spire)
        print("\n🛸 Creating FLOATING PLATFORM RING...")
        for i in range(8):  # 8 platforms in a circle
            angle = i * 45  # degrees
            import math
            x = 600 * math.cos(math.radians(angle))
            y = 600 * math.sin(math.radians(angle))
            z = 300  # Floating height
            
            platform_result = self.send_command("spawn_actor", {
                "type": "StaticMeshActor",
                "name": f"FloatingPlatform_{i}_{timestamp}",
                "location": [x, y, z],
                "scale": [10, 10, 2]  # Large flat platforms
            })
            if platform_result.get('status') == 'success':
                print(f"   ✅ Platform {i+1}: {platform_result['result']['name']}")
                structures_created.append(f"Floating Platform {i+1}")
        
        # 5. GIANT WALL PERIMETER 
        print("\n🧱 Creating MASSIVE PERIMETER WALLS...")
        wall_positions = [
            [1500, 0, 0],    # East wall
            [-1500, 0, 0],   # West wall  
            [0, 1500, 0],    # North wall
            [0, -1500, 0]    # South wall
        ]
        
        for i, pos in enumerate(wall_positions):
            wall_result = self.send_command("spawn_actor", {
                "type": "StaticMeshActor",
                "name": f"PerimeterWall_{i}_{timestamp}",
                "location": pos,
                "scale": [2, 30, 15]  # Long, tall walls
            })
            if wall_result.get('status') == 'success':
                print(f"   ✅ Wall {i+1}: {wall_result['result']['name']}")
                structures_created.append(f"Perimeter Wall {i+1}")
        
        # 6. MEGA SPOTLIGHT
        print("\n💡 Adding MEGA LIGHTING...")
        light_result = self.send_command("spawn_actor", {
            "type": "DirectionalLight",
            "name": f"MegaLight_{timestamp}",
            "location": [0, 0, 2000]  # Way up high
        })
        if light_result.get('status') == 'success':
            print(f"   ✅ Mega Light: {light_result['result']['name']}")
            structures_created.append("Mega Directional Light")
            
        print("\n" + "=" * 50)
        print("🎉 MEGA STRUCTURE COMPLETE!")
        print("=" * 50)
        print(f"📊 Total Elements Created: {len(structures_created)}")
        print("\n📋 Your Mega Structure Includes:")
        for structure in structures_created:
            print(f"   🏗️  {structure}")
            
        print(f"\n🔍 TO SEE YOUR MEGA STRUCTURE:")
        print("1. Clear World Outliner search")
        print(f"2. Search for: 'Mega' or '{timestamp}'")
        print("3. Click on any Mega structure")
        print("4. Press 'F' to focus")
        print("5. Use mouse wheel to ZOOM OUT - this is HUGE!")
        print(f"\n📏 Size: 3000+ units across (MASSIVE!)")
        print(f"🎯 Search term: '{timestamp}' to find all parts")

if __name__ == "__main__":
    builder = MegaStructureBuilder()
    builder.create_mega_structure()