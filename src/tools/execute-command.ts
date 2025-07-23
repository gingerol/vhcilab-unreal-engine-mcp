import { Tool } from './types.js';

export const executeCommandTool: Tool = {
  name: 'execute_command',
  description: 'Execute a console command in Unreal Engine',
  inputSchema: {
    type: 'object',
    properties: {
      command: {
        type: 'string',
        description: 'The console command to execute',
      },
    },
    required: ['command'],
  },
  handler: async (client, args) => {
    return client.executeConsoleCommand(args.command);
  },
};