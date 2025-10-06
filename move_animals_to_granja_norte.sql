-- Mover animales ER001-ER010 a Granja Norte (Farm ID 8)
-- Esto corregirá el filtro por granja

-- Verificar granjas antes del cambio
SELECT 'BEFORE CHANGE - Farms:' as info;
SELECT "Id", "Name" FROM "Farms" ORDER BY "Id";

SELECT 'BEFORE CHANGE - Animals by Farm:' as info;
SELECT
    f."Name" as "FarmName",
    COUNT(a."Id") as "AnimalCount",
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as "AnimalTags"
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
GROUP BY f."Id", f."Name"
ORDER BY f."Id";

-- Mover animales ER001-ER010 a granja 8 (Granja norte)
UPDATE "Animals"
SET "FarmId" = 8,
    "UpdatedAt" = NOW()
WHERE "Tag" IN ('ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010');

-- Verificar granjas después del cambio
SELECT 'AFTER CHANGE - Animals by Farm:' as info;
SELECT
    f."Name" as "FarmName",
    COUNT(a."Id") as "AnimalCount",
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as "AnimalTags"
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
GROUP BY f."Id", f."Name"
ORDER BY f."Id";

-- Verificar el resultado esperado:
-- Farm 7 (Entre Rios - Vaca GPS): debería tener solo GPS-ER-001
-- Farm 8 (Granja norte): debería tener ER001, ER002, ER003, ER004, ER005, ER006, ER007, ER008, ER009, ER010