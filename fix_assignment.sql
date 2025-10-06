-- Manual assignment of tracker to animal
-- This fixes the issue where animal ID 3 has trackerId null

UPDATE "Animals"
SET "TrackerId" = 3
WHERE "Id" = 3 AND "Name" = 'Vaca GPS Entre Rios';

-- Verify the assignment worked
SELECT a."Id" as AnimalId, a."Name", a."TrackerId", t."DeviceId"
FROM "Animals" a
LEFT JOIN "Trackers" t ON a."TrackerId" = t."Id"
WHERE a."Id" = 3;