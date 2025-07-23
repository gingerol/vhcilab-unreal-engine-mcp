import { Tool } from './types.js';

export const deleteActorTool: Tool = {
  name: 'delete_actor',
  description: 'Delete an actor from the level',
  inputSchema: {
    type: 'object',
    properties: {
      actorId: {
        type: 'string',
        description: 'The ID or name of the actor to delete',
      },
    },
    required: ['actorId'],
  },
  handler: async (client, args) => {
    return client.deleteActor(args.actorId);
  },
};