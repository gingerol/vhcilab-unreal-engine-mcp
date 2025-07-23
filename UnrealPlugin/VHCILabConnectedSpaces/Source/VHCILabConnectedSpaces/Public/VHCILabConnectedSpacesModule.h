#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FVHCILabConnectedSpacesModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

private:
    void StartWebServer();
    void StopWebServer();
    
    class FVHCILabWebServer* WebServer;
};