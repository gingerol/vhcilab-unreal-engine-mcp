import { Tool } from './types.js';

export const buildLightingTool: Tool = {
  name: 'build_lighting',
  description: 'Build lighting for the current level',
  inputSchema: {
    type: 'object',
    properties: {
      quality: {
        type: 'string',
        enum: ['Preview', 'Medium', 'High', 'Production'],
        description: 'Lighting build quality',
      },
    },
  },
  handler: async (client) => {
    return client.buildLighting();
  },
};