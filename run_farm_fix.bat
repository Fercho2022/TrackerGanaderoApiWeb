@echo off
echo Running farm assignment fix...
echo This will fix the farm and animal assignments:
echo - Entre Rios farm will have only GPS-ER-001 animal
echo - Granja Norte farm will have ER001-ER010 animals
echo.
pause
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d CattleTrackingDB -f "C:\Cursos\Net\TrackerGanaderoMixto\ProyectoApiWebTrackerGanadero\fix_farm_assignments.sql"
echo.
echo Farm assignment fix completed!
pause