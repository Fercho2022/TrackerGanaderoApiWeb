-- Simple script to manually insert 10 cows and trackers
-- Este script añade 10 vacas y trackers para el farm 7 (Entre Rios)

-- Insert trackers first
INSERT INTO "Trackers" ("DeviceId", "Model", "BatteryLevel", "IsActive", "CreatedAt", "LastSeen") VALUES
('COW_GPS_ER_01', 'GPS-Collar-V3', 95, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_02', 'GPS-Collar-V3', 88, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_03', 'GPS-Collar-V3', 92, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_04', 'GPS-Collar-V3', 97, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_05', 'GPS-Collar-V3', 85, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_06', 'GPS-Collar-V3', 91, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_07', 'GPS-Collar-V3', 89, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_08', 'GPS-Collar-V3', 94, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_09', 'GPS-Collar-V3', 86, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00'),
('COW_GPS_ER_10', 'GPS-Collar-V3', 93, true, '2025-10-02 12:00:00', '2025-10-02 12:00:00');

-- Insert animals with explicit tracker IDs
INSERT INTO "Animals" ("Name", "Tag", "Breed", "Gender", "Status", "FarmId", "TrackerId", "BirthDate", "Weight", "CreatedAt", "UpdatedAt")
SELECT
    'Vaca Entre Rios 01', 'GPS-ER-001', 'Holstein', 'Female', 'Healthy', 7, t."Id", '2021-03-15', 450.5, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_01'
UNION ALL
SELECT
    'Vaca Entre Rios 02', 'GPS-ER-002', 'Angus', 'Female', 'Healthy', 7, t."Id", '2020-08-22', 425.0, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_02'
UNION ALL
SELECT
    'Vaca Entre Rios 03', 'GPS-ER-003', 'Holstein', 'Female', 'Healthy', 7, t."Id", '2021-01-10', 465.2, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_03'
UNION ALL
SELECT
    'Vaca Entre Rios 04', 'GPS-ER-004', 'Hereford', 'Female', 'Monitoring', 7, t."Id", '2020-11-05', 440.8, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_04'
UNION ALL
SELECT
    'Vaca Entre Rios 05', 'GPS-ER-005', 'Holstein', 'Female', 'Healthy', 7, t."Id", '2021-06-18', 435.6, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_05'
UNION ALL
SELECT
    'Vaca Entre Rios 06', 'GPS-ER-006', 'Angus', 'Female', 'Healthy', 7, t."Id", '2020-12-12', 455.3, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_06'
UNION ALL
SELECT
    'Vaca Entre Rios 07', 'GPS-ER-007', 'Holstein', 'Female', 'Healthy', 7, t."Id", '2021-04-25', 448.9, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_07'
UNION ALL
SELECT
    'Vaca Entre Rios 08', 'GPS-ER-008', 'Hereford', 'Female', 'Healthy', 7, t."Id", '2020-09-30', 442.1, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_08'
UNION ALL
SELECT
    'Vaca Entre Rios 09', 'GPS-ER-009', 'Angus', 'Female', 'Sick', 7, t."Id", '2021-02-14', 430.7, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_09'
UNION ALL
SELECT
    'Vaca Entre Rios 10', 'GPS-ER-010', 'Holstein', 'Female', 'Healthy', 7, t."Id", '2021-05-08', 452.4, '2025-10-02 12:00:00', '2025-10-02 12:00:00'
FROM "Trackers" t WHERE t."DeviceId" = 'COW_GPS_ER_10';