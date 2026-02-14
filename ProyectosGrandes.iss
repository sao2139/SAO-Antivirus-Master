; Script generated for SAO-Antivirus (Project Aegis)
; LANGUAGES: ENGLISH & SPANISH
; IMAGES: BMP FORMAT

#define MyAppName "SAO-Antivirus"
#define MyAppVersion "1.0 Guardian Edition"
#define MyAppPublisher "Kirito Dev" 
#define MyAppExeName "SAO-Antivirus.exe"

[Setup]
; --- Application Identity ---
AppId={{A1B2C3D4-E5F6-7890-SAO-PROJECT-AEGIS}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes

; --- LANGUAGE SETTINGS (Ask the user) ---
ShowLanguageDialog=yes

; --- VISUAL AESTHETICS (Must be BMP) ---
SetupIconFile=assets\logo.ico
WizardImageFile=assets\banner_install.bmp
WizardSmallImageFile=assets\logo_sao.bmp

; --- Output Settings ---
OutputDir=Instalador_Final
OutputBaseFilename=Setup_SAO_Antivirus_Multi
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
; Define both languages here
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
; The string "{cm:CreateDesktopIcon}" automatically translates based on selection
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 1. The Main Executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; 2. Assets Folder
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; 3. Configuration and Readme
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Dirs]
Name: "{app}\quarantine_vault"
Name: "{app}\database"
Name: "{app}\logs"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\logo.ico"

[Run]
; "{cm:LaunchProgram...}" also translates automatically
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser