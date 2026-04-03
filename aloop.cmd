@echo off
setlocal enabledelayedexpansion
REM aloop — Simple CLI for your AI agent (Windows)
REM Usage: aloop up         Deploy infrastructure to Azure
REM        aloop start      Pick a loop type and start the agent
REM        aloop stop       Stop the agent gracefully
REM        aloop steer      Upload steering.md changes
REM        aloop status     Check progress (default)
REM        aloop download   Download finished artifacts
REM        aloop down       Tear down all Azure resources
REM        aloop login      Switch Azure account (e.g. aloop login user@live.com)

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "COMMAND=%~1"
set "ARG2=%~2"
if "%COMMAND%"=="" set "COMMAND=status"

REM === Check prerequisites ===
set "MISSING=0"
where azd >nul 2>&1
if errorlevel 1 (
    echo   Azure Developer CLI ^(azd^) not found.
    echo   Install: https://aka.ms/azd-install
    set "MISSING=1"
)
where az >nul 2>&1
if errorlevel 1 (
    echo   Azure CLI ^(az^) not found.
    echo   Install: https://aka.ms/install-azure-cli
    set "MISSING=1"
)
if "%MISSING%"=="1" (
    echo.
    echo   Need an Azure account? https://azure.microsoft.com/free
    exit /b 1
)

REM === Route command ===
if "%COMMAND%"=="login"    goto cmd_login
if "%COMMAND%"=="up"       goto cmd_up
if "%COMMAND%"=="start"    goto cmd_start
if "%COMMAND%"=="stop"     goto cmd_stop
if "%COMMAND%"=="steer"    goto cmd_steer
if "%COMMAND%"=="download" goto cmd_download
if "%COMMAND%"=="status"   goto cmd_status
if "%COMMAND%"=="down"     goto cmd_down
goto cmd_help

REM ──────────────────────────────────────────────
:cmd_login
REM ──────────────────────────────────────────────
echo.
if defined ARG2 (
    echo   Switching to account: %ARG2%
    echo   Sign in as %ARG2% in the browser window that opens.
) else (
    echo   Logging into Azure...
)
az logout >nul 2>&1
az login
azd auth login >nul 2>&1
echo   Logged in. Run 'aloop up' to deploy infrastructure.
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_up
REM ──────────────────────────────────────────────
echo.
echo   Deploying aloop infrastructure to Azure...
echo.
call azd up
if errorlevel 1 exit /b 1
echo.
echo   Infrastructure ready! Run 'aloop start' to begin a loop.
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_start
REM ──────────────────────────────────────────────
set "STEERING=%ROOT%\steering.md"
REM Check if steering.md exists AND is not the default template
if exist "%STEERING%" (
    findstr /c:"Describe what you want the agent to achieve" "%STEERING%" >nul 2>&1
    if errorlevel 1 goto :start_deploy
    REM It's the default template — show loop picker
)

REM No steering.md — offer loop type picker
if not exist "%ROOT%\loops" (
    echo   No steering.md found. Create one with your goal and instructions.
    exit /b 1
)

echo.
echo   Pick a loop type:
echo.
set "COUNT=0"
for /d %%D in ("%ROOT%\loops\*") do (
    set /a COUNT+=1
    set "DIR_!COUNT!=%%D"
    set "NAME_!COUNT!=%%~nxD"
    if exist "%%D\demo.md" (
        echo     !COUNT!. %%~nxD  ^(demo available^)
    ) else (
        echo     !COUNT!. %%~nxD
    )
)

echo.
set "PICK="
set /p "PICK=  Enter number (or press Enter for 1): "
if "%PICK%"=="" set "PICK=1"

set "CHOSEN=!DIR_%PICK%!"
set "CNAME=!NAME_%PICK%!"

if not defined CHOSEN (
    echo   Invalid selection.
    exit /b 1
)

REM Check for template with placeholders vs demo
if exist "!CHOSEN!\steering.md" (
    findstr /r "\[.*\]" "!CHOSEN!\steering.md" >nul 2>&1
    if not errorlevel 1 (
        if exist "!CHOSEN!\demo.md" (
            echo.
            echo   This template has [PLACEHOLDER] fields you'll need to fill in.
            set "USE_DEMO="
            set /p "USE_DEMO=  Try the ready-to-run demo instead? [Y/n]: "
            if "!USE_DEMO!"=="" set "USE_DEMO=Y"
            if /i "!USE_DEMO!"=="Y" (
                copy "!CHOSEN!\demo.md" "%STEERING%" >nul
                echo   Created steering.md from '!CNAME!' demo.
            ) else (
                copy "!CHOSEN!\steering.md" "%STEERING%" >nul
                echo   Created steering.md from '!CNAME!' template. Fill in the [PLACEHOLDERS], then run 'aloop start' again.
                echo.
                exit /b 0
            )
            echo.
            goto :start_deploy
        )
    )
    copy "!CHOSEN!\steering.md" "%STEERING%" >nul
    echo   Created steering.md from '!CNAME!'.
    echo.
    goto :start_deploy
) else if exist "!CHOSEN!\demo.md" (
    copy "!CHOSEN!\demo.md" "%STEERING%" >nul
    echo   Created steering.md from '!CNAME!' demo.
    echo.
    goto :start_deploy
) else (
    echo   No steering template found for '!CNAME!'.
    exit /b 1
)

