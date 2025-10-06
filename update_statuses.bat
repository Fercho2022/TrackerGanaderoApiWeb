@echo off
echo Actualizando estados de animales en la base de datos...
echo.

:: Ejecutar el script SQL
psql -h localhost -U postgres -d tracker_ganadero -f update_animal_statuses.sql

echo.
echo Actualizacion completada!
pause