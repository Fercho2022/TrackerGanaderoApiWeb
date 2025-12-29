-- Script SQL para configurar Granja Central manualmente
-- Ejecutar en pgAdmin o cliente PostgreSQL

-- 1. Crear Granja Central
INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
SELECT 'Granja Central', 'Granja Central - Centro de Operaciones GPS', 1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Farms" WHERE "Name" = 'Granja Central');

-- 2. Crear trackers para los 10 dispositivos del emulador
INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
VALUES
('COW_NORTH_FARM_01', 'Tracker Granja Central 01', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_02', 'Tracker Granja Central 02', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_03', 'Tracker Granja Central 03', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_04', 'Tracker Granja Central 04', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_05', 'Tracker Granja Central 05', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_06', 'Tracker Granja Central 06', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_07', 'Tracker Granja Central 07', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_08', 'Tracker Granja Central 08', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_09', 'Tracker Granja Central 09', 'Active', 'v2.0', NOW()),
('COW_NORTH_FARM_10', 'Tracker Granja Central 10', 'Active', 'v2.0', NOW())
ON CONFLICT ("DeviceId") DO NOTHING;

-- 3. Crear animales para Granja Central
INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT
    'Vaca Central ' || LPAD(tracker_num::text, 2, '0'),
    'GC' || LPAD(tracker_num::text, 3, '0'),
    CASE WHEN tracker_num % 2 = 0 THEN 'Female' ELSE 'Male' END,
    CASE tracker_num % 4
        WHEN 0 THEN 'Holstein'
        WHEN 1 THEN 'Angus'
        WHEN 2 THEN 'Brahman'
        ELSE 'Hereford'
    END,
    '2021-01-01'::date,
    400.0 + (tracker_num * 10),
    'Active',
    (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
    (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_' || LPAD(tracker_num::text, 2, '0')),
    NOW(),
    NOW()
FROM generate_series(1, 10) AS tracker_num
ON CONFLICT ("Tag") DO NOTHING;

-- 4. Verificar la configuración
SELECT
    f."Name" as farm_name,
    f."Id" as farm_id,
    COUNT(a."Id") as animal_count,
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
WHERE f."Name" = 'Granja Central'
GROUP BY f."Name", f."Id";

-- 5. Verificar trackers
SELECT
    t."DeviceId",
    t."Name",
    a."Name" as animal_name,
    a."Tag"
FROM "Trackers" t
LEFT JOIN "Animals" a ON t."Id" = a."TrackerId"
WHERE t."DeviceId" LIKE 'COW_NORTH_FARM_%'
ORDER BY t."DeviceId";