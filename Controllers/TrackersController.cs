using ApiWebTrackerGanado.Interfaces;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TrackersController : ControllerBase
    {
        private readonly ITrackerRepository _trackerRepository;

        public TrackersController(ITrackerRepository trackerRepository)
        {
            _trackerRepository = trackerRepository;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<object>>> GetTrackers([FromQuery] bool onlyActive = true)
        {
            var trackers = onlyActive
                ? await _trackerRepository.GetActiveTrackersAsync()
                : await _trackerRepository.GetAllAsync();

            var trackerDtos = trackers.Select(t => new
            {
                t.Id,
                t.DeviceId,
                t.Model,
                t.BatteryLevel,
                t.IsActive,
                t.LastSeen,
                AnimalId = t.Animal?.Id,
                AnimalName = t.Animal?.Name,
                t.CreatedAt
            });

            return Ok(trackerDtos);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<object>> GetTracker(int id)
        {
            var tracker = await _trackerRepository.GetByIdAsync(id);
            if (tracker == null) return NotFound();

            var trackerDto = new
            {
                tracker.Id,
                tracker.DeviceId,
                tracker.Model,
                tracker.BatteryLevel,
                tracker.IsActive,
                tracker.LastSeen,
                AnimalId = tracker.Animal?.Id,
                AnimalName = tracker.Animal?.Name,
                tracker.CreatedAt
            };

            return Ok(trackerDto);
        }

        [HttpGet("device/{deviceId}")]
        public async Task<ActionResult<object>> GetTrackerByDeviceId(string deviceId)
        {
            var tracker = await _trackerRepository.GetTrackerWithAnimalAsync(deviceId);
            if (tracker == null) return NotFound();

            var trackerDto = new
            {
                tracker.Id,
                tracker.DeviceId,
                tracker.Model,
                tracker.BatteryLevel,
                tracker.IsActive,
                tracker.LastSeen,
                AnimalId = tracker.Animal?.Id,
                AnimalName = tracker.Animal?.Name,
                FarmId = tracker.Animal?.FarmId,
                FarmName = tracker.Animal?.Farm?.Name,
                tracker.CreatedAt
            };

            return Ok(trackerDto);
        }

        [HttpGet("low-battery")]
        public async Task<ActionResult<IEnumerable<object>>> GetLowBatteryTrackers([FromQuery] int threshold = 20)
        {
            var trackers = await _trackerRepository.GetTrackersWithLowBatteryAsync(threshold);

            var trackerDtos = trackers.Select(t => new
            {
                t.Id,
                t.DeviceId,
                t.BatteryLevel,
                t.LastSeen,
                AnimalId = t.Animal?.Id,
                AnimalName = t.Animal?.Name,
                BatteryStatus = t.BatteryLevel <= 10 ? "Critical" : t.BatteryLevel <= 20 ? "Low" : "Normal"
            });

            return Ok(trackerDtos);
        }

        [HttpPost]
        public async Task<ActionResult<object>> CreateTracker([FromBody] CreateTrackerDto createTrackerDto)
        {
            var tracker = new Models.Tracker
            {
                DeviceId = createTrackerDto.DeviceId,
                Model = createTrackerDto.Model,
                BatteryLevel = 100,
                IsActive = true,
                LastSeen = DateTime.UtcNow,
                CreatedAt = DateTime.UtcNow
            };

            await _trackerRepository.AddAsync(tracker);

            var trackerDto = new
            {
                tracker.Id,
                tracker.DeviceId,
                tracker.Model,
                tracker.BatteryLevel,
                tracker.IsActive,
                tracker.LastSeen,
                tracker.CreatedAt
            };

            return CreatedAtAction(nameof(GetTracker), new { id = tracker.Id }, trackerDto);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateTracker(int id, [FromBody] UpdateTrackerDto updateTrackerDto)
        {
            var tracker = await _trackerRepository.GetByIdAsync(id);
            if (tracker == null) return NotFound();

            tracker.DeviceId = updateTrackerDto.DeviceId;
            tracker.Model = updateTrackerDto.Model;
            tracker.IsActive = updateTrackerDto.IsActive;

            await _trackerRepository.UpdateAsync(tracker);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTracker(int id)
        {
            var tracker = await _trackerRepository.GetByIdAsync(id);
            if (tracker == null) return NotFound();

            await _trackerRepository.DeleteAsync(tracker);
            return NoContent();
        }
    }

    public class CreateTrackerDto
    {
        [Required]
        public string DeviceId { get; set; } = string.Empty;
        [Required]
        public string Model { get; set; } = string.Empty;
    }

    public class UpdateTrackerDto
    {
        [Required]
        public string DeviceId { get; set; } = string.Empty;
        [Required]
        public string Model { get; set; } = string.Empty;
        public bool IsActive { get; set; } = true;
    }
}