:start_deploy
REM Reset abort flag if set from a previous stop
findstr /c:"abort: true" "%STEERING%" >nul 2>&1
if not errorlevel 1 (
    powershell -NoProfile -Command "(Get-Content '%STEERING%') -replace 'abort: true','abort: false' | Set-Content '%STEERING%'"
)

REM Check if infrastructure is deployed
set "SA="
for /f "usebackq delims=" %%V in (`azd env get-value AZURE_STORAGE_ACCOUNT_NAME 2^>nul`) do set "SA=%%V"
if not defined SA (
    echo.
    echo   No infrastructure found. Deploying now...
    echo.
    call azd up
    if errorlevel 1 exit /b 1
)

call :get_store
if errorlevel 1 exit /b 1
echo   Uploading steering.md...
call :upload_blob "steering.md" "%STEERING%"
echo.
echo   Agent is running! Check progress with: aloop.cmd status
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_stop
REM ──────────────────────────────────────────────
call :get_store
if errorlevel 1 exit /b 1
set "STEERING=%ROOT%\steering.md"
if not exist "%STEERING%" (
    echo   No steering.md found.
    exit /b 1
)

findstr /c:"abort: false" "%STEERING%" >nul 2>&1
if not errorlevel 1 (
    powershell -NoProfile -Command "(Get-Content '%STEERING%') -replace 'abort: false','abort: true' | Set-Content '%STEERING%'"
    goto :stop_upload
)
findstr /c:"abort: true" "%STEERING%" >nul 2>&1
if errorlevel 1 (
    echo.>> "%STEERING%"
    echo abort: true>> "%STEERING%"
)

:stop_upload
call :upload_blob "steering.md" "%STEERING%"
echo.
echo   Agent will stop on its next iteration.
echo   Run 'aloop start' to restart later.
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_steer
REM ──────────────────────────────────────────────
call :get_store
if errorlevel 1 exit /b 1
set "STEERING=%ROOT%\steering.md"
if not exist "%STEERING%" (
    echo   No steering.md found. Create one first.
    exit /b 1
)
call :upload_blob "steering.md" "%STEERING%"
echo.
echo   Steering updated. Agent picks up changes next iteration.
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_download
REM ──────────────────────────────────────────────
call :get_store
if errorlevel 1 exit /b 1
set "OUTDIR=%ROOT%\output"
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

set "BLOBS="
for /f "usebackq delims=" %%B in (`az storage blob list --account-name "%SA%" -c agent-workspace --prefix "artifacts/" --auth-mode key --query "[].name" -o tsv --only-show-errors 2^>nul`) do (
    set "BLOBS=1"
    set "BNAME=%%~nxB"
    call :download_blob "%%B" "%OUTDIR%\!BNAME!"
    echo   !BNAME!
)

if not defined BLOBS (
    echo.
    echo   No artifacts yet. The agent may still be working.
    echo.
    exit /b 0
)

echo.
echo   Saved to: %OUTDIR%
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_status
REM ──────────────────────────────────────────────
call :get_store
if errorlevel 1 exit /b 1
set "TMP=%TEMP%\aloop_progress_%RANDOM%.json"
call :download_blob "progress.json" "%TMP%" 2>nul
if not exist "%TMP%" (
    echo.
    echo   No progress yet. Agent may still be starting up.
    echo.
    exit /b 0
)

for %%F in ("%TMP%") do if %%~zF==0 (
    echo.
    echo   No progress yet. Agent may still be starting up.
    echo.
    del "%TMP%" 2>nul
    exit /b 0
)

REM Parse progress.json with Python
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(d.get('status','?'))" 2^>nul`) do set "STATUS=%%V"
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(d.get('total_iterations','?'))" 2^>nul`) do set "ITERS=%%V"
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(d.get('best_score','?'))" 2^>nul`) do set "BEST=%%V"
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(d.get('best_iteration','?'))" 2^>nul`) do set "BEST_IT=%%V"
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(' -> '.join(str(s) for s in d.get('scores',[])))" 2^>nul`) do set "SCORES=%%V"
for /f "usebackq delims=" %%V in (`python -c "import json; d=json.load(open(r'%TMP%')); print(d.get('last_updated','?'))" 2^>nul`) do set "UPDATED=%%V"

echo.
echo   aloop
echo   -----
echo   Status:     %STATUS%
echo   Iterations: %ITERS%
echo   Best Score: %BEST%/100 (iteration %BEST_IT%)
echo   Scores:     %SCORES%
echo   Updated:    %UPDATED%
echo.
del "%TMP%" 2>nul
exit /b 0

