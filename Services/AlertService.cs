using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
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
            // TODO: Re-implement PostGIS-based alerts when Location property is restored
            // Temporarily disabled to resolve NullReferenceException during PostGIS migration

            /*
            // Check if animal is outside farm boundaries
            var farm = await _farmRepository.GetFarmWithBoundariesAsync(animal.FarmId);

            if (farm?.Boundaries != null && !farm.Boundaries.Contains(location.Location))
            {
                await CreateAlertAsync(animal, "OutOfBounds", "High",
                    $"{animal.Name} has left the farm boundaries");
            }

            // Check immobility
            var recentLocations = await _locationHistoryRepository
                .GetRecentLocationsAsync(animal.Id, 2);

            if (recentLocations.Count() >= 20)
            {
                var locations = recentLocations.ToList();
                var maxDistance = 0.0;
                var centerPoint = locations.First().Location;

                foreach (var loc in locations)
                {
                    var distance = centerPoint.Distance(loc.Location);
                    if (distance > maxDistance)
                        maxDistance = distance;
                }

                if (maxDistance < 0.0001)
                {
                    await CreateAlertAsync(animal, "Immobility", "Medium",
                        $"{animal.Name} has been immobile for over 2 hours");
                }
            }
            */
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
                Severity = a.Severity,
                Message = a.Message,
                AnimalId = a.AnimalId,
                AnimalName = a.Animal.Name,
                IsRead = a.IsRead,
                IsResolved = a.IsResolved,
                CreatedAt = a.CreatedAt
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
                Severity = alert.Severity,
                Message = alert.Message,
                AnimalId = alert.AnimalId,
                AnimalName = animal.Name,
                IsRead = alert.IsRead,
                IsResolved = alert.IsResolved,
                CreatedAt = alert.CreatedAt
            };

            await _hubContext.Clients.Group($"farm_{animal.FarmId}")
                .SendAsync("NewAlert", alertDto);
        }
    }
}

