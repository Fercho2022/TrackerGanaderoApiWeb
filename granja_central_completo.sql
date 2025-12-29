-- ===========================================
-- CONFIGURACION COMPLETA DE GRANJA CENTRAL
-- ===========================================
-- Ejecutar todo este archivo en pgAdmin o psql

-- 1. CREAR GRANJA CENTRAL
INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
SELECT 'Granja Central', 'Granja Central - Centro de Operaciones GPS', 1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Farms" WHERE "Name" = 'Granja Central');

-- 2. CREAR TRACKERS (COW_NORTH_FARM_01 a COW_NORTH_FARM_10)
INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_01', 'Tracker Granja Central 01', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_01');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_02', 'Tracker Granja Central 02', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_02');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_03', 'Tracker Granja Central 03', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_03');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_04', 'Tracker Granja Central 04', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_04');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_05', 'Tracker Granja Central 05', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_05');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_06', 'Tracker Granja Central 06', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_06');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_07', 'Tracker Granja Central 07', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_07');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_08', 'Tracker Granja Central 08', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_08');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_09', 'Tracker Granja Central 09', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_09');

INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT 'COW_NORTH_FARM_10', 'Tracker Granja Central 10', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_10');

-- 3. CREAR ANIMALES (GC001 a GC010)
INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 01', 'GC001', 'Male', 'Holstein', '2021-01-01', 410.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_01'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC001');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 02', 'GC002', 'Female', 'Angus', '2021-01-01', 420.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_02'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC002');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 03', 'GC003', 'Male', 'Brahman', '2021-01-01', 430.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_03'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC003');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 04', 'GC004', 'Female', 'Hereford', '2021-01-01', 440.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_04'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC004');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 05', 'GC005', 'Male', 'Holstein', '2021-01-01', 450.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_05'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC005');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 06', 'GC006', 'Female', 'Angus', '2021-01-01', 460.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_06'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC006');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 07', 'GC007', 'Male', 'Brahman', '2021-01-01', 470.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_07'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC007');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 08', 'GC008', 'Female', 'Hereford', '2021-01-01', 480.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_08'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC008');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 09', 'GC009', 'Male', 'Holstein', '2021-01-01', 490.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_09'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC009');

INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT 'Vaca Central 10', 'GC010', 'Female', 'Angus', '2021-01-01', 500.0, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_10'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = 'GC010');

-- 4. VERIFICAR CONFIGURACION
SELECT
    f."Name" as farm_name,
    f."Id" as farm_id,
    COUNT(a."Id") as animal_count,
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
WHERE f."Name" = 'Granja Central'
GROUP BY f."Name", f."Id";

-- 5. VERIFICAR TRACKERS Y ANIMALES
SELECT
    t."DeviceId",
    t."Name" as tracker_name,
    a."Name" as animal_name,
    a."Tag"
FROM "Trackers" t
LEFT JOIN "Animals" a ON t."Id" = a."TrackerId"
WHERE t."DeviceId" LIKE 'COW_NORTH_FARM_%'
ORDER BY t."DeviceId";