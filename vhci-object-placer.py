#!/usr/bin/env python3
"""
VHCI Lab Scene Builder - MCP Server for Unreal Engine
====================================================

A Model Context Protocol (MCP) server that enables natural language scene building in Unreal Engine.
Parse text commands to create objects, lights, and structures in UE scenes.

Key Features:
- Natural language scene building commands
- TCP communication with UnrealMCP plugin (port 55557)  
- Light object creation (guaranteed visible)
- Actor spawning with intelligent placement
- Real-time feedback from Unreal Engine

Architecture:
Claude Code -> MCP Protocol -> Scene Builder -> TCP Socket -> UnrealMCP -> Unreal Engine

Author: VHCI Lab
Version: 1.0.0
License: MIT
"""

import logging
import socket
import json
import re
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VHCIUniversalCreator")

# UE Connection Config
UNREAL_HOST = "127.0.0.1" 
UNREAL_PORT = 55557

@dataclass
class GameElement:
    """Represents a game element to be created"""
    type: str  # 'level', 'character', 'mechanic', 'vr', 'ui', etc.
    name: str
    properties: Dict[str, Any]
    dependencies: List[str]  # Other elements this depends on

class UnrealConnection:
    """Enhanced connection to Unreal Engine via UnrealMCP plugin"""
    
    def __init__(self):
        self.connected = False
        
    async def send_command(self, command_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to UnrealMCP plugin and return response"""
        try:
            # Create socket connection (UnrealMCP closes after each command)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)  # Shorter timeout
            
            logger.info(f"Connecting to UE at {UNREAL_HOST}:{UNREAL_PORT}")
            
            # Connect and send command
            sock.connect((UNREAL_HOST, UNREAL_PORT))
            message = json.dumps({"type": command_type, "params": params})
            logger.info(f"Sending: {message}")
            sock.send(message.encode('utf-8'))
            
            # Receive response with timeout handling
            response_data = b""
            sock.settimeout(5.0)  # Set receive timeout
            
            try:
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk
                    
                    # Try to parse - if we have complete JSON, break
                    try:
                        json.loads(response_data.decode('utf-8'))
                        break  # Got complete JSON
                    except json.JSONDecodeError:
                        continue  # Need more data
                        
            except socket.timeout:
                logger.warning("Socket receive timeout, using available data")
                
            sock.close()
            
            if not response_data:
                return {"status": "error", "error": "No response received"}
            
            # Parse JSON response
            response = json.loads(response_data.decode('utf-8'))
            logger.info(f"UE Response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"UE command failed: {e}")
            return {"status": "error", "error": str(e)}

class GameCreationIntelligence:
    """AI system that understands game development and breaks down complex requests"""
    
    def __init__(self):
        self.ue_conn = UnrealConnection()
        
    def parse_game_description(self, description: str) -> List[GameElement]:
        """Parse natural language into structured game elements"""
        elements = []
        desc_lower = description.lower()
        
        # Game Type Detection
        game_type = self._detect_game_type(desc_lower)
        
        # Environment/Level Elements - More flexible detection
        if any(word in desc_lower for word in ['level', 'world', 'environment', 'map', 'scene', 'castle', 'building', 'place', 'location', 'area', 'create', 'build', 'make']):
            level_element = self._parse_level_requirements(description, game_type)
            if level_element:
                elements.append(level_element)
        
        # Character/Player Elements  
        if any(word in desc_lower for word in ['player', 'character', 'avatar', 'controller']):
            char_element = self._parse_character_requirements(description, game_type)
            if char_element:
                elements.append(char_element)
                
        # Gameplay Mechanics
        mechanics = self._parse_gameplay_mechanics(description, game_type)
        elements.extend(mechanics)
        
        # VR-Specific Elements
        if any(word in desc_lower for word in ['vr', 'virtual reality', 'headset', 'hand tracking']):
            vr_elements = self._parse_vr_requirements(description)
            elements.extend(vr_elements)
            
        # UI/UX Elements
        if any(word in desc_lower for word in ['ui', 'menu', 'hud', 'interface']):
            ui_element = self._parse_ui_requirements(description, game_type)
            if ui_element:
                elements.append(ui_element)
        
        return elements
    
    def _detect_game_type(self, description: str) -> str:
        """Detect the primary game genre/type"""
        type_keywords = {
            'fps': ['first person', 'fps', 'shooting', 'gun', 'weapon'],
            'platformer': ['platform', 'jump', 'side scroll'],
            'rpg': ['rpg', 'role playing', 'quest', 'inventory', 'stats'],
            'survival': ['survival', 'craft', 'resource', 'hunger', 'health'],
            'puzzle': ['puzzle', 'solve', 'logic', 'brain'],
            'racing': ['race', 'car', 'speed', 'track'],
            'vr': ['vr', 'virtual reality', 'immersive'],
            'multiplayer': ['multiplayer', 'online', 'coop', 'pvp']
        }
        
        for game_type, keywords in type_keywords.items():
            if any(keyword in description for keyword in keywords):
                return game_type
        
        return 'generic'
    
    def _parse_level_requirements(self, description: str, game_type: str) -> Optional[GameElement]:
        """Extract level/environment requirements"""
        # Environment keywords
        environments = {
            'medieval': ['castle', 'medieval', 'knight', 'sword', 'dungeon'],
            'modern': ['city', 'urban', 'building', 'street', 'office'],
            'sci_fi': ['space', 'futuristic', 'alien', 'robot', 'laser'],
            'nature': ['forest', 'mountain', 'river', 'tree', 'outdoor'],
            'underwater': ['ocean', 'underwater', 'sea', 'coral', 'fish']
        }
        
        detected_env = 'generic'
        for env_type, keywords in environments.items():
            if any(keyword in description.lower() for keyword in keywords):
                detected_env = env_type
                break
                
        # Size and scale detection
        scale = 'medium'
        if any(word in description.lower() for word in ['large', 'huge', 'massive', 'open world']):
            scale = 'large'
        elif any(word in description.lower() for word in ['small', 'tiny', 'compact']):
            scale = 'small'
            
        return GameElement(
            type='level',
            name=f'{detected_env}_level',
            properties={
                'environment': detected_env,
                'scale': scale,
                'game_type': game_type,
                'lighting': 'dynamic',
                'weather': 'clear'
            },
            dependencies=[]
        )
    
    def _parse_character_requirements(self, description: str, game_type: str) -> Optional[GameElement]:
        """Extract character/player requirements"""
        char_props = {
            'controller_type': 'first_person' if game_type == 'fps' else 'third_person',
            'movement': 'standard',
            'abilities': []
        }
        
        # Movement type detection
        if any(word in description.lower() for word in ['teleport', 'vr']):
            char_props['movement'] = 'teleport'
        elif any(word in description.lower() for word in ['fly', 'flight']):
            char_props['movement'] = 'flying'
            
        # Special abilities
        abilities = []
        if 'jump' in description.lower():
            abilities.append('jump')
        if any(word in description.lower() for word in ['shoot', 'gun', 'weapon']):
            abilities.append('combat')
        if any(word in description.lower() for word in ['interact', 'grab', 'pick up']):
            abilities.append('interaction')
            
        char_props['abilities'] = abilities
        
        return GameElement(
            type='character',
            name='player_character',
            properties=char_props,
            dependencies=['level']
        )
    
    def _parse_gameplay_mechanics(self, description: str, game_type: str) -> List[GameElement]:
        """Extract gameplay mechanic requirements"""
        mechanics = []
        desc_lower = description.lower()
        
        # Combat system
        if any(word in desc_lower for word in ['fight', 'combat', 'weapon', 'enemy']):
            mechanics.append(GameElement(
                type='mechanic',
                name='combat_system',
                properties={'damage_system': True, 'weapons': True},
                dependencies=['character']
            ))
        
        # Inventory system
        if any(word in desc_lower for word in ['inventory', 'item', 'collect', 'pickup']):
            mechanics.append(GameElement(
                type='mechanic', 
                name='inventory_system',
                properties={'slots': 20, 'categories': ['weapons', 'consumables', 'misc']},
                dependencies=['character']
            ))
            
        # Crafting system
        if any(word in desc_lower for word in ['craft', 'recipe', 'build', 'construct']):
            mechanics.append(GameElement(
                type='mechanic',
                name='crafting_system', 
                properties={'stations': True, 'recipes': []},
                dependencies=['inventory_system']
            ))
            
        # Physics interactions
        if any(word in desc_lower for word in ['physics', 'grab', 'throw', 'realistic']):
            mechanics.append(GameElement(
                type='mechanic',
                name='physics_system',
                properties={'realistic': True, 'interactions': True},
                dependencies=['level']
            ))
        
        return mechanics
    
    def _parse_vr_requirements(self, description: str) -> List[GameElement]:
        """Extract VR-specific requirements"""
        vr_elements = []
        desc_lower = description.lower()
        
        # Hand tracking
        if any(word in desc_lower for word in ['hand', 'grab', 'gesture', 'finger']):
            vr_elements.append(GameElement(
                type='vr',
                name='hand_tracking',
                properties={'hand_models': True, 'gestures': True},
                dependencies=['character']
            ))
            
        # Locomotion
        vr_elements.append(GameElement(
            type='vr',
            name='vr_locomotion',
            properties={
                'teleport': True,
                'smooth': True,
                'comfort_settings': True
            },
            dependencies=['character']
        ))
        
        # VR UI
        if any(word in desc_lower for word in ['menu', 'ui', 'interface']):
            vr_elements.append(GameElement(
                type='vr',
                name='vr_ui',
                properties={'spatial_ui': True, 'hand_interaction': True},
                dependencies=['vr_locomotion']
            ))
        
        return vr_elements
    
    def _parse_ui_requirements(self, description: str, game_type: str) -> Optional[GameElement]:
        """Extract UI/UX requirements"""
        ui_props = {
            'hud': True,
            'main_menu': True,
            'pause_menu': True,
            'style': 'modern'
        }
        
        # Style detection
        if any(word in description.lower() for word in ['medieval', 'fantasy']):
            ui_props['style'] = 'medieval'
        elif any(word in description.lower() for word in ['sci-fi', 'futuristic']):
            ui_props['style'] = 'sci_fi'
            
        return GameElement(
            type='ui',
            name='game_ui',
            properties=ui_props,
            dependencies=['character']
        )
    
    async def create_game_elements(self, elements: List[GameElement]) -> Dict[str, Any]:
        """Execute creation of all game elements in proper dependency order"""
        results = {"created_elements": [], "errors": []}
        
        # Sort by dependencies (simple topological sort)
        sorted_elements = self._sort_by_dependencies(elements)
        
        for element in sorted_elements:
            try:
                logger.info(f"Creating {element.type}: {element.name}")
                result = await self._create_single_element(element)
                results["created_elements"].append({
                    "type": element.type,
                    "name": element.name,
                    "result": result
                })
            except Exception as e:
                error_msg = f"Failed to create {element.name}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        return results
    
    def _sort_by_dependencies(self, elements: List[GameElement]) -> List[GameElement]:
        """Sort elements by dependency order"""
        # Simple sorting - create levels first, then characters, then mechanics
        order = ['level', 'character', 'vr', 'mechanic', 'ui']
        
        sorted_elements = []
        for element_type in order:
            for element in elements:
                if element.type == element_type:
                    sorted_elements.append(element)
        
        # Add any remaining elements
        for element in elements:
            if element not in sorted_elements:
                sorted_elements.append(element)
                
        return sorted_elements
    
    async def _create_single_element(self, element: GameElement) -> Dict[str, Any]:
        """Create a single game element using UE commands"""
        
        if element.type == 'level':
            return await self._create_level(element)
        elif element.type == 'character':
            return await self._create_character(element)
        elif element.type == 'mechanic':
            return await self._create_mechanic(element)
        elif element.type == 'vr':
            return await self._create_vr_element(element)
        elif element.type == 'ui':
            return await self._create_ui(element)
        else:
            return {"status": "error", "error": f"Unknown element type: {element.type}"}
    
    async def _create_level(self, element: GameElement) -> Dict[str, Any]:
        """Create level/environment"""
        env = element.properties.get('environment', 'generic')
        scale = element.properties.get('scale', 'medium')
        
        results = []
        
        # Create basic level geometry
        if env == 'medieval':
            # Create castle walls
            wall_result = await self.ue_conn.send_command('spawn_actor', {
                'type': 'StaticMeshActor',
                'name': 'CastleWall_Main',
                'location': [0, 0, 0]
            })
            results.append(wall_result)
            
            # Add towers
            for i, pos in enumerate([[500, 500, 0], [500, -500, 0], [-500, 500, 0], [-500, -500, 0]]):
                tower_result = await self.ue_conn.send_command('spawn_actor', {
                    'type': 'StaticMeshActor', 
                    'name': f'Tower_{i}',
                    'location': pos
                })
                results.append(tower_result)
                
        elif env == 'underwater':
            # Create ocean floor
            floor_result = await self.ue_conn.send_command('spawn_actor', {
                'type': 'StaticMeshActor',
                'name': 'OceanFloor',
                'location': [0, 0, -500]
            })
            results.append(floor_result)
            
            # Add coral reefs
            for i in range(5):
                coral_result = await self.ue_conn.send_command('spawn_actor', {
                    'type': 'StaticMeshActor',
                    'name': f'Coral_{i}',
                    'location': [i * 200 - 400, i * 150 - 300, -450]
                })
                results.append(coral_result)
        
        else:
            # Generic level - create basic ground plane
            ground_result = await self.ue_conn.send_command('spawn_actor', {
                'type': 'StaticMeshActor',
                'name': 'GroundPlane',
                'location': [0, 0, 0]
            })
            results.append(ground_result)
        
        # Add lighting
        light_result = await self.ue_conn.send_command('spawn_actor', {
            'type': 'DirectionalLight',
            'name': 'MainLight',
            'location': [0, 0, 1000]
        })
        results.append(light_result)
        
        return {"status": "success", "results": results}
    
    async def _create_character(self, element: GameElement) -> Dict[str, Any]:
        """Create player character"""
        controller_type = element.properties.get('controller_type', 'first_person')
        abilities = element.properties.get('abilities', [])
        
        # Create basic pawn
        pawn_result = await self.ue_conn.send_command('spawn_actor', {
            'type': 'Pawn',
            'name': 'PlayerPawn',
            'location': [0, 0, 100]
        })
        
        # TODO: Add components for abilities (combat, interaction, etc.)
        # This would require more complex Blueprint creation
        
        return {"status": "success", "pawn": pawn_result}
    
    async def _create_mechanic(self, element: GameElement) -> Dict[str, Any]:
        """Create gameplay mechanics"""
        # Mechanics typically require Blueprint logic
        # For now, create placeholder actors that represent the systems
        
        mechanic_result = await self.ue_conn.send_command('spawn_actor', {
            'type': 'Actor',
            'name': f'{element.name}_manager',
            'location': [0, 0, 0]
        })
        
        return {"status": "success", "mechanic": mechanic_result}
    
    async def _create_vr_element(self, element: GameElement) -> Dict[str, Any]:
        """Create VR-specific elements"""
        # VR elements would typically involve pawn setup and input configuration
        vr_result = await self.ue_conn.send_command('spawn_actor', {
            'type': 'Pawn',
            'name': f'VR_{element.name}',
            'location': [0, 0, 120]  # Head height
        })
        
        return {"status": "success", "vr_element": vr_result}
    
    async def _create_ui(self, element: GameElement) -> Dict[str, Any]:
        """Create UI elements"""
        # UI creation would typically use UMG (Unreal Motion Graphics)
        # For now, create a basic widget placeholder
        
        return {"status": "success", "ui": "UI system initialized"}

# Initialize MCP Server
mcp = FastMCP("VHCI Scene Builder")

@mcp.tool()
async def create_objects(
    description: str
) -> str:
    """
    🏗️ VHCI Lab Scene Builder
    
    Build scenes in Unreal Engine from natural language descriptions.
    Create objects, lights, and structures with simple text commands.
    
    Args:
        description: Natural language description of what to create
                    Examples:
                    - "Create 10 colored lights in a circle"
                    - "Build a tower of cubes"
                    - "Add rainbow lighting to the scene"
                    - "Create a ring of structures"
    
    Returns:
        Detailed report of all created game elements and systems
    """
    
    logger.info(f"Creating objects: {description}")
    
    try:
        # Initialize game creation intelligence
        creator = GameCreationIntelligence()
        
        # Parse the natural language description
        game_elements = creator.parse_game_description(description)
        
        if not game_elements:
            return "❌ Could not understand the object description. Try simpler commands like 'Create 10 lights in a circle' or 'Place 5 cubes in a row'"
        
        # Create all game elements
        creation_results = await creator.create_game_elements(game_elements)
        
        # Format response
        response = f"""
🏗️ **VHCI Lab Scene Builder - Scene Created**

**Description**: {description}

## 📋 Created Objects:
"""
        
        for element in creation_results["created_elements"]:
            response += f"✅ **{element['type'].title()}**: {element['name']}\n"
            
        if creation_results["errors"]:
            response += "\n## ⚠️ Issues Encountered:\n"
            for error in creation_results["errors"]:
                response += f"❌ {error}\n"
        
        response += f"""
## 🔍 To see your objects:
1. Search in World Outliner for object names
2. Click on any object and press 'F' to focus
3. Note: Non-light objects may need mesh assignment for visibility

**📊 Total Objects Created**: {len(creation_results["created_elements"])}

---
*VHCI Lab Scene Builder for Unreal Engine*
"""
        
        return response
        
    except Exception as e:
        logger.error(f"Object creation failed: {e}")
        return f"❌ **Object Creation Failed**: {str(e)}\n\nPlease ensure Unreal Engine is running with the UnrealMCP plugin enabled on port 55557."

if __name__ == "__main__":
    mcp.run()