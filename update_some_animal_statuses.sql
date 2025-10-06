-- Actualizar algunos animales a diferentes estados para probar el filtrado
-- Mantener los datos en inglés en la BD, pero se mostrarán en español en la UI

-- Cambiar algunos animales a "Sick" (se mostrará como "Enfermo")
UPDATE "Animals" SET "Status" = 'Sick' WHERE "Id" IN (3, 6, 9);

-- Cambiar algunos animales a "Monitoring" (se mostrará como "En observación")
UPDATE "Animals" SET "Status" = 'Monitoring' WHERE "Id" IN (4, 7);

-- Los demás mantienen "Healthy" (se mostrará como "Saludable")

-- Verificar los cambios
SELECT "Id", "Name", "Tag", "Status" FROM "Animals" ORDER BY "Id";

-- Mostrar conteo por estado
SELECT "Status", COUNT(*) as "Cantidad" FROM "Animals" GROUP BY "Status" ORDER BY "Status";