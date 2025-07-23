#include "VHCILabConnectedSpacesModule.h"
#include "VHCILabWebServer.h"

#define LOCTEXT_NAMESPACE "FVHCILabConnectedSpacesModule"

void FVHCILabConnectedSpacesModule::StartupModule()
{
    UE_LOG(LogTemp, Log, TEXT("VHCI Lab Connected Spaces Module Starting"));
    StartWebServer();
}

void FVHCILabConnectedSpacesModule::ShutdownModule()
{
    StopWebServer();
}

void FVHCILabConnectedSpacesModule::StartWebServer()
{
    if (!WebServer)
    {
        WebServer = new FVHCILabWebServer();
        WebServer->Start();
    }
}

void FVHCILabConnectedSpacesModule::StopWebServer()
{
    if (WebServer)
    {
        WebServer->Stop();
        delete WebServer;
        WebServer = nullptr;
    }
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FVHCILabConnectedSpacesModule, VHCILabConnectedSpaces)