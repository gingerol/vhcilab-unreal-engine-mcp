#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { UnrealEngineClient } from './unreal-client.js';
import { tools } from './tools/index.js';

const server = new Server(
  {
    name: 'vhci-lab-unreal-engine',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

const ueClient = new UnrealEngineClient();

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: Object.values(tools).map(tool => ({
    name: tool.name,
    description: tool.description,
    inputSchema: tool.inputSchema,
  })),
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const tool = tools[name];

  if (!tool) {
    throw new McpError(ErrorCode.MethodNotFound, `Tool not found: ${name}`);
  }

  try {
    const result = await tool.handler(ueClient, args);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    throw new McpError(
      ErrorCode.InternalError,
      `Tool execution failed: ${error instanceof Error ? error.message : String(error)}`
    );
  }
});

async function main() {
  console.error('VHCI Lab Connected Spaces - Unreal Engine MCP Server starting...');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error('Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});