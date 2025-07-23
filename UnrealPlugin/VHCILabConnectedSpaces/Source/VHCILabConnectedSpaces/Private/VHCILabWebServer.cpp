#include "VHCILabWebServer.h"
#include "HttpServerModule.h"
#include "HttpServerRequest.h"
#include "HttpServerResponse.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Editor.h"
#include "LevelEditorSubsystem.h"
#include "EditorActorSubsystem.h"
#include "UnrealEdGlobals.h"
#include "Editor/UnrealEdEngine.h"

FVHCILabWebServer::FVHCILabWebServer()
{
}

FVHCILabWebServer::~FVHCILabWebServer()
{
    Stop();
}

void FVHCILabWebServer::Start()
{
    FHttpServerModule& HttpServerModule = FHttpServerModule::Get();
    HttpRouter = HttpServerModule.GetHttpRouter(8080);
    
    if (HttpRouter.IsValid())
    {
        RegisterRoutes();
        HttpServerModule.StartAllListeners();
        UE_LOG(LogTemp, Log, TEXT("VHCI Lab Web Server started on port 8080"));
    }
}

void FVHCILabWebServer::Stop()
{
    if (HttpRouter.IsValid())
    {
        FHttpServerModule::Get().StopAllListeners();
        HttpRouter.Reset();
    }
}

void FVHCILabWebServer::RegisterRoutes()
{
    HttpRouter->BindRoute(FHttpPath(TEXT("/api/execute")), EHttpServerRequestVerbs::VERB_POST,
        [this](const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
        {
            return HandleExecuteCommand(Request, OnComplete);
        });
}

bool FVHCILabWebServer::HandleExecuteCommand(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    TSharedPtr<FJsonObject> RequestJson = ParseJsonBody(Request);
    if (!RequestJson.IsValid())
    {
        OnComplete(CreateJsonResponse(false, nullptr, TEXT("Invalid JSON")));
        return true;
    }

    FString Command;
    if (!RequestJson->TryGetStringField(TEXT("command"), Command))
    {
        OnComplete(CreateJsonResponse(false, nullptr, TEXT("Missing command field")));
        return true;
    }

    TSharedPtr<FJsonObject> Params;
    RequestJson->TryGetObjectField(TEXT("params"), Params);

    // Route to specific handlers based on command
    if (Command == TEXT("GetProjectInfo"))
    {
        return HandleGetProjectInfo(Request, OnComplete);
    }
    else if (Command == TEXT("CreateActor"))
    {
        return HandleCreateActor(Request, OnComplete);
    }
    else if (Command == TEXT("GetActors"))
    {
        return HandleGetActors(Request, OnComplete);
    }
    else if (Command == TEXT("ConsoleCommand"))
    {
        FString ConsoleCmd;
        if (Params && Params->TryGetStringField(TEXT("command"), ConsoleCmd))
        {
            if (GEditor)
            {
                GEditor->Exec(GEditor->GetEditorWorldContext().World(), *ConsoleCmd);
                OnComplete(CreateJsonResponse(true));
                return true;
            }
        }
    }
    else if (Command == TEXT("SaveAll"))
    {
        if (GEditor)
        {
            GEditor->SaveAll();
            OnComplete(CreateJsonResponse(true));
            return true;
        }
    }

    OnComplete(CreateJsonResponse(false, nullptr, FString::Printf(TEXT("Unknown command: %s"), *Command)));
    return true;
}

bool FVHCILabWebServer::HandleGetProjectInfo(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    TSharedPtr<FJsonObject> ResponseData = MakeShareable(new FJsonObject);
    
    if (GEditor && GEditor->GetEditorWorldContext().World())
    {
        UWorld* World = GEditor->GetEditorWorldContext().World();
        ResponseData->SetStringField(TEXT("projectName"), FApp::GetProjectName());
        ResponseData->SetStringField(TEXT("engineVersion"), FEngineVersion::Current().ToString());
        ResponseData->SetStringField(TEXT("worldName"), World->GetMapName());
    }

    OnComplete(CreateJsonResponse(true, ResponseData));
    return true;
}

bool FVHCILabWebServer::HandleCreateActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    TSharedPtr<FJsonObject> RequestJson = ParseJsonBody(Request);
    if (!RequestJson.IsValid())
    {
        OnComplete(CreateJsonResponse(false, nullptr, TEXT("Invalid JSON")));
        return true;
    }

    TSharedPtr<FJsonObject> Params;
    if (!RequestJson->TryGetObjectField(TEXT("params"), Params))
    {
        OnComplete(CreateJsonResponse(false, nullptr, TEXT("Missing params")));
        return true;
    }

    FString ClassName;
    if (!Params->TryGetStringField(TEXT("className"), ClassName))
    {
        OnComplete(CreateJsonResponse(false, nullptr, TEXT("Missing className")));
        return true;
    }

    // Get location if provided
    FVector Location = FVector::ZeroVector;
    const TSharedPtr<FJsonObject>* LocationObj;
    if (Params->TryGetObjectField(TEXT("location"), LocationObj))
    {
        (*LocationObj)->TryGetNumberField(TEXT("x"), Location.X);
        (*LocationObj)->TryGetNumberField(TEXT("y"), Location.Y);
        (*LocationObj)->TryGetNumberField(TEXT("z"), Location.Z);
    }

    // Create actor
    if (UEditorActorSubsystem* ActorSubsystem = GEditor->GetEditorSubsystem<UEditorActorSubsystem>())
    {
        UWorld* World = GEditor->GetEditorWorldContext().World();
        
        // Handle basic actor types
        AActor* NewActor = nullptr;
        
        if (ClassName == TEXT("CubeActor"))
        {
            NewActor = ActorSubsystem->SpawnActorFromClass(AStaticMeshActor::StaticClass(), Location);
            // Would need additional setup for mesh component
        }
        else if (ClassName == TEXT("PointLight"))
        {
            NewActor = ActorSubsystem->SpawnActorFromClass(APointLight::StaticClass(), Location);
        }
        else if (ClassName == TEXT("DirectionalLight"))
        {
            NewActor = ActorSubsystem->SpawnActorFromClass(ADirectionalLight::StaticClass(), Location);
        }
        else
        {
            // Try to find class by name
            UClass* ActorClass = FindObject<UClass>(ANY_PACKAGE, *ClassName);
            if (ActorClass && ActorClass->IsChildOf(AActor::StaticClass()))
            {
                NewActor = ActorSubsystem->SpawnActorFromClass(ActorClass, Location);
            }
        }

        if (NewActor)
        {
            TSharedPtr<FJsonObject> ResponseData = MakeShareable(new FJsonObject);
            ResponseData->SetStringField(TEXT("actorId"), NewActor->GetName());
            ResponseData->SetStringField(TEXT("actorClass"), NewActor->GetClass()->GetName());
            
            OnComplete(CreateJsonResponse(true, ResponseData));
            return true;
        }
    }

    OnComplete(CreateJsonResponse(false, nullptr, TEXT("Failed to create actor")));
    return true;
}

bool FVHCILabWebServer::HandleGetActors(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    TSharedPtr<FJsonObject> ResponseData = MakeShareable(new FJsonObject);
    TArray<TSharedPtr<FJsonValue>> ActorsArray;

    if (UEditorActorSubsystem* ActorSubsystem = GEditor->GetEditorSubsystem<UEditorActorSubsystem>())
    {
        TArray<AActor*> AllActors = ActorSubsystem->GetAllLevelActors();
        
        for (AActor* Actor : AllActors)
        {
            if (Actor)
            {
                TSharedPtr<FJsonObject> ActorJson = MakeShareable(new FJsonObject);
                ActorJson->SetStringField(TEXT("name"), Actor->GetName());
                ActorJson->SetStringField(TEXT("class"), Actor->GetClass()->GetName());
                
                FVector Location = Actor->GetActorLocation();
                TSharedPtr<FJsonObject> LocationJson = MakeShareable(new FJsonObject);
                LocationJson->SetNumberField(TEXT("x"), Location.X);
                LocationJson->SetNumberField(TEXT("y"), Location.Y);
                LocationJson->SetNumberField(TEXT("z"), Location.Z);
                ActorJson->SetObjectField(TEXT("location"), LocationJson);
                
                ActorsArray.Add(MakeShareable(new FJsonValueObject(ActorJson)));
            }
        }
    }

    ResponseData->SetArrayField(TEXT("actors"), ActorsArray);
    OnComplete(CreateJsonResponse(true, ResponseData));
    return true;
}

bool FVHCILabWebServer::HandleModifyActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    // Implementation for modifying actors
    OnComplete(CreateJsonResponse(false, nullptr, TEXT("Not implemented yet")));
    return true;
}

bool FVHCILabWebServer::HandleDeleteActor(const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
{
    // Implementation for deleting actors
    OnComplete(CreateJsonResponse(false, nullptr, TEXT("Not implemented yet")));
    return true;
}

TSharedPtr<FJsonObject> FVHCILabWebServer::ParseJsonBody(const FHttpServerRequest& Request)
{
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Request.Body);
    FJsonSerializer::Deserialize(Reader, JsonObject);
    return JsonObject;
}

TUniquePtr<FHttpServerResponse> FVHCILabWebServer::CreateJsonResponse(bool bSuccess, const TSharedPtr<FJsonObject>& Data, const FString& Error)
{
    TSharedPtr<FJsonObject> ResponseJson = MakeShareable(new FJsonObject);
    ResponseJson->SetBoolField(TEXT("success"), bSuccess);
    
    if (Data.IsValid())
    {
        ResponseJson->SetObjectField(TEXT("data"), Data);
    }
    
    if (!Error.IsEmpty())
    {
        ResponseJson->SetStringField(TEXT("error"), Error);
    }

    FString ResponseString;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&ResponseString);
    FJsonSerializer::Serialize(ResponseJson.ToSharedRef(), Writer);

    auto Response = FHttpServerResponse::Create(ResponseString, TEXT("application/json"));
    Response->Headers.Add(TEXT("Access-Control-Allow-Origin"), {TEXT("*")});
    
    return Response;
}