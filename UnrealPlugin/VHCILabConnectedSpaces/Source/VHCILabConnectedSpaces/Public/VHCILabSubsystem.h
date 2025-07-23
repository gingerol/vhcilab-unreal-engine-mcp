#pragma once

#include "CoreMinimal.h"
#include "Subsystems/EditorSubsystem.h"
#include "Engine/World.h"
#include "VHCILabSubsystem.generated.h"

UCLASS()
class VHCILABCONNECTEDSPACES_API UVHCILabSubsystem : public UEditorSubsystem
{
	GENERATED_BODY()

public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;

	// MCP Command Interface
	UFUNCTION(CallInEditor = true, Category = "VHCI Lab")
	FString ProcessMCPCommand(const FString& Command, const FString& Parameters);

	// Actor Management
	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Actors")
	AActor* CreateActorAtLocation(const FString& ActorClass, const FVector& Location, const FRotator& Rotation = FRotator::ZeroRotator);

	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Actors")
	TArray<AActor*> GetAllActorsInLevel(const FString& FilterByClass = TEXT(""));

	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Actors")
	bool DeleteActor(AActor* Actor);

	// Blueprint Management
	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Blueprints")
	UBlueprint* CreateBlueprint(const FString& Name, const FString& ParentClass, const FString& PackagePath);

	// Level Operations
	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Level")
	bool SaveCurrentLevel();

	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Level")
	bool BuildLighting();

	// Project Info
	UFUNCTION(CallInEditor = true, Category = "VHCI Lab | Project")
	FString GetProjectInfo();

private:
	class FVHCILabTCPServer* TCPServer;
	class FVHCILabHTTPServer* HTTPServer;
	class FVHCILabWebSocketServer* WebSocketServer;

	// Connection management
	void StartServers();
	void StopServers();

	// Command processing
	FString ProcessActorCommand(const FString& SubCommand, const TSharedPtr<FJsonObject>& Params);
	FString ProcessBlueprintCommand(const FString& SubCommand, const TSharedPtr<FJsonObject>& Params);
	FString ProcessLevelCommand(const FString& SubCommand, const TSharedPtr<FJsonObject>& Params);
};
