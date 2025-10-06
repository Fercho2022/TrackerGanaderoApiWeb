@echo off
echo Actualizando algunos estados de animales...
echo.

:: Ejecutar el script SQL
psql -h localhost -U postgres -d tracker_ganadero -f update_some_animal_statuses.sql

echo.
echo Actualizacion completada!
pause