using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiWebTrackerGanado.Data;

namespace ApiWebTrackerGanado.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SetupController : ControllerBase
    {
        private readonly CattleTrackingContext _context;

        public SetupController(CattleTrackingContext context)
        {
            _context = context;
        }

        [HttpPost("create-tables")]
        public async Task<IActionResult> CreateTables()
        {
            try
            {
                // Execute raw SQL to create tables
                await _context.Database.ExecuteSqlRawAsync(@"
                    -- Create Customers table
                    CREATE TABLE IF NOT EXISTS ""Customers"" (
                        ""Id"" SERIAL PRIMARY KEY,
                        ""UserId"" INTEGER NOT NULL,
                        ""CompanyName"" VARCHAR(200) NOT NULL,
                        ""TaxId"" VARCHAR(50),
                        ""ContactPerson"" VARCHAR(100),
                        ""Phone"" VARCHAR(20),
                        ""Address"" VARCHAR(500),
                        ""City"" VARCHAR(100),
                        ""Country"" VARCHAR(100),
                        ""Plan"" VARCHAR(50) NOT NULL DEFAULT 'Basic',
                        ""TrackerLimit"" INTEGER NOT NULL DEFAULT 10,
                        ""FarmLimit"" INTEGER NOT NULL DEFAULT 1,
                        ""Status"" VARCHAR(20) NOT NULL DEFAULT 'Active',
                        ""SubscriptionStart"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""SubscriptionEnd"" TIMESTAMP,
                        ""CreatedAt"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""UpdatedAt"" TIMESTAMP NOT NULL DEFAULT NOW()
                    );");

                await _context.Database.ExecuteSqlRawAsync(@"
                    -- Create Licenses table
                    CREATE TABLE IF NOT EXISTS ""Licenses"" (
                        ""Id"" SERIAL PRIMARY KEY,
                        ""CustomerId"" INTEGER NOT NULL,
                        ""LicenseKey"" VARCHAR(50) NOT NULL UNIQUE,
                        ""LicenseType"" VARCHAR(50) NOT NULL DEFAULT 'Basic',
                        ""MaxTrackers"" INTEGER NOT NULL DEFAULT 10,
                        ""MaxFarms"" INTEGER NOT NULL DEFAULT 1,
                        ""MaxUsers"" INTEGER NOT NULL DEFAULT 1,
                        ""Features"" VARCHAR(1000),
                        ""Status"" VARCHAR(20) NOT NULL DEFAULT 'Active',
                        ""IssuedAt"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""ActivatedAt"" TIMESTAMP,
                        ""ExpiresAt"" TIMESTAMP NOT NULL DEFAULT NOW() + INTERVAL '1 year',
                        ""ActivationIp"" VARCHAR(50),
                        ""HardwareId"" VARCHAR(100),
                        ""Notes"" VARCHAR(500),
                        ""CreatedAt"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""UpdatedAt"" TIMESTAMP NOT NULL DEFAULT NOW()
                    );");

                await _context.Database.ExecuteSqlRawAsync(@"
                    -- Create CustomerTrackers table
                    CREATE TABLE IF NOT EXISTS ""CustomerTrackers"" (
                        ""Id"" SERIAL PRIMARY KEY,
                        ""CustomerId"" INTEGER NOT NULL,
                        ""TrackerId"" INTEGER NOT NULL,
                        ""FarmId"" INTEGER,
                        ""AnimalName"" VARCHAR(100),
                        ""Status"" VARCHAR(20) NOT NULL DEFAULT 'Active',
                        ""AssignedAt"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""UnassignedAt"" TIMESTAMP,
                        ""CreatedAt"" TIMESTAMP NOT NULL DEFAULT NOW(),
                        ""UpdatedAt"" TIMESTAMP NOT NULL DEFAULT NOW()
                    );");

                // Insert test customer
                await _context.Database.ExecuteSqlRawAsync(@"
                    INSERT INTO ""Customers"" (""UserId"", ""CompanyName"", ""ContactPerson"", ""Phone"", ""Address"", ""Status"", ""Plan"", ""TrackerLimit"")
                    SELECT 1, 'Test Company', 'Test Contact Person', '123-456-7890', 'Test Address 123', 'Active', 'Premium', 50
                    WHERE NOT EXISTS (SELECT 1 FROM ""Customers"" WHERE ""CompanyName"" = 'Test Company');");

                // Insert test license
                await _context.Database.ExecuteSqlRawAsync(@"
                    INSERT INTO ""Licenses"" (""CustomerId"", ""LicenseKey"", ""LicenseType"", ""MaxTrackers"", ""MaxFarms"", ""MaxUsers"", ""Status"", ""IssuedAt"", ""ExpiresAt"")
                    SELECT c.""Id"", 'TG-2024-1234-5678-9ABC', 'Premium', 50, 5, 10, 'Active', NOW(), NOW() + INTERVAL '1 year'
                    FROM ""Customers"" c
                    WHERE c.""CompanyName"" = 'Test Company'
                      AND NOT EXISTS (SELECT 1 FROM ""Licenses"" WHERE ""LicenseKey"" = 'TG-2024-1234-5678-9ABC');");

                return Ok(new {
                    message = "Tables and test data created successfully",
                    licenseKey = "TG-2024-1234-5678-9ABC",
                    instructions = "You can now activate the license using the license key above"
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = "Error creating tables", error = ex.Message });
            }
        }
    }
}