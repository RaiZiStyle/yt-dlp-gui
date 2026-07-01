; installer/setup.iss
#define MyAppName "yt-dlp GUI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Ton Nom"
#define MyAppExeName "yt-dlp-gui.exe"
#define MyAppSourceDir "..\dist\yt-dlp-gui"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=..\installer_output
OutputBaseFilename=yt-dlp-gui-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Demande les droits admin pour installer dans Program Files
PrivilegesRequired=admin

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Copie tout le dossier bundle PyInstaller
Source: "{#MyAppSourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Raccourci dans le menu Démarrer
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Raccourci sur le bureau (optionnel, coché par défaut)
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Lance l'app après installation (optionnel)
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Nettoie les fichiers créés par l'app à la désinstallation
Type: filesandordirs; Name: "{app}"