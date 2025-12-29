using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Helpers;
using ApiWebTrackerGanado.Hubs;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Services
{
    public class AlertService : IAlertService 
    {

        private readonly IAlertRepository _alertRepository;
        private readonly IFarmRepository _farmRepository;
        private readonly ILocationHistoryRepository _locationHistoryRepository;
        private readonly IHubContext<LiveTrackingHub> _hubContext;

        public AlertService(
            IAlertRepository alertRepository,
            IFarmRepository farmRepository,
            ILocationHistoryRepository locationHistoryRepository,
            IHubContext<LiveTrackingHub> hubContext)
        {
            _alertRepository = alertRepository;
            _farmRepository = farmRepository;
            _locationHistoryRepository = locationHistoryRepository;
            _hubContext = hubContext;
        }

        public async Task CheckLocationAlertsAsync(Animal animal, LocationHistory location)
        {
            // Check if animal is outside farm boundaries using new boundary system
            var farm = await _farmRepository.GetByIdWithBoundariesAsync(animal.FarmId);

            if (farm?.BoundaryCoordinates != null && farm.BoundaryCoordinates.Any())
            {
                bool isInsideFarm = GeofencingHelper.IsPointInPolygon(
                    location.Latitude,
                    location.Longitude,
                    farm.BoundaryCoordinates);

                if (!isInsideFarm)
                {
                    await CreateAlertAsync(animal, "OutOfBounds", "High",
                        $"{animal.Name} has left the farm boundaries");
                }
            }

            // Check immobility using coordinate-based calculations
            var recentLocations = await _locationHistoryRepository
                .GetRecentLocationsAsync(animal.Id, 2);

            if (recentLocations.Count() >= 20)
            {
                var locations = recentLocations.ToList();
                var maxDistance = 0.0;
                var firstLocation = locations.First();

                foreach (var loc in locations)
                {
                    var distance = GeofencingHelper.CalculateDistance(
                        firstLocation.Latitude, firstLocation.Longitude,
                        loc.Latitude, loc.Longitude);

                    if (distance > maxDistance)
                        maxDistance = distance;
                }

                // If the animal hasn't moved more than 10 meters in the last 20 readings
                if (maxDistance < 10)
                {
                    await CreateAlertAsync(animal, "Immobility", "Medium",
                        $"{animal.Name} has been immobile for over 2 hours");
                }
            }
        }

        public async Task CheckActivityAlertsAsync(Animal animal, int activityLevel)
        {
            var avgActivity = await _locationHistoryRepository
                .GetAverageActivityLevelAsync(animal.Id, 24);

            if (avgActivity > 0)
            {
                if (activityLevel < avgActivity * 0.3 && activityLevel < 20)
                {
                    await CreateAlertAsync(animal, "LowActivity", "Medium",
                        $"{animal.Name} showing unusually low activity levels");
                }

                if (activityLevel > avgActivity * 2 && activityLevel > 80)
                {
                    await CreateAlertAsync(animal, "HighActivity", "Medium",
                        $"{animal.Name} showing unusually high activity levels");
                }
            }
        }

        public async Task CheckBreedingAlertsAsync(Animal animal)
        {
            var recentActivity = await _locationHistoryRepository
                .GetRecentLocationsAsync(animal.Id, 72); // 3 days

            var highActivityDays = recentActivity
                .Where(lh => lh.ActivityLevel > 70)
                .GroupBy(lh => lh.Timestamp.Date)
                .Where(g => g.Count() > 5)
                .Count();

            if (highActivityDays >= 2)
            {
                await CreateAlertAsync(animal, "PossibleHeat", "Low",
                    $"{animal.Name} may be in heat - elevated activity detected");
            }
        }

        public async Task<IEnumerable<AlertDto>> GetActiveAlertsAsync(int farmId)
        {
            var alerts = await _alertRepository.GetFarmAlertsAsync(farmId, true);

            return alerts.Select(a => new AlertDto
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
        }

        public async Task MarkAlertAsReadAsync(int alertId)
        {
            var alert = await _alertRepository.GetByIdAsync(alertId);
            if (alert != null)
            {
                alert.IsRead = true;
                await _alertRepository.UpdateAsync(alert);
            }
        }

        public async Task ResolveAlertAsync(int alertId)
        {
            var alert = await _alertRepository.GetByIdAsync(alertId);
            if (alert != null)
            {
                alert.IsResolved = true;
                alert.ResolvedAt = DateTime.UtcNow;
                await _alertRepository.UpdateAsync(alert);
            }
        }

        private async Task CreateAlertAsync(Animal animal, string type, string severity, string message)
        {
            var hasSimilar = await _alertRepository.HasSimilarAlertAsync(animal.Id, type, 24);
            if (hasSimilar) return;

            var alert = new Alert
            {
                Type = type,
                Severity = severity,
                Message = message,
                AnimalId = animal.Id,
                CreatedAt = DateTime.UtcNow
            };

            await _alertRepository.AddAsync(alert);

            var alertDto = new AlertDto
            {
                Id = alert.Id,
                Type = alert.Type,
                Title = GetAlertTitle(alert.Type, alert.Severity),
                Severity = alert.Severity,
                Message = alert.Message,
                AnimalId = alert.AnimalId,
                FarmId = animal.FarmId,
                AnimalName = animal.Name,
                IsRead = alert.IsRead,
                IsResolved = alert.IsResolved,
                CreatedAt = alert.CreatedAt,
                ResolvedAt = alert.ResolvedAt
            };

            await _hubContext.Clients.Group($"farm_{animal.FarmId}")
                .SendAsync("NewAlert", alertDto);
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

