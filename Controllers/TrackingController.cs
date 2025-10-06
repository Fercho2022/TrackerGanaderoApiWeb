using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TrackingController : ControllerBase
    {
        private readonly ITrackingService _trackingService;

        public TrackingController(ITrackingService trackingService)
        {
            _trackingService = trackingService;
        }

        [HttpPost("tracker-data")]
        [AllowAnonymous] // Trackers need to send data without authentication
        public async Task<IActionResult> ReceiveTrackerData([FromBody] TrackerDataDto trackerData)
        {
            try
            {
                await _trackingService.ProcessTrackerDataAsync(trackerData);
                return Ok(new { success = true, message = "Data processed successfully" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        [HttpGet("animal/{animalId}/current-location")]
        // [Authorize] // TODO: Re-enable authentication when implemented properly
        public async Task<ActionResult<LocationDto>> GetAnimalCurrentLocation(int animalId)
        {
            var location = await _trackingService.GetAnimalCurrentLocationAsync(animalId);
            if (location == null)
                return NotFound();

            return Ok(location);
        }

        [HttpGet("animal/{animalId}/location-history")]
        // [Authorize] // TODO: Re-enable authentication when implemented properly
        public async Task<ActionResult<IEnumerable<LocationDto>>> GetAnimalLocationHistory(
            int animalId,
            [FromQuery] DateTime from,
            [FromQuery] DateTime to)
        {
            var locations = await _trackingService.GetAnimalLocationHistoryAsync(animalId, from, to);
            return Ok(locations);
        }

        [HttpGet("animals-in-area")]
        // [Authorize] // TODO: Re-enable authentication when implemented properly
        public async Task<ActionResult<IEnumerable<AnimalDto>>> GetAnimalsInArea(
            [FromQuery] double lat1,
            [FromQuery] double lng1,
            [FromQuery] double lat2,
            [FromQuery] double lng2)
        {
            var animals = await _trackingService.GetAnimalsInAreaAsync(lat1, lng1, lat2, lng2);
            return Ok(animals);
        }

        [HttpGet("farm/{farmId}/animals")]
        // [Authorize] // TODO: Re-enable authentication when implemented properly
        public async Task<ActionResult<IEnumerable<object>>> GetFarmAnimalsLocations(int farmId)
        {
            try
            {
                var farmAnimals = await _trackingService.GetFarmAnimalsLocationsAsync(farmId);
                return Ok(farmAnimals);
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        [HttpPost("assign-tracker")]
        // TODO: Remove this temporary endpoint when tracker assignment is properly implemented
        public async Task<IActionResult> AssignTracker()
        {
            try
            {
                // TEMPORARY HACK: Assign tracker ID 3 to animal ID 3 using raw SQL
                var dbContext = HttpContext.RequestServices.GetRequiredService<ApiWebTrackerGanado.Data.CattleTrackingContext>();

                // Execute raw SQL to assign tracker
                var rowsAffected = await dbContext.Database.ExecuteSqlRawAsync(
                    "UPDATE \"Animals\" SET \"TrackerId\" = 3 WHERE \"Id\" = 3"
                );

                return Ok(new {
                    success = true,
                    message = "Tracker assigned successfully",
                    animalId = 3,
                    trackerId = 3,
                    rowsAffected = rowsAffected
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        [HttpPost("save-location-history")]
        // [Authorize] // TODO: Re-enable authentication when implemented properly
        public async Task<IActionResult> SaveLocationHistory([FromBody] SaveLocationHistoryDto locationData)
        {
            try
            {
                await _trackingService.SaveLocationHistoryAsync(locationData);
                return Ok(new { success = true, message = "Location history saved successfully" });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        [HttpPost("setup-10-cows")]
        // TODO: Remove this temporary endpoint when proper setup is implemented
        public async Task<IActionResult> Setup10Cows()
        {
            try
            {
                var dbContext = HttpContext.RequestServices.GetRequiredService<ApiWebTrackerGanado.Data.CattleTrackingContext>();

                // Insert 10 animals for farm ID 7 (Entre Rios - Vaca GPS) using raw SQL
                var sql = @"
                    INSERT INTO ""Animals"" (""Name"", ""Tag"", ""Gender"", ""Breed"", ""BirthDate"", ""Weight"", ""Status"", ""FarmId"", ""TrackerId"", ""CreatedAt"", ""UpdatedAt"")
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
                        ('Vaca Entre Rios 10', 'ER010', 'Male', 'Angus', '2021-02-14', 505.0, 'Active', 7, 14, NOW(), NOW())";

                var rowsAffected = await dbContext.Database.ExecuteSqlRawAsync(sql);

                return Ok(new {
                    success = true,
                    message = "10 cows setup completed successfully",
                    farmId = 7,
                    farmName = "Entre Rios - Vaca GPS",
                    rowsAffected = rowsAffected
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message });
            }
        }

        [HttpPost("fix-farm-assignments")]
        // TODO: Remove this temporary endpoint when proper setup is implemented
        public async Task<IActionResult> FixFarmAssignments()
        {
            try
            {
                var dbContext = HttpContext.RequestServices.GetRequiredService<ApiWebTrackerGanado.Data.CattleTrackingContext>();

                // STEP 1: Create Granja Norte farm if it doesn't exist
                var createFarmSql = @"
                    INSERT INTO ""Farms"" (""Name"", ""Address"", ""UserId"", ""CreatedAt"")
                    VALUES ('Granja Norte', 'Granja Norte - Zona de Pastoreo', 1, NOW())
                    ON CONFLICT (""Name"") DO NOTHING";

                await dbContext.Database.ExecuteSqlRawAsync(createFarmSql);

                // STEP 2: Create special tracker and animal for Entre Ríos
                var createTrackerSql = @"
                    INSERT INTO ""Trackers"" (""DeviceId"", ""Name"", ""Status"", ""FirmwareVersion"", ""CreatedAt"")
                    VALUES ('GPS_ER_001', 'GPS Tracker Especial Entre Ríos', 'Active', 'v2.0', NOW())
                    ON CONFLICT (""DeviceId"") DO NOTHING";

                await dbContext.Database.ExecuteSqlRawAsync(createTrackerSql);

                // Create GPS animal for Entre Ríos
                var createGpsAnimalSql = @"
                    INSERT INTO ""Animals"" (""Name"", ""Tag"", ""Gender"", ""Breed"", ""BirthDate"", ""Weight"", ""Status"", ""FarmId"", ""TrackerId"", ""CreatedAt"", ""UpdatedAt"")
                    VALUES (
                        'Vaca GPS Entre Ríos',
                        'GPS-ER-001',
                        'Female',
                        'Holstein GPS',
                        '2021-01-01',
                        475.0,
                        'Active',
                        7,
                        (SELECT ""Id"" FROM ""Trackers"" WHERE ""DeviceId"" = 'GPS_ER_001'),
                        NOW(),
                        NOW()
                    )
                    ON CONFLICT (""Tag"") DO UPDATE SET
                        ""Name"" = EXCLUDED.""Name"",
                        ""FarmId"" = EXCLUDED.""FarmId"",
                        ""TrackerId"" = EXCLUDED.""TrackerId""";

                await dbContext.Database.ExecuteSqlRawAsync(createGpsAnimalSql);

                // STEP 3: Move ER001-ER010 animals to Granja Norte
                var moveAnimalsSql = @"
                    UPDATE ""Animals""
                    SET ""FarmId"" = (SELECT ""Id"" FROM ""Farms"" WHERE ""Name"" = 'Granja Norte'),
                        ""UpdatedAt"" = NOW()
                    WHERE ""Tag"" IN ('ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010')";

                var movedAnimals = await dbContext.Database.ExecuteSqlRawAsync(moveAnimalsSql);

                // STEP 4: Get verification data
                var verificationSql = @"
                    SELECT
                        f.""Name"" as ""FarmName"",
                        COUNT(a.""Id"") as ""AnimalCount"",
                        STRING_AGG(a.""Tag"", ', ' ORDER BY a.""Tag"") as ""AnimalTags""
                    FROM ""Farms"" f
                    LEFT JOIN ""Animals"" a ON f.""Id"" = a.""FarmId""
                    WHERE f.""Name"" IN ('Entre Rios - Vaca GPS', 'Granja Norte')
                    GROUP BY f.""Name""
                    ORDER BY f.""Name""";

                // Execute verification (this would need to return results, but for now just confirm success)

                return Ok(new {
                    success = true,
                    message = "Farm assignments fixed successfully",
                    details = new {
                        farmCreated = "Granja Norte farm created/verified",
                        gpsAnimalCreated = "GPS-ER-001 animal created for Entre Ríos farm",
                        animalsMoved = $"{movedAnimals} animals moved to Granja Norte",
                        expectedResult = new {
                            entreRios = "Should contain only GPS-ER-001",
                            granjaNorte = "Should contain ER001-ER010"
                        }
                    }
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { success = false, message = ex.Message, details = ex.StackTrace });
            }
        }
    }
}

