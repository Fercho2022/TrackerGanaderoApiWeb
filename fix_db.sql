-- Insert animals directly via SQL for the 10 GPS trackers - FarmId = 7 (Entre Rios - Vaca GPS)
INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
VALUES
  ('Vaca Entre Rios 01', 'ER001', 'Female', 'Holstein', '2021-03-15', 450.0, 'Active', 7, 4, NOW(), NOW()),
  ('Vaca Entre Rios 02', 'ER002', 'Male', 'Angus', '2020-08-22', 520.0, 'Active', 7, 6, NOW(), NOW()),
  ('Vaca Entre Rios 03', 'ER003', 'Female', 'Holstein', '2021-05-10', 420.0, 'Active', 7, 7, NOW(), NOW()),
  ('Vaca Entre Rios 04', 'ER004', 'Female', 'Brahman', '2020-12-05', 480.0, 'Active', 7, 8, NOW(), NOW()),
  ('Vaca Entre Rios 05', 'ER005', 'Male', 'Angus', '2021-01-18', 510.0, 'Active', 7, 9, NOW(), NOW()),
  ('Vaca Entre Rios 06', 'ER006', 'Female', 'Holstein', '2021-04-25', 440.0, 'Active', 7, 10, NOW(), NOW()),
  ('Vaca Entre Rios 07', 'ER007', 'Male', 'Hereford', '2020-09-12', 495.0, 'Active', 7, 11, NOW(), NOW()),
  ('Vaca Entre Rios 08', 'ER008', 'Female', 'Holstein', '2021-06-08', 415.0, 'Active', 7, 12, NOW(), NOW()),
  ('Vaca Entre Rios 09', 'ER009', 'Female', 'Brahman', '2020-11-30', 465.0, 'Active', 7, 13, NOW(), NOW()),
  ('Vaca Entre Rios 10', 'ER010', 'Male', 'Angus', '2021-02-14', 505.0, 'Active', 7, 14, NOW(), NOW())
ON CONFLICT ("Tag") DO UPDATE SET
  "TrackerId" = EXCLUDED."TrackerId",
  "FarmId" = EXCLUDED."FarmId",
  "UpdatedAt" = NOW();

-- Verify the results
SELECT
    a."Tag",
    a."Name",
    t."DeviceId",
    a."TrackerId",
    f."Name" as FarmName
FROM "Animals" a
JOIN "Trackers" t ON a."TrackerId" = t."Id"
JOIN "Farms" f ON a."FarmId" = f."Id"
WHERE f."Id" = 7
ORDER BY a."Tag";