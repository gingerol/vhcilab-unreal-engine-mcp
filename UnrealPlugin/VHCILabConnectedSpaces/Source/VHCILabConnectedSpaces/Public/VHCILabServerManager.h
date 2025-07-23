#pragma once

#include "CoreMinimal.h"
#include "HAL/Runnable.h"
#include "HAL/RunnableThread.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Dom/JsonObject.h"

// Forward declarations
class UVHCILabSubsystem;

/**
 * Multi-protocol server manager supporting TCP, HTTP, and WebSocket
 * Provides redundancy and fallback mechanisms for robust communication
 */
class VHCILABCONNECTEDSPACES_API FVHCILabServerManager
{
public:
    FVHCILabServerManager(UVHCILabSubsystem* InSubsystem);
    ~FVHCILabServerManager();

    // Server lifecycle
    bool StartAllServers();
    void StopAllServers();
    bool IsAnyServerRunning() const;

    // Configuration
    void SetPorts(int32 TCPPort = 55557, int32 HTTPPort = 30010, int32 WSPort = 30011);
    void SetMaxConnections(int32 MaxConnections = 10);

    // Status monitoring
    TArray<FString> GetServerStatus() const;
    int32 GetActiveConnections() const;

private:
    UVHCILabSubsystem* Subsystem;

    // Server instances
    TUniquePtr<class FVHCILabTCPServer> TCPServer;
    TUniquePtr<class FVHCILabHTTPServer> HTTPServer;
    TUniquePtr<class FVHCILabWebSocketServer> WebSocketServer;

    // Configuration
    int32 TCPPort;
    int32 HTTPPort;
    int32 WSPort;
    int32 MaxConnections;

    // Status tracking
    mutable FCriticalSection StatusMutex;
};

/**
 * TCP Server implementation for direct socket communication
 */
class VHCILABCONNECTEDSPACES_API FVHCILabTCPServer : public FRunnable
{
public:
    FVHCILabTCPServer(UVHCILabSubsystem* InSubsystem, int32 InPort);
    virtual ~FVHCILabTCPServer();

    // FRunnable interface
    virtual bool Init() override;
    virtual uint32 Run() override;
    virtual void Stop() override;
    virtual void Exit() override;

    bool StartServer();
    void StopServer();
    bool IsRunning() const { return bIsRunning; }
    int32 GetActiveConnections() const { return ActiveConnections; }

private:
    UVHCILabSubsystem* Subsystem;
    int32 Port;
    TSharedPtr<FSocket> ListenerSocket;
    FRunnableThread* Thread;
    
    FCriticalSection ConnectionMutex;
    TArray<TSharedPtr<FSocket>> ClientSockets;
    std::atomic<bool> bIsRunning;
    std::atomic<int32> ActiveConnections;

    void HandleClient(TSharedPtr<FSocket> ClientSocket);
    FString ProcessMessage(const FString& Message);
};

/**
 * HTTP Server for REST API communication
 */
class VHCILABCONNECTEDSPACES_API FVHCILabHTTPServer
{
public:
    FVHCILabHTTPServer(UVHCILabSubsystem* InSubsystem, int32 InPort);
    ~FVHCILabHTTPServer();

    bool StartServer();
    void StopServer();
    bool IsRunning() const { return bIsRunning; }

private:
    UVHCILabSubsystem* Subsystem;
    int32 Port;
    std::atomic<bool> bIsRunning;

    // HTTP route handlers
    FString HandleGET(const FString& Path, const TMap<FString, FString>& QueryParams);
    FString HandlePOST(const FString& Path, const FString& Body);
    FString HandlePUT(const FString& Path, const FString& Body);
    FString HandleDELETE(const FString& Path);
};

/**
 * WebSocket Server for real-time bidirectional communication
 */
class VHCILABCONNECTEDSPACES_API FVHCILabWebSocketServer
{
public:
    FVHCILabWebSocketServer(UVHCILabSubsystem* InSubsystem, int32 InPort);
    ~FVHCILabWebSocketServer();

    bool StartServer();
    void StopServer();
    bool IsRunning() const { return bIsRunning; }

    // WebSocket specific functionality
    void BroadcastMessage(const FString& Message);
    void SendToClient(const FString& ClientId, const FString& Message);

private:
    UVHCILabSubsystem* Subsystem;
    int32 Port;
    std::atomic<bool> bIsRunning;

    FCriticalSection ClientMutex;
    TMap<FString, TSharedPtr<class FWebSocketConnection>> Clients;

    void HandleNewConnection(TSharedPtr<class FWebSocketConnection> Connection);
    void HandleClientDisconnection(const FString& ClientId);
    void HandleMessage(const FString& ClientId, const FString& Message);
};