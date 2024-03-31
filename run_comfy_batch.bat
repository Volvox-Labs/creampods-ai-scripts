

@ECHO OFF
ECHO Starting up batch testing...

@REM how to do error handling

@REM starting server
@REM ..\..\embedded_python\python.exe ..\main.py %* /wait
start  ..\..\python_embeded\python.exe ..\main.py %* 
@REM run api

echo waiting 30s for the server to boot.
TIMEOUT /T 30

set total_runs=5000
set countfiles=5000
set runi=1

:loop
@REM test_iteration = (num_times_to_execute - countfiles) + 1
ECHO Running render %runi% / %total_runs% 
START /B /wait ..\..\python_embeded\python.exe run_ai_with_cache.py %*

set /a countfiles -= 1
set /a runi += 1

@REM ::executes 5000 times

if %countfiles% GTR 0 goto loop
