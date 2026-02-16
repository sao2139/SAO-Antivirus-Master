; Script generated for SAO-Antivirus (Project Aegis)
; VERSION: 2.0.0
; COMPATIBILITY: Windows 10/11
; TYPE: Enterprise Auto-Update Ready

#define MyAppName "SAO-Antivirus"
; CAMBIO: Versión 1.0.2 para que el sistema de updates la reconozca
#define MyAppVersion "2.0.0 Guardian Edition"
#define MyAppPublisher "Kirito Dev" 
#define MyAppExeName "SAO-Antivirus.exe"

[Setup]
; --- Identidad de la Aplicación ---
; MANTENER ESTE ID IGUAL SIEMPRE para permitir actualizaciones
AppId={{A1B2C3D4-E5F6-7890-SAO-PROJECT-AEGIS}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes

; --- Configuración de Actualización (Enterprise) ---
; Cierra la app vieja si está corriendo
CloseApplications=yes
; No reinicia la app automáticamente (deja que el usuario decida)
RestartApplications=no
; Si ya existe, actualiza sin preguntar ruta (Silencioso)
DisableDirPage=auto

; --- Estética ---
ShowLanguageDialog=yes
SetupIconFile=assets\logo.ico
WizardImageFile=assets\banner_install.bmp
WizardSmallImageFile=assets\logo_sao.bmp

; --- Configuración de Salida ---
OutputDir=Instalador_Final
OutputBaseFilename=Setup_SAO_Antivirus_v1.0.2
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 1. Ejecutable Principal (Asegúrate que esté en la carpeta dist/)
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; 2. Recursos y Assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; 3. Configuración del Usuario
; 'onlyifdoesntexist' es VITAL: No borra la config del usuario si ya tiene una
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist

; 4. Documentación
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Dirs]
; Crear carpetas vacías necesarias
Name: "{app}\quarantine_vault"
Name: "{app}\database"
Name: "{app}\logs"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\logo.ico"

[Run]
; Ejecutar al finalizar
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser