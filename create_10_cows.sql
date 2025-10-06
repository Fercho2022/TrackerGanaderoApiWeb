-- Insert 10 trackers for the GPS emulator
INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
VALUES
    ('COW_GPS_ER_01', 'GPS Tracker 1', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_02', 'GPS Tracker 2', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_03', 'GPS Tracker 3', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_04', 'GPS Tracker 4', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_05', 'GPS Tracker 5', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_06', 'GPS Tracker 6', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_07', 'GPS Tracker 7', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_08', 'GPS Tracker 8', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_09', 'GPS Tracker 9', 'Active', 'v1.0', NOW()),
    ('COW_GPS_ER_10', 'GPS Tracker 10', 'Active', 'v1.0', NOW())
ON CONFLICT ("DeviceId") DO NOTHING;

-- Insert 10 animals for the GPS emulator (Farm ID 7 = Entre Rios)
INSERT INTO "Animals" ("TagNumber", "Breed", "Sex", "BirthDate", "Weight", "FarmId", "TrackerId", "CreatedAt")
VALUES
    ('ER001', 'Holstein', 'Female', '2021-03-15', 450.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_01'), NOW()),
    ('ER002', 'Angus', 'Male', '2020-08-22', 520.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_02'), NOW()),
    ('ER003', 'Holstein', 'Female', '2021-05-10', 420.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_03'), NOW()),
    ('ER004', 'Brahman', 'Female', '2020-12-05', 480.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_04'), NOW()),
    ('ER005', 'Angus', 'Male', '2021-01-18', 510.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_05'), NOW()),
    ('ER006', 'Holstein', 'Female', '2021-04-25', 440.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_06'), NOW()),
    ('ER007', 'Hereford', 'Male', '2020-09-12', 495.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_07'), NOW()),
    ('ER008', 'Holstein', 'Female', '2021-06-08', 415.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_08'), NOW()),
    ('ER009', 'Brahman', 'Female', '2020-11-30', 465.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_09'), NOW()),
    ('ER010', 'Angus', 'Male', '2021-02-14', 505.0, 7, (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = 'COW_GPS_ER_10'), NOW())
ON CONFLICT ("TagNumber") DO UPDATE SET
    "TrackerId" = EXCLUDED."TrackerId";

-- Verify the data
SELECT
    a."TagNumber",
    a."Breed",
    t."DeviceId",
    t."Status",
    f."Name" as FarmName
FROM "Animals" a
JOIN "Trackers" t ON a."TrackerId" = t."Id"
JOIN "Farms" f ON a."FarmId" = f."Id"
WHERE f."Id" = 7
ORDER BY a."TagNumber";