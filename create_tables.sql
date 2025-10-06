-- Create tables for CattleTrackingDB without PostGIS
-- This is a temporary solution until PostGIS is properly installed

-- Users table
CREATE TABLE IF NOT EXISTS "Users" (
    "Id" SERIAL PRIMARY KEY,
    "Email" VARCHAR(255) NOT NULL UNIQUE,
    "PasswordHash" VARCHAR(255) NOT NULL,
    "Name" VARCHAR(100),
    "Role" VARCHAR(50) DEFAULT 'User',
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farms table
CREATE TABLE IF NOT EXISTS "Farms" (
    "Id" SERIAL PRIMARY KEY,
    "Name" VARCHAR(200) NOT NULL,
    "Address" VARCHAR(500),
    "Boundaries" TEXT, -- Will store geometry as text for now
    "UserId" INTEGER NOT NULL,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("UserId") REFERENCES "Users"("Id")
);

-- Trackers table
CREATE TABLE IF NOT EXISTS "Trackers" (
    "Id" SERIAL PRIMARY KEY,
    "DeviceId" VARCHAR(100) NOT NULL UNIQUE,
    "Model" VARCHAR(100),
    "BatteryLevel" INTEGER DEFAULT 100,
    "IsActive" BOOLEAN DEFAULT TRUE,
    "LastSignal" TIMESTAMP WITH TIME ZONE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Animals table
CREATE TABLE IF NOT EXISTS "Animals" (
    "Id" SERIAL PRIMARY KEY,
    "Tag" VARCHAR(50) NOT NULL,
    "Name" VARCHAR(100),
    "Breed" VARCHAR(100),
    "Gender" VARCHAR(10),
    "Weight" DECIMAL(10, 2),
    "BirthDate" DATE,
    "IsActive" BOOLEAN DEFAULT TRUE,
    "FarmId" INTEGER NOT NULL,
    "TrackerId" INTEGER,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("FarmId") REFERENCES "Farms"("Id"),
    FOREIGN KEY ("TrackerId") REFERENCES "Trackers"("Id")
);

-- Pastures table
CREATE TABLE IF NOT EXISTS "Pastures" (
    "Id" SERIAL PRIMARY KEY,
    "Name" VARCHAR(100) NOT NULL,
    "Area" TEXT, -- Will store geometry as text for now
    "AreaSize" DECIMAL(10, 2),
    "GrassType" VARCHAR(50),
    "Capacity" INTEGER,
    "IsActive" BOOLEAN DEFAULT TRUE,
    "FarmId" INTEGER NOT NULL,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("FarmId") REFERENCES "Farms"("Id")
);

-- LocationHistories table
CREATE TABLE IF NOT EXISTS "LocationHistories" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "TrackerId" INTEGER NOT NULL,
    "Location" TEXT, -- Will store geometry as text for now
    "Altitude" DOUBLE PRECISION,
    "Speed" DOUBLE PRECISION,
    "ActivityLevel" INTEGER,
    "Temperature" DOUBLE PRECISION,
    "SignalStrength" INTEGER,
    "Timestamp" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id"),
    FOREIGN KEY ("TrackerId") REFERENCES "Trackers"("Id")
);

-- PastureUsages table
CREATE TABLE IF NOT EXISTS "PastureUsages" (
    "Id" SERIAL PRIMARY KEY,
    "PastureId" INTEGER NOT NULL,
    "AnimalId" INTEGER NOT NULL,
    "StartTime" TIMESTAMP WITH TIME ZONE,
    "EndTime" TIMESTAMP WITH TIME ZONE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("PastureId") REFERENCES "Pastures"("Id"),
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- Alerts table
CREATE TABLE IF NOT EXISTS "Alerts" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "Type" VARCHAR(50) NOT NULL,
    "Message" VARCHAR(500),
    "Severity" VARCHAR(20),
    "IsRead" BOOLEAN DEFAULT FALSE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- HealthRecords table
CREATE TABLE IF NOT EXISTS "HealthRecords" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "RecordType" VARCHAR(100),
    "Description" TEXT,
    "Treatment" VARCHAR(500),
    "VeterinarianName" VARCHAR(200),
    "Cost" DECIMAL(10, 2),
    "RecordDate" DATE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- WeightRecords table
CREATE TABLE IF NOT EXISTS "WeightRecords" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "Weight" DECIMAL(10, 2) NOT NULL,
    "Notes" VARCHAR(500),
    "RecordDate" DATE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- BreedingRecords table
CREATE TABLE IF NOT EXISTS "BreedingRecords" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "BreedingDate" DATE,
    "PartnerTag" VARCHAR(50),
    "ExpectedBirthDate" DATE,
    "ActualBirthDate" DATE,
    "Notes" VARCHAR(500),
    "IsSuccessful" BOOLEAN DEFAULT FALSE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- Transactions table
CREATE TABLE IF NOT EXISTS "Transactions" (
    "Id" SERIAL PRIMARY KEY,
    "AnimalId" INTEGER NOT NULL,
    "Type" VARCHAR(50),
    "Amount" DECIMAL(12, 2),
    "Description" VARCHAR(500),
    "TransactionDate" DATE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("AnimalId") REFERENCES "Animals"("Id")
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS "IX_Animals_FarmId" ON "Animals"("FarmId");
CREATE INDEX IF NOT EXISTS "IX_Animals_TrackerId" ON "Animals"("TrackerId");
CREATE INDEX IF NOT EXISTS "IX_Farms_UserId" ON "Farms"("UserId");
CREATE INDEX IF NOT EXISTS "IX_LocationHistories_AnimalId" ON "LocationHistories"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_LocationHistories_TrackerId" ON "LocationHistories"("TrackerId");
CREATE INDEX IF NOT EXISTS "IX_LocationHistories_Timestamp" ON "LocationHistories"("Timestamp");
CREATE INDEX IF NOT EXISTS "IX_Pastures_FarmId" ON "Pastures"("FarmId");
CREATE INDEX IF NOT EXISTS "IX_PastureUsages_PastureId" ON "PastureUsages"("PastureId");
CREATE INDEX IF NOT EXISTS "IX_PastureUsages_AnimalId" ON "PastureUsages"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_Alerts_AnimalId" ON "Alerts"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_Alerts_CreatedAt" ON "Alerts"("CreatedAt");
CREATE INDEX IF NOT EXISTS "IX_HealthRecords_AnimalId" ON "HealthRecords"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_WeightRecords_AnimalId" ON "WeightRecords"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_BreedingRecords_AnimalId" ON "BreedingRecords"("AnimalId");
CREATE INDEX IF NOT EXISTS "IX_Transactions_AnimalId" ON "Transactions"("AnimalId");