#pragma once

#include "CoreMinimal.h"
#include "HttpServerModule.h"
#include "IHttpRouter.h"
#include "Dom/JsonObject.h"

class FVHCILabWebServer
{
public:
    FVHCILabWebServer();
    ~FVHCILabWebServer();

    void Start();
    void Stop();

private:
    TSharedPtr<IHttpRouter> HttpRouter;
    
    void RegisterRoutes();
    
    // Route handlers
    bool HandleExecuteCommand(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    bool HandleGetProjectInfo(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    bool HandleCreateActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    bool HandleGetActors(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    bool HandleModifyActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    bool HandleDeleteActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete);
    
    // Helper functions
    TSharedPtr<FJsonObject> ParseJsonBody(const FHttpServerRequest& Request);
    TUniquePtr<FHttpServerResponse> CreateJsonResponse(bool bSuccess, const TSharedPtr<FJsonObject>& Data = nullptr, const FString& Error = TEXT(""));
};