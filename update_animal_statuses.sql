-- Script para actualizar los estados de los animales con variedad de estados
-- para probar el filtrado en la página de gestión de animales

-- Primero veamos los animales actuales
SELECT "Id", "Name", "Tag", "Status" FROM "Animals" ORDER BY "Id";

-- Actualizar algunos animales a diferentes estados
-- Animales Saludables (algunos mantienen este estado)
UPDATE "Animals" SET "Status" = 'Saludable' WHERE "Id" IN (1, 2, 5, 8, 10, 13);

-- Animales Enfermos
UPDATE "Animals" SET "Status" = 'Enfermo' WHERE "Id" IN (3, 6, 9, 12);

-- Animales En observación
UPDATE "Animals" SET "Status" = 'En observación' WHERE "Id" IN (4, 7, 11);

-- Verificar los cambios
SELECT "Id", "Name", "Tag", "Status", "UpdatedAt" FROM "Animals" ORDER BY "Id";

-- Mostrar conteo por estado
SELECT "Status", COUNT(*) as "Cantidad" FROM "Animals" GROUP BY "Status" ORDER BY "Status";