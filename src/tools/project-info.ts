import { Tool } from './types.js';

export const projectInfoTool: Tool = {
  name: 'project_info',
  description: 'Get information about the current Unreal Engine project',
  inputSchema: {
    type: 'object',
    properties: {},
  },
  handler: async (client) => {
    return client.executeCommand('get_project_info');
  },
};