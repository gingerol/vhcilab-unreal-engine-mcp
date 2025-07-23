import { UnrealEngineClient } from '../unreal-client.js';

export interface Tool {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
  handler: (client: UnrealEngineClient, args: any) => Promise<any>;
}