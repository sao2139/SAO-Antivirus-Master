; Script generated for SAO-Antivirus (Project Aegis)
; UPDATED FOR: Auto-Update System (Enterprise Grade)
; LANGUAGES: ENGLISH & SPANISH
; IMAGES: BMP FORMAT

#define MyAppName "SAO-Antivirus"
; CAMBIO 1: Incrementamos la versión para que el sistema detecte que es nuevo
#define MyAppVersion "1.0.1 Guardian Edition"
#define MyAppPublisher "Kirito Dev" 
#define MyAppExeName "SAO-Antivirus.exe"

[Setup]
; --- Application Identity ---
; ¡IMPORTANTE! Este AppId es el mismo que me pasaste. NO LO CAMBIES.
; Gracias a que es idéntico, Windows sabe que es una actualización y no un programa nuevo.
AppId={{A1B2C3D4-E5F6-7890-SAO-PROJECT-AEGIS}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes

; --- UPDATE SETTINGS (NUEVO: Lógica Empresarial) ---
; Detecta si la app está corriendo y la cierra suavemente para poder actualizar los archivos .exe
CloseApplications=yes
; Evita que la app se reinicie sola al terminar (tu código Python controla el reinicio si quieres)
RestartApplications=no
; Si ya está instalado, no pregunta la carpeta de nuevo (Actualización Directa/Silenciosa)
DisableDirPage=auto

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
; CAMBIO CRÍTICO: 'onlyifdoesntexist' evita que la actualización borre la configuración del usuario.
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Dirs]
Name: "{app}\quarantine_vault"
Name: "{app}\database"
Name: "{app}\logs"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\logo.ico"

[Run]
; El flag 'nowait' permite que el instalador termine y tu script Python no se quede colgado esperando.
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser