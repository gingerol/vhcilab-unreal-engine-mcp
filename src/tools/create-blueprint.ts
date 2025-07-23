import { Tool } from './types.js';

export const createBlueprintTool: Tool = {
  name: 'create_blueprint',
  description: 'Create a new Blueprint class',
  inputSchema: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: 'Name of the Blueprint',
      },
      parentClass: {
        type: 'string',
        description: 'Parent class to inherit from (e.g., Actor, Pawn, Character)',
      },
      path: {
        type: 'string',
        description: 'Content path where to save the Blueprint (e.g., /Game/Blueprints/)',
      },
    },
    required: ['name', 'parentClass', 'path'],
  },
  handler: async (client, args) => {
    return client.createBlueprint(args.name, args.parentClass, args.path);
  },
};