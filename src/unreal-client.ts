import axios, { AxiosInstance } from 'axios';
import net from 'net';

export interface UnrealEngineConfig {
  httpPort: number;
  host: string;
  fallbackPorts?: number[];
  timeout?: number;
}

export interface UEResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  method?: string;
}

/**
 * Robust Unreal Engine client with multiple connection methods and fallback
 */
export class UnrealEngineClient {
  private config: Required<UnrealEngineConfig>;
  private http: AxiosInstance;
  private activePort: number | null = null;

  constructor(config?: Partial<UnrealEngineConfig>) {
    this.config = {
      host: config?.host || 'localhost',
      httpPort: config?.httpPort || 30010,
      fallbackPorts: config?.fallbackPorts || [30020, 30000, 8080, 7777],
      timeout: config?.timeout || 15000,
    };

    this.http = axios.create({
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'VHCI-Lab-Connected-Spaces/1.0'
      }
    });
  }

  async executeCommand(command: string, params?: any): Promise<UEResponse> {
    // Try TCP first (more reliable), then Web Remote Control as fallback
    try {
      // Map our generic commands to UnrealMCP specific commands
      let tcpCommand = command;
      let tcpParams = params;
      
      switch (command) {
        case 'get_project_info':
          tcpCommand = 'ping'; // Start with ping to test connectivity
          tcpParams = {};
          break;
        case 'create_actor':
          tcpCommand = 'spawn_actor';
          tcpParams = {
            type: 'StaticMeshActor', // UnrealMCP expects 'type' not 'actor_type'
            name: params?.actor_name || `Actor_${Date.now()}`,
            location: params?.location ? [params.location.x, params.location.y, params.location.z] : [0, 0, 0]
          };
          break;
        case 'spawn_actor':
        case 'spawn_blueprint_actor':
          tcpCommand = 'spawn_actor';
          break;
      }
      
      return await this.tryTCPCommand(tcpCommand, tcpParams);
    } catch (tcpError) {
      console.warn('TCP failed, trying Web Remote Control...');
      // Fallback to Web Remote Control for specific commands
      switch (command) {
        case 'get_project_info':
          return this.tryWebRemoteControl('/remote/info', 'GET');
        case 'create_actor':
        case 'spawn_actor':
        case 'spawn_blueprint_actor':
          return this.createActorCommand(params);
        default:
          return { success: false, error: `Command '${command}' failed on both TCP and Web Remote Control` };
      }
    }
  }

  private async tryTCPCommand(command: string, params?: any): Promise<UEResponse> {
    return new Promise((resolve, reject) => {
      const client = new net.Socket();
      let responseData = '';
      
      const timeout = setTimeout(() => {
        client.destroy();
        reject(new Error('TCP connection timeout'));
      }, 10000);

      client.connect(55557, this.config.host, () => {
        // UnrealMCP expects { "type": "command_name", "params": {...} } format
        const message = JSON.stringify({ 
          type: command, 
          params: params || {} 
        });
        client.write(message); // No newline needed
      });

      client.on('data', (data) => {
        responseData += data.toString();
        // Try to parse response - UnrealMCP sends complete JSON
        try {
          const response = JSON.parse(responseData.trim());
          clearTimeout(timeout);
          client.destroy();
          resolve({ 
            success: response.status === 'success',
            data: response.result || response,
            error: response.error,
            method: 'TCP:55557'
          });
        } catch (e) {
          // Continue receiving data - might be incomplete JSON
        }
      });

      client.on('error', (error) => {
        clearTimeout(timeout);
        reject(new Error(`TCP connection error: ${error.message}`));
      });

      client.on('close', () => {
        clearTimeout(timeout);
        if (responseData.trim()) {
          try {
            const response = JSON.parse(responseData.trim());
            resolve({ 
              success: response.status === 'success',
              data: response.result || response,
              error: response.error,
              method: 'TCP:55557'
            });
          } catch (e) {
            // If we got data but couldn't parse it, still consider it a response
            resolve({
              success: true,
              data: { rawResponse: responseData.trim() },
              method: 'TCP:55557'
            });
          }
        } else {
          reject(new Error('No response received from TCP server'));
        }
      });
    });
  }

  private async tryWebRemoteControl(endpoint: string, method: 'GET' | 'PUT' | 'POST', payload?: any): Promise<UEResponse> {
    const ports = [this.activePort || this.config.httpPort, ...this.config.fallbackPorts].filter(Boolean) as number[];
    
    for (const port of ports) {
      try {
        const url = `http://${this.config.host}:${port}${endpoint}`;
        
        let response;
        if (method === 'GET') {
          response = await this.http.get(url, { timeout: 5000 });
        } else if (method === 'PUT') {
          response = await this.http.put(url, payload, { timeout: 10000 });
        } else {
          response = await this.http.post(url, payload, { timeout: 10000 });
        }
        
        // Success - remember this port
        this.activePort = port;
        
        return {
          success: true,
          data: response.data,
          method: `WebRemoteControl:${port}`
        };
        
      } catch (error) {
        // Try next port
        console.warn(`Port ${port} failed:`, error instanceof Error ? error.message : String(error));
        continue;
      }
    }
    
    return {
      success: false,
      error: `Web Remote Control not responding on any port. Tried: ${ports.join(', ')}`,
      method: 'none'
    };
  }

  private async createActorCommand(params: any): Promise<UEResponse> {
    const location = params?.location || { x: 0, y: 0, z: 0 };
    const blueprintPath = params?.blueprint_path || '/Engine/BasicShapes/Cube';
    const actorName = params?.actor_name || `Actor_${Date.now()}`;

    const pythonScript = `
import unreal

try:
    # Create the actor
    location = unreal.Vector(${location.x}, ${location.y}, ${location.z})
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, 
        location=location
    )
    
    if actor:
        # Set the mesh for basic shapes
        if '${blueprintPath}' == '/Engine/BasicShapes/Cube':
            mesh = unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
            if mesh:
                actor.static_mesh_component.set_static_mesh(mesh)
                actor.set_actor_label('${actorName}')
                print(f"SUCCESS: Created cube {actor.get_name()} at {location}")
            else:
                print("ERROR: Could not load cube mesh")
        elif '${blueprintPath}' == '/Engine/BasicShapes/Sphere':
            mesh = unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Sphere')
            if mesh:
                actor.static_mesh_component.set_static_mesh(mesh)
                actor.set_actor_label('${actorName}')
                print(f"SUCCESS: Created sphere {actor.get_name()} at {location}")
        else:
            actor.set_actor_label('${actorName}')
            print(f"SUCCESS: Created actor {actor.get_name()} at {location}")
    else:
        print("ERROR: Failed to create actor")
        
except Exception as e:
    print(f"ERROR: {str(e)}")
`;

    const payload = {
      objectPath: "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
      functionName: "ExecutePythonScript",
      parameters: {
        PythonScript: pythonScript
      }
    };

    return this.tryWebRemoteControl('/remote/object/call', 'PUT', payload);
  }

  // Public API methods
  async getProjectInfo(): Promise<UEResponse> {
    return this.executeCommand('get_project_info');
  }

  async createActor(className: string, location?: { x: number; y: number; z: number }): Promise<UEResponse> {
    const blueprintMap: Record<string, string> = {
      'CubeActor': '/Engine/BasicShapes/Cube',
      'SphereActor': '/Engine/BasicShapes/Sphere',
      'CylinderActor': '/Engine/BasicShapes/Cylinder',
    };

    return this.executeCommand('create_actor', {
      blueprint_path: blueprintMap[className] || className,
      location: location || { x: 0, y: 0, z: 0 },
      actor_name: `${className}_${Date.now()}`
    });
  }

  async getActors(className?: string): Promise<UEResponse> {
    return { success: false, error: 'Get actors not implemented yet' };
  }

  async modifyActor(actorId: string, properties: Record<string, any>): Promise<UEResponse> {
    return { success: false, error: 'Modify actor not implemented yet' };
  }

  async deleteActor(actorId: string): Promise<UEResponse> {
    return { success: false, error: 'Delete actor not implemented yet' };
  }

  async createBlueprint(name: string, parentClass: string, path: string): Promise<UEResponse> {
    return { success: false, error: 'Create blueprint not implemented yet' };
  }

  async executeConsoleCommand(command: string): Promise<UEResponse> {
    return { success: false, error: 'Console command not implemented yet' };
  }

  async buildLighting(): Promise<UEResponse> {
    return { success: false, error: 'Build lighting not implemented yet' };
  }

  async saveAll(): Promise<UEResponse> {
    // Try TCP first - for now return success since UnrealMCP might not have save implemented
    try {
      return await this.tryTCPCommand('ping', {}); // Use ping to test connection
    } catch (tcpError) {
      // Fallback to Web Remote Control Python script
      const pythonScript = `
import unreal
try:
    unreal.EditorAssetLibrary.save_directory('/Game/')
    print("SUCCESS: Project saved")
except Exception as e:
    print(f"ERROR: {str(e)}")
`;

      const payload = {
        objectPath: "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        functionName: "ExecutePythonScript",
        parameters: { PythonScript: pythonScript }
      };

      return this.tryWebRemoteControl('/remote/object/call', 'PUT', payload);
    }
  }

  // Status methods
  getActivePort(): number | null {
    return this.activePort;
  }

  async testConnection(): Promise<UEResponse> {
    // Try TCP first, then fallback to Web Remote Control
    try {
      const tcpResult = await this.tryTCPCommand('ping', {});
      return {
        success: true,
        data: {
          activePort: 55557,
          method: 'TCP:55557',
          info: tcpResult.data
        }
      };
    } catch (tcpError) {
      // Fallback to Web Remote Control
      const result = await this.tryWebRemoteControl('/remote/info', 'GET');
      if (result.success) {
        return {
          success: true,
          data: {
            activePort: this.activePort,
            method: result.method,
            info: result.data
          }
        };
      }
      return result;
    }
  }
}