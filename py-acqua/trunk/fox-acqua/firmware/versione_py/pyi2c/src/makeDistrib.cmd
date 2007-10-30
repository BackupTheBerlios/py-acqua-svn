@echo OFF
for %%d in (dist build output src\LOG src\captured src\config) do rmdir /S /Q %%d
del /S /Q *.pyc 
rem path %path%;C:\PYTHON24


python.exe setup.py bdist_wininst 

