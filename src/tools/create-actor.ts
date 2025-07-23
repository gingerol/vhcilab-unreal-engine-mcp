import { Tool } from './types.js';

export const createActorTool: Tool = {
  name: 'create_actor',
  description: 'Create a new actor in the Unreal Engine level. Supports all actor types including meshes, lights, cameras, etc.',
  inputSchema: {
    type: 'object',
    properties: {
      className: {
        type: 'string',
        description: 'The class name of the actor to create (e.g., StaticMeshActor, PointLight, CameraActor, CubeActor)',
      },
      location: {
        type: 'object',
        properties: {
          x: { type: 'number' },
          y: { type: 'number' },
          z: { type: 'number' },
        },
        description: 'World location for the actor',
      },
      rotation: {
        type: 'object',
        properties: {
          pitch: { type: 'number' },
          yaw: { type: 'number' },
          roll: { type: 'number' },
        },
        description: 'Rotation in degrees',
      },
      scale: {
        type: 'object',
        properties: {
          x: { type: 'number' },
          y: { type: 'number' },
          z: { type: 'number' },
        },
        description: 'Scale of the actor',
      },
      name: {
        type: 'string',
        description: 'Custom name for the actor',
      },
    },
    required: ['className'],
  },
  handler: async (client, args) => {
    // Map common actor types to Unreal Engine class types
    const classMap: Record<string, string> = {
      'CubeActor': 'StaticMeshActor',
      'SphereActor': 'StaticMeshActor', 
      'CylinderActor': 'StaticMeshActor',
      'PointLight': 'PointLight',
      'DirectionalLight': 'DirectionalLight',
      'SpotLight': 'SpotLight',
      'CameraActor': 'CameraActor',
      'StaticMeshActor': 'StaticMeshActor'
    };
    
    const actorClass = classMap[args.className] || 'StaticMeshActor';
    
    // Use create_actor command which maps to spawn_actor in UnrealMCP
    return client.createActor(args.className, args.location);
  },
};