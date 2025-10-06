using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using Microsoft.AspNetCore.SignalR;
using NetTopologySuite.Geometries;
using NetTopologySuite;
using Microsoft.EntityFrameworkCore;
using ApiWebTrackerGanado.Hubs;
using ApiWebTrackerGanado.Helpers;

namespace ApiWebTrackerGanado.Services
{
    public class TrackingService : ITrackingService 
    {
        private readonly ITrackerRepository _trackerRepository;
        private readonly ILocationHistoryRepository _locationHistoryRepository;
        private readonly IAnimalRepository _animalRepository;
        private readonly IHubContext<LiveTrackingHub> _hubContext;
        private readonly IAlertService _alertService;

        public TrackingService(
            ITrackerRepository trackerRepository,
            ILocationHistoryRepository locationHistoryRepository,
            IAnimalRepository animalRepository,
            IHubContext<LiveTrackingHub> hubContext,
            IAlertService alertService)
        {
            _trackerRepository = trackerRepository;
            _locationHistoryRepository = locationHistoryRepository;
            _animalRepository = animalRepository;
            _hubContext = hubContext;
            _alertService = alertService;
        }

        public async Task ProcessTrackerDataAsync(TrackerDataDto trackerData)
        {
            var tracker = await _trackerRepository.GetTrackerWithAnimalAsync(trackerData.DeviceId);
            if (tracker?.Animal == null) return;

            // Update tracker status
            tracker.BatteryLevel = trackerData.BatteryLevel;
            tracker.LastSeen = trackerData.Timestamp.Kind == DateTimeKind.Utc
                ? trackerData.Timestamp
                : trackerData.Timestamp.ToUniversalTime();
            await _trackerRepository.UpdateAsync(tracker);

            // Create location history entry
            var location = GeometryHelper.CreatePoint(trackerData.Longitude, trackerData.Latitude);

            var locationHistory = new LocationHistory
            {
                AnimalId = tracker.Animal.Id,
                TrackerId = tracker.Id,
                // Location = location, // Temporarily disabled for PostGIS migration
                Latitude = trackerData.Latitude,
                Longitude = trackerData.Longitude,
                Altitude = trackerData.Altitude,
                Speed = trackerData.Speed,
                ActivityLevel = trackerData.ActivityLevel,
                Temperature = trackerData.Temperature,
                SignalStrength = trackerData.SignalStrength,
                Timestamp = trackerData.Timestamp.Kind == DateTimeKind.Utc
                    ? trackerData.Timestamp
                    : trackerData.Timestamp.ToUniversalTime()
            };

            await _locationHistoryRepository.AddAsync(locationHistory);

            // Check for alerts
            await _alertService.CheckLocationAlertsAsync(tracker.Animal, locationHistory);
            await _alertService.CheckActivityAlertsAsync(tracker.Animal, trackerData.ActivityLevel);

            // Send real-time update
            var locationDto = new LocationDto
            {
                Latitude = trackerData.Latitude,
                Longitude = trackerData.Longitude,
                Altitude = trackerData.Altitude,
                Speed = trackerData.Speed,
                ActivityLevel = trackerData.ActivityLevel,
                Temperature = trackerData.Temperature,
                Timestamp = trackerData.Timestamp
            };

            await _hubContext.Clients.Group($"animal_{tracker.Animal.Id}")
                .SendAsync("LocationUpdate", tracker.Animal.Id, locationDto);

            await _hubContext.Clients.Group($"farm_{tracker.Animal.FarmId}")
                .SendAsync("AnimalLocationUpdate", tracker.Animal.Id, locationDto);
        }

        public async Task<IEnumerable<LocationDto>> GetAnimalLocationHistoryAsync(int animalId, DateTime from, DateTime to)
        {
            var locations = await _locationHistoryRepository
                .GetAnimalLocationHistoryAsync(animalId, from, to);

            return locations.Select(lh => new LocationDto
            {
                Latitude = lh.Latitude,
                Longitude = lh.Longitude,
                Altitude = lh.Altitude,
                Speed = lh.Speed,
                ActivityLevel = lh.ActivityLevel,
                Temperature = lh.Temperature,
                Timestamp = lh.Timestamp
            });
        }

        public async Task<LocationDto?> GetAnimalCurrentLocationAsync(int animalId)
        {
            var lastLocation = await _locationHistoryRepository.GetAnimalLastLocationAsync(animalId);

            if (lastLocation == null) return null;

            return new LocationDto
            {
                Latitude = lastLocation.Latitude,
                Longitude = lastLocation.Longitude,
                Altitude = lastLocation.Altitude,
                Speed = lastLocation.Speed,
                ActivityLevel = lastLocation.ActivityLevel,
                Temperature = lastLocation.Temperature,
                Timestamp = lastLocation.Timestamp
            };
        }

        public async Task<IEnumerable<AnimalDto>> GetAnimalsInAreaAsync(double lat1, double lng1, double lat2, double lng2)
        {
            var area = GeometryHelper.CreateRectangle(lng1, lat1, lng2, lat2);
            var animalsInArea = await _locationHistoryRepository.GetLocationsInAreaAsync(area, DateTime.UtcNow.AddHours(-1), DateTime.UtcNow);

            return animalsInArea
                .GroupBy(lh => lh.AnimalId)
                .Select(g => new AnimalDto
                {
                    Id = g.First().Animal.Id,
                    Name = g.First().Animal.Name,
                    Tag = g.First().Animal.Tag,
                    BirthDate = g.First().Animal.BirthDate,
                    Gender = g.First().Animal.Gender,
                    Breed = g.First().Animal.Breed,
                    Weight = g.First().Animal.Weight,
                    Status = g.First().Animal.Status,
                    FarmId = g.First().Animal.FarmId,
                    TrackerId = g.First().Animal.TrackerId
                });
        }

        public async Task<IEnumerable<object>> GetFarmAnimalsLocationsAsync(int farmId)
        {
            var animals = await _animalRepository.GetAnimalsWithTrackersAsync(farmId);
            var result = new List<object>();

            foreach (var animal in animals)
            {
                var currentLocation = await GetAnimalCurrentLocationAsync(animal.Id);

                result.Add(new
                {
                    animal.Id,
                    animal.Name,
                    animal.Tag,
                    animal.Status,
                    animal.FarmId,
                    animal.TrackerId,
                    CurrentLocation = currentLocation
                });
            }

            return result;
        }

        public async Task SaveLocationHistoryAsync(SaveLocationHistoryDto locationData)
        {
            // Verify that the animal and tracker exist
            var animal = await _animalRepository.GetByIdAsync(locationData.AnimalId);
            if (animal == null)
                throw new ArgumentException($"Animal with ID {locationData.AnimalId} not found");

            var tracker = await _trackerRepository.GetByIdAsync(locationData.TrackerId);
            if (tracker == null)
                throw new ArgumentException($"Tracker with ID {locationData.TrackerId} not found");

            // Create location history entry from frontend data
            var locationHistory = new LocationHistory
            {
                AnimalId = locationData.AnimalId,
                TrackerId = locationData.TrackerId,
                Latitude = locationData.Latitude,
                Longitude = locationData.Longitude,
                Altitude = locationData.Altitude,
                Speed = locationData.Speed,
                ActivityLevel = locationData.ActivityLevel,
                Temperature = locationData.Temperature,
                SignalStrength = locationData.SignalStrength,
                Timestamp = locationData.Timestamp.Kind == DateTimeKind.Utc
                    ? locationData.Timestamp
                    : locationData.Timestamp.ToUniversalTime()
            };

            await _locationHistoryRepository.AddAsync(locationHistory);

            // Check for alerts based on the new location
            await _alertService.CheckLocationAlertsAsync(animal, locationHistory);
            await _alertService.CheckActivityAlertsAsync(animal, locationData.ActivityLevel);

            // Send real-time update via SignalR
            var locationDto = new LocationDto
            {
                Latitude = locationData.Latitude,
                Longitude = locationData.Longitude,
                Altitude = locationData.Altitude,
                Speed = locationData.Speed,
                ActivityLevel = locationData.ActivityLevel,
                Temperature = locationData.Temperature,
                Timestamp = locationData.Timestamp
            };

            await _hubContext.Clients.Group($"animal_{locationData.AnimalId}")
                .SendAsync("LocationUpdate", locationData.AnimalId, locationDto);

            await _hubContext.Clients.Group($"farm_{animal.FarmId}")
                .SendAsync("AnimalLocationUpdate", locationData.AnimalId, locationDto);
        }
    }
}