REM ──────────────────────────────────────────────
:cmd_down
REM ──────────────────────────────────────────────
echo.
echo   This will permanently delete all aloop Azure resources.
echo   Resource group, storage, OpenAI, container app — everything.
echo.
set "CONFIRM="
set /p "CONFIRM=  Are you sure? [y/N]: "
if /i not "%CONFIRM%"=="y" (
    echo   Cancelled.
    echo.
    exit /b 0
)

REM Get resource info from azd environment
set "RG="
set "OPENAI_ENDPOINT="
set "SUB="
for /f "usebackq delims=" %%V in (`azd env get-value AZURE_RESOURCE_GROUP 2^>nul`) do set "RG=%%V"
for /f "usebackq delims=" %%V in (`azd env get-value AZURE_OPENAI_ENDPOINT 2^>nul`) do set "OPENAI_ENDPOINT=%%V"
for /f "usebackq delims=" %%V in (`az account show --query id -o tsv 2^>nul`) do set "SUB=%%V"

if not defined RG (
    echo   No Azure environment found. Nothing to delete.
    echo.
    exit /b 0
)

REM Extract OpenAI account name from endpoint
set "OPENAI_NAME="
if defined OPENAI_ENDPOINT (
    for /f "usebackq delims=" %%V in (`python -c "import re; m=re.match(r'https://([^.]+)\.', '%OPENAI_ENDPOINT%'); print(m.group(1) if m else '')" 2^>nul`) do set "OPENAI_NAME=%%V"
)

REM Get location before deleting
set "LOCATION="
for /f "usebackq delims=" %%V in (`az group show -n "%RG%" --query location -o tsv 2^>nul`) do set "LOCATION=%%V"

REM Step 1: Delete the resource group
echo   Deleting resource group: %RG%...
az group delete -n "%RG%" -y --no-wait >nul 2>&1
echo   Resource group deletion started.

REM Step 2: Purge soft-deleted OpenAI resource
if defined OPENAI_NAME if defined LOCATION (
    echo   Waiting for resource group deletion to register...
    ping -n 11 127.0.0.1 >nul 2>&1
    echo   Purging soft-deleted OpenAI resource: !OPENAI_NAME!...
    az cognitiveservices account purge --name "!OPENAI_NAME!" --location "!LOCATION!" --resource-group "%RG%" --subscription "%SUB%" >nul 2>&1
    echo   OpenAI resource purged.
)

REM Step 3: Clean up azd environment
set "AZD_ENV="
for /f "usebackq delims=" %%V in (`azd env list --query "[?IsDefault].Name" -o tsv 2^>nul`) do set "AZD_ENV=%%V"
if defined AZD_ENV (
    echo   Removing azd environment: !AZD_ENV!...
    azd env delete "!AZD_ENV!" --force --purge >nul 2>&1
    if errorlevel 1 azd env delete "!AZD_ENV!" --force >nul 2>&1
    echo   Environment removed.
)

echo.
echo   All aloop resources deleted. Run 'aloop up' to deploy fresh.
echo.
exit /b 0

REM ──────────────────────────────────────────────
:cmd_help
REM ──────────────────────────────────────────────
echo.
echo   aloop — Run your AI agent
echo.
echo   Infrastructure:
echo     aloop up         Deploy infrastructure to Azure
echo     aloop down       Tear down all Azure resources
echo.
echo   Loop control:
echo     aloop start      Pick a loop type and start the agent
echo     aloop stop       Stop the agent gracefully
echo     aloop steer      Upload steering changes
echo     aloop status     Check progress (default)
echo     aloop download   Download finished artifacts
echo.
echo   Account:
echo     aloop login      Switch Azure account (e.g. aloop login user@live.com)
echo.
echo   Quick start:
echo     1. aloop start   (pick a loop type, deploys to Azure)
echo     2. Edit steering.md with your goal
echo     3. aloop steer   (sends changes to the agent)
echo     4. aloop         (check how it's doing)
echo     5. aloop download (grab the finished work)
echo.
exit /b 0

REM ──────────────────────────────────────────────
REM Helper functions
REM ──────────────────────────────────────────────

:get_store
for /f "usebackq delims=" %%V in (`azd env get-value AZURE_STORAGE_ACCOUNT_NAME 2^>nul`) do set "SA=%%V"
if not defined SA (
    echo   No Azure environment found. Run 'aloop start' first.
    exit /b 1
)
exit /b 0

:upload_blob
az storage blob upload --account-name "%SA%" -c agent-workspace -n "%~1" --file "%~2" --overwrite --auth-mode login --only-show-errors 2>nul
if errorlevel 1 (
    az storage blob upload --account-name "%SA%" -c agent-workspace -n "%~1" --file "%~2" --overwrite --auth-mode key --only-show-errors 2>nul
)
exit /b 0

:download_blob
az storage blob download --account-name "%SA%" -c agent-workspace -n "%~1" --file "%~2" --overwrite --auth-mode login --only-show-errors 2>nul
if errorlevel 1 (
    az storage blob download --account-name "%SA%" -c agent-workspace -n "%~1" --file "%~2" --overwrite --auth-mode key --only-show-errors 2>nul
)
exit /b 0
