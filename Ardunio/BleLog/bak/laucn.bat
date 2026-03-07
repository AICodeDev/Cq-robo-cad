@echo off
ECHO Launching Wan2GP script...

:: Change to the specified directory
cd /d "C:\Arduino\BleLog"

git fetch
git pull


:: Activate conda environment and run the Python script
call conda activate cq
cmd && call conda activate cq &&  python run.py
python run.py


:: Pause to view any output or errors (optional)
pause
