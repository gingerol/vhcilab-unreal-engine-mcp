import { Tool } from './types.js';
import { createActorTool } from './create-actor.js';
import { getActorsTool } from './get-actors.js';
import { modifyActorTool } from './modify-actor.js';
import { deleteActorTool } from './delete-actor.js';
import { createBlueprintTool } from './create-blueprint.js';
import { executeCommandTool } from './execute-command.js';
import { projectInfoTool } from './project-info.js';
import { saveTool } from './save.js';
import { buildLightingTool } from './build-lighting.js';

export const tools: Record<string, Tool> = {
  create_actor: createActorTool,
  get_actors: getActorsTool,
  modify_actor: modifyActorTool,
  delete_actor: deleteActorTool,
  create_blueprint: createBlueprintTool,
  execute_command: executeCommandTool,
  project_info: projectInfoTool,
  save_all: saveTool,
  build_lighting: buildLightingTool,
};

export type ToolName = keyof typeof tools;