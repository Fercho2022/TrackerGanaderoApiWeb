-- Assign tracker to animal
UPDATE "Animals"
SET "TrackerId" = 3
WHERE "Id" = 3 AND "Name" = 'Vaca GPS Entre Rios';

-- Verify the assignment
SELECT a."Id", a."Name", a."TrackerId", t."DeviceId"
FROM "Animals" a
LEFT JOIN "Trackers" t ON a."TrackerId" = t."Id"
WHERE a."Id" = 3;