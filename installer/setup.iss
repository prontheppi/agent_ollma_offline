; Phase 8 placeholder for EnterpriseOfflineAI_Setup.exe.
; Installer must not download dependencies, pull models, or perform online checks.

[Setup]
AppName=EnterpriseOfflineAI
AppVersion=0.1.0
DefaultDirName={autopf}\EnterpriseOfflineAI
DefaultGroupName=EnterpriseOfflineAI
OutputBaseFilename=EnterpriseOfflineAI_Setup

[Files]
; Phase 8 will add packaged desktop and backend binaries here.

[Icons]
Name: "{group}\EnterpriseOfflineAI"; Filename: "{app}\EnterpriseOfflineAI.exe"
