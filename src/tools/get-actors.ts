import { Tool } from './types.js';

export const getActorsTool: Tool = {
  name: 'get_actors',
  description: 'Get a list of actors in the current level, optionally filtered by class name',
  inputSchema: {
    type: 'object',
    properties: {
      className: {
        type: 'string',
        description: 'Optional filter by actor class name',
      },
    },
  },
  handler: async (client, args) => {
    return client.getActors(args.className);
  },
};