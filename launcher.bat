@echo off
color d
:menu
cls
echo =============================================
echo               SwapX Program Menu             
echo =============================================
echo 1. Launch SwapX
echo 2. About SwapX
echo 3. Exit
echo =============================================
set /p choice="Choose an option (1 to 3): "

if "%choice%"=="1" goto Launch
if "%choice%"=="2" goto tutorial
if "%choice%"=="3" goto end

echo Invalid choice. Please select a valid option.
pause
goto menu

:Launch
cls
echo =============================================
echo           Launching SwapX Application        
echo =============================================
start SwapX
goto using

:using
cls
echo  _                            _               
echo | |                          | |              
echo | |     __ _ _   _ _ __   ___| |__   ___ _ __ 
echo | |    / _` | | | | '_ \ / __| '_ \ / _ \ '__|
echo | |___| (_| | |_| | | | | (__| | | |  __/ |   
echo \_____/\__,_|\__,_|_| |_|\___|_| |_|\___|_|   
echo                                              
echo =============================================
echo SwapX is running. Have fun swapping faces!
echo =============================================
pause
goto menu

:tutorial
cls
echo =============================================
echo               About SwapX Program            
echo =============================================
echo SwapX is a 1-man coding project. 
echo With SwapX, you can swap faces with ANY person
echo you like in any photo or video.
echo =============================================
pause
goto menu

:end
exit