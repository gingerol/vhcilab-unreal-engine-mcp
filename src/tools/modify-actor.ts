import { Tool } from './types.js';

export const modifyActorTool: Tool = {
  name: 'modify_actor',
  description: 'Modify properties of an existing actor',
  inputSchema: {
    type: 'object',
    properties: {
      actorId: {
        type: 'string',
        description: 'The ID or name of the actor to modify',
      },
      properties: {
        type: 'object',
        description: 'Properties to modify (e.g., location, rotation, scale, visibility, material)',
      },
    },
    required: ['actorId', 'properties'],
  },
  handler: async (client, args) => {
    return client.modifyActor(args.actorId, args.properties);
  },
};