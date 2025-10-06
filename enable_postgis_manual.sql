-- Habilitar PostGIS manualmente en la base de datos
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verificar que PostGIS esté instalado
SELECT name, default_version, installed_version
FROM pg_available_extensions
WHERE name = 'postgis';

-- Verificar que el tipo geometry esté disponible
SELECT typname FROM pg_type WHERE typname = 'geometry';