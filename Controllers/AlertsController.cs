using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AlertsController : ControllerBase
    {
        private readonly AlertService _alertService;
        private readonly IAlertRepository _alertRepository;

        public AlertsController(AlertService alertService, IAlertRepository alertRepository)
        {
            _alertService = alertService;
            _alertRepository = alertRepository;
        }

        [HttpGet("farm/{farmId}")]
        public async Task<ActionResult<IEnumerable<AlertDto>>> GetFarmAlerts(int farmId, [FromQuery] bool onlyActive = true)
        {
            var alerts = await _alertService.GetActiveAlertsAsync(farmId);
            return Ok(alerts);
        }

        [HttpGet("farm/{farmId}/critical")]
        public async Task<ActionResult<IEnumerable<AlertDto>>> GetCriticalAlerts(int farmId)
        {
            var criticalAlerts = await _alertRepository.GetCriticalAlertsAsync(farmId);
            var alertDtos = criticalAlerts.Select(a => new AlertDto
            {
                Id = a.Id,
                Type = a.Type,
                Severity = a.Severity,
                Message = a.Message,
                AnimalId = a.AnimalId,
                AnimalName = a.Animal.Name,
                IsRead = a.IsRead,
                IsResolved = a.IsResolved,
                CreatedAt = a.CreatedAt
            });

            return Ok(alertDtos);
        }

        [HttpGet("farm/{farmId}/unread-count")]
        public async Task<ActionResult<int>> GetUnreadAlertsCount(int farmId)
        {
            var count = await _alertRepository.GetUnreadAlertsCountAsync(farmId);
            return Ok(count);
        }

        [HttpPut("{alertId}/read")]
        public async Task<IActionResult> MarkAsRead(int alertId)
        {
            await _alertService.MarkAlertAsReadAsync(alertId);
            return NoContent();
        }

        [HttpPut("{alertId}/resolve")]
        public async Task<IActionResult> ResolveAlert(int alertId)
        {
            await _alertService.ResolveAlertAsync(alertId);
            return NoContent();
        }

        [HttpGet("animal/{animalId}")]
        public async Task<ActionResult<IEnumerable<AlertDto>>> GetAnimalAlerts(int animalId, [FromQuery] bool onlyActive = true)
        {
            var alerts = await _alertRepository.GetAnimalAlertsAsync(animalId, onlyActive);
            var alertDtos = alerts.Select(a => new AlertDto
            {
                Id = a.Id,
                Type = a.Type,
                Severity = a.Severity,
                Message = a.Message,
                AnimalId = a.AnimalId,
                AnimalName = a.Animal?.Name ?? "Unknown",
                IsRead = a.IsRead,
                IsResolved = a.IsResolved,
                CreatedAt = a.CreatedAt
            });

            return Ok(alertDtos);
        }
    }
}
