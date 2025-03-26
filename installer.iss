#define MyAppName "WatsonxPrototype"
#define MyAppVersion "2.0"
#define MyAppPublisher "Costas Hadjineophytou"
#define MyAppURL "https://your-website.com"
#define MyAppExeName "WatsonxPrototype.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-G7H8-I9J0-K1L2M3N4O5P6}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=WatsonxPrototype_Setup
SetupIconFile=frontend\assets\images\watsonx_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\WatsonxPrototype\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\WatsonxPrototype\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".env.template"; DestDir: "{app}"; DestName: ".env"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent 