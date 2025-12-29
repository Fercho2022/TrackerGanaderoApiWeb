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
        private readonly IAlertService _alertService;
        private readonly IAlertRepository _alertRepository;

        public AlertsController(IAlertService alertService, IAlertRepository alertRepository)
        {
            _alertService = alertService;
            _alertRepository = alertRepository;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<AlertDto>>> GetAllAlerts([FromQuery] bool? isResolved = null)
        {
            var alerts = await _alertRepository.GetAllAsync();
            var alertDtos = alerts.Select(a => new AlertDto
            {
                Id = a.Id,
                Type = a.Type,
                Title = GetAlertTitle(a.Type, a.Severity),
                Severity = a.Severity,
                Message = a.Message,
                AnimalId = a.AnimalId,
                FarmId = a.Animal?.FarmId,
                AnimalName = a.Animal?.Name ?? "N/A",
                FarmName = a.Animal?.Farm?.Name,
                IsRead = a.IsRead,
                IsResolved = a.IsResolved,
                CreatedAt = a.CreatedAt,
                ResolvedAt = a.ResolvedAt
            });

            if (isResolved.HasValue)
                alertDtos = alertDtos.Where(a => a.IsResolved == isResolved.Value);

            return Ok(alertDtos.OrderByDescending(a => a.CreatedAt));
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

        private static string GetAlertTitle(string type, string severity)
        {
            return type switch
            {
                "OutOfBounds" => "🚨 Animal Fuera del Área",
                "LowActivity" => "😴 Baja Actividad",
                "HighActivity" => "🏃 Alta Actividad",
                "Immobility" => "🛑 Animal Inmóvil",
                "PossibleHeat" => "🔥 Posible Celo",
                _ => $"⚠️ Alerta {severity}"
            };
        }
    }
}
