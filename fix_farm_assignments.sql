-- Fix farm and animal assignments
-- Problem: All animals ER001-ER010 are assigned to Farm ID 7 (Entre Ríos)
-- Solution: Reassign animals properly between farms

-- First, let's check current farm structure
SELECT "Id", "Name", "Address" FROM "Farms" ORDER BY "Id";

-- Check current animals and their farm assignments
SELECT a."Id", a."Name", a."Tag", a."FarmId", f."Name" as "FarmName"
FROM "Animals" a
JOIN "Farms" f ON a."FarmId" = f."Id"
ORDER BY a."Tag";

-- STEP 1: Create Granja Norte farm if it doesn't exist
INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
VALUES ('Granja Norte', 'Granja Norte - Zona de Pastoreo', 1, NOW())
ON CONFLICT ("Name") DO NOTHING;

-- Get the farm IDs for reference
-- Assuming Farm ID 7 = "Entre Ríos - Vaca GPS"
-- We need to get the ID for "Granja Norte"

-- STEP 2: Create the special GPS animal for Entre Ríos farm
-- First, create the special tracker for GPS-ER-001
INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
VALUES ('GPS_ER_001', 'GPS Tracker Especial Entre Ríos', 'Active', 'v2.0', NOW())
ON CONFLICT ("DeviceId") DO NOTHING;

-- Create the special GPS animal for Entre Ríos (should be the only animal in this farm)
INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
VALUES (
    'Vaca GPS Entre Ríos',
    'GPS-ER-001',
    'Female',
    'Holstein GPS',
    '2021-01-01',
    475.0,
    'Active',
    7, -- Entre Ríos farm ID
    (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'GPS_ER_001'),
    NOW(),
    NOW()
)
ON CONFLICT ("Tag") DO UPDATE SET
    "Name" = EXCLUDED."Name",
    "FarmId" = EXCLUDED."FarmId",
    "TrackerId" = EXCLUDED."TrackerId";

-- STEP 3: Update existing animals ER001-ER010 to belong to Granja Norte
-- First get Granja Norte farm ID
WITH granja_norte AS (
    SELECT "Id" as "GranjaNorteId" FROM "Farms" WHERE "Name" = 'Granja Norte'
)
UPDATE "Animals"
SET "FarmId" = (SELECT "GranjaNorteId" FROM granja_norte),
    "UpdatedAt" = NOW()
WHERE "Tag" IN ('ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010');

-- STEP 4: Clean up any duplicate or incorrectly assigned animals
-- Remove any existing animals that might conflict with our new structure
DELETE FROM "Animals"
WHERE "Name" LIKE '%Entre Rios%'
AND "Tag" NOT IN ('GPS-ER-001', 'ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010');

-- STEP 5: Verify the final structure
-- Show animals in Entre Ríos farm (should only be GPS-ER-001)
SELECT 'ENTRE RIOS FARM ANIMALS:' as "Result";
SELECT a."Id", a."Name", a."Tag", a."Breed", f."Name" as "FarmName"
FROM "Animals" a
JOIN "Farms" f ON a."FarmId" = f."Id"
WHERE f."Name" LIKE '%Entre%R%os%' OR f."Id" = 7
ORDER BY a."Tag";

-- Show animals in Granja Norte farm (should be ER001-ER010)
SELECT 'GRANJA NORTE FARM ANIMALS:' as "Result";
SELECT a."Id", a."Name", a."Tag", a."Breed", f."Name" as "FarmName"
FROM "Animals" a
JOIN "Farms" f ON a."FarmId" = f."Id"
WHERE f."Name" = 'Granja Norte'
ORDER BY a."Tag";

-- Show all farms with animal counts
SELECT 'FARM SUMMARY:' as "Result";
SELECT
    f."Id",
    f."Name" as "FarmName",
    COUNT(a."Id") as "AnimalCount",
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as "AnimalTags"
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
GROUP BY f."Id", f."Name"
ORDER BY f."Id";