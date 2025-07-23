import { Tool } from './types.js';

export const saveTool: Tool = {
  name: 'save_all',
  description: 'Save all unsaved assets and levels in the project',
  inputSchema: {
    type: 'object',
    properties: {},
  },
  handler: async (client) => {
    return client.saveAll();
  },
};