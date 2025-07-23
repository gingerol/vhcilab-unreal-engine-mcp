using UnrealBuildTool;

public class VHCILabConnectedSpaces : ModuleRules
{
    public VHCILabConnectedSpaces(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
        
        PublicIncludePaths.AddRange(
            new string[] {
            }
        );
        
        PrivateIncludePaths.AddRange(
            new string[] {
            }
        );
        
        PublicDependencyModuleNames.AddRange(
            new string[]
            {
                "Core",
                "HTTP",
                "Json",
                "JsonUtilities",
                "WebSockets"
            }
        );
        
        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
                "CoreUObject",
                "Engine",
                "Slate",
                "SlateCore",
                "UnrealEd",
                "EditorSubsystem",
                "BlueprintGraph",
                "KismetCompiler",
                "ToolMenus",
                "EditorWidgets",
                "Projects"
            }
        );
    }
}