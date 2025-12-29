using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Services
{
    /// <summary>
    /// Servicio para integrar la gestión de trackers de clientes con granjas y animales
    /// Conecta el flujo Customer -> CustomerTracker con Farm -> Animal -> Tracker
    /// </summary>
    public class FarmTrackerIntegrationService
    {
        private readonly CattleTrackingContext _context;
        private readonly ILogger<FarmTrackerIntegrationService> _logger;

        public FarmTrackerIntegrationService(
            CattleTrackingContext context,
            ILogger<FarmTrackerIntegrationService> logger)
        {
            _context = context;
            _logger = logger;
        }

        /// <summary>
        /// Obtiene todos los trackers disponibles para un usuario en sus granjas
        /// (sus CustomerTrackers que no están asignados a animales)
        /// </summary>
        public async Task<List<AvailableFarmTrackerDto>> GetAvailableTrackersForFarmsAsync(int userId)
        {
            try
            {
                // Buscar customer del usuario
                var customer = await _context.Customers
                    .FirstOrDefaultAsync(c => c.UserId == userId && c.Status == "Active");

                if (customer == null)
                {
                    _logger.LogInformation("No active customer found for user {UserId}", userId);
                    return new List<AvailableFarmTrackerDto>();
                }

                // Obtener CustomerTrackers activos que no están asignados a animales
                var availableTrackers = await _context.CustomerTrackers
                    .Include(ct => ct.Tracker)
                    .Where(ct => ct.CustomerId == customer.Id &&
                                ct.Status == "Active" &&
                                ct.AssignedAnimal == null)
                    .Select(ct => new AvailableFarmTrackerDto
                    {
                        CustomerTrackerId = ct.Id,
                        TrackerId = ct.TrackerId,
                        DeviceId = ct.Tracker.DeviceId,
                        TrackerName = ct.Tracker.Name ?? ct.Tracker.DeviceId,
                        CustomName = ct.CustomName,
                        Model = ct.Tracker.Model,
                        BatteryLevel = ct.Tracker.BatteryLevel,
                        LastSeen = ct.Tracker.LastSeen,
                        IsOnline = ct.Tracker.LastSeen > DateTime.UtcNow.AddMinutes(-5),
                        AssignedAt = ct.AssignedAt
                    })
                    .ToListAsync();

                _logger.LogInformation("Found {Count} available trackers for user {UserId}",
                    availableTrackers.Count, userId);

                return availableTrackers;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting available trackers for user {UserId}", userId);
                throw;
            }
        }

        /// <summary>
        /// Asigna un CustomerTracker a un animal específico
        /// </summary>
        public async Task<bool> AssignTrackerToAnimalAsync(int customerTrackerId, int animalId, int userId)
        {
            try
            {
                // Verificar que el CustomerTracker pertenece al usuario
                var customerTracker = await _context.CustomerTrackers
                    .Include(ct => ct.Customer)
                    .Include(ct => ct.Tracker)
                    .Include(ct => ct.AssignedAnimal)
                    .FirstOrDefaultAsync(ct => ct.Id == customerTrackerId);

                if (customerTracker == null)
                {
                    _logger.LogWarning("CustomerTracker {CustomerTrackerId} not found", customerTrackerId);
                    return false;
                }

                if (customerTracker.Customer.UserId != userId)
                {
                    _logger.LogWarning("CustomerTracker {CustomerTrackerId} does not belong to user {UserId}",
                        customerTrackerId, userId);
                    return false;
                }

                if (customerTracker.Status != "Active")
                {
                    _logger.LogWarning("CustomerTracker {CustomerTrackerId} is not active", customerTrackerId);
                    return false;
                }

                if (customerTracker.AssignedAnimal != null)
                {
                    _logger.LogWarning("CustomerTracker {CustomerTrackerId} is already assigned to animal {AnimalId}",
                        customerTrackerId, customerTracker.AssignedAnimal.Id);
                    return false;
                }

                // Verificar que el animal pertenece al usuario
                var animal = await _context.Animals
                    .Include(a => a.Farm)
                    .FirstOrDefaultAsync(a => a.Id == animalId);

                if (animal == null)
                {
                    _logger.LogWarning("Animal {AnimalId} not found", animalId);
                    return false;
                }

                if (animal.Farm.UserId != userId)
                {
                    _logger.LogWarning("Animal {AnimalId} does not belong to user {UserId}", animalId, userId);
                    return false;
                }

                // Si el animal ya tiene un tracker, desasignar el anterior
                if (animal.CustomerTrackerId.HasValue)
                {
                    await UnassignTrackerFromAnimalAsync(animal.Id, userId);
                }

                // Asignar el tracker al animal
                animal.TrackerId = customerTracker.TrackerId;
                animal.CustomerTrackerId = customerTrackerId;
                customerTracker.UpdatedAt = DateTime.UtcNow;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Successfully assigned CustomerTracker {CustomerTrackerId} to animal {AnimalId}",
                    customerTrackerId, animalId);

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error assigning CustomerTracker {CustomerTrackerId} to animal {AnimalId}",
                    customerTrackerId, animalId);
                throw;
            }
        }

        /// <summary>
        /// Desasigna un tracker de un animal
        /// </summary>
        public async Task<bool> UnassignTrackerFromAnimalAsync(int animalId, int userId)
        {
            try
            {
                var animal = await _context.Animals
                    .Include(a => a.Farm)
                    .Include(a => a.CustomerTracker)
                    .FirstOrDefaultAsync(a => a.Id == animalId);

                if (animal == null || animal.Farm.UserId != userId)
                {
                    _logger.LogWarning("Animal {AnimalId} not found or does not belong to user {UserId}",
                        animalId, userId);
                    return false;
                }

                if (animal.CustomerTrackerId.HasValue && animal.CustomerTracker != null)
                {
                    animal.CustomerTracker.UpdatedAt = DateTime.UtcNow;
                }

                // Desasignar tracker del animal
                animal.TrackerId = null;
                animal.CustomerTrackerId = null;

                await _context.SaveChangesAsync();

                _logger.LogInformation("Successfully unassigned tracker from animal {AnimalId}", animalId);

                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error unassigning tracker from animal {AnimalId}", animalId);
                throw;
            }
        }

        /// <summary>
        /// Limpia trackers inactivos (que no han transmitido en los últimos 2 minutos) de todos los animales de una granja
        /// </summary>
        public async Task<int> CleanupInactiveTrackersFromFarmAsync(int farmId, int userId)
        {
            try
            {
                _logger.LogInformation("Starting cleanup of inactive trackers for farm {FarmId}, user {UserId}", farmId, userId);

                // Verificar que la granja pertenece al usuario
                var farm = await _context.Farms
                    .FirstOrDefaultAsync(f => f.Id == farmId && f.UserId == userId);

                if (farm == null)
                {
                    _logger.LogWarning("Farm {FarmId} not found or does not belong to user {UserId}", farmId, userId);
                    return 0;
                }

                // Obtener todos los animales de la granja que tengan trackers asignados
                var animalsWithTrackers = await _context.Animals
                    .Include(a => a.CustomerTracker)
                        .ThenInclude(ct => ct!.Tracker)
                    .Where(a => a.FarmId == farmId && a.CustomerTrackerId.HasValue)
                    .ToListAsync();

                var cutoffTime = DateTime.UtcNow.AddMinutes(-2);
                var cleanedCount = 0;

                foreach (var animal in animalsWithTrackers)
                {
                    if (animal.CustomerTracker?.Tracker != null)
                    {
                        var tracker = animal.CustomerTracker.Tracker;

                        // Si el tracker no ha transmitido en los últimos 2 minutos, desasignarlo
                        if (tracker.LastSeen <= cutoffTime)
                        {
                            _logger.LogInformation("Removing inactive tracker {DeviceId} from animal {AnimalId} (last seen: {LastSeen})",
                                tracker.DeviceId, animal.Id, tracker.LastSeen);

                            animal.CustomerTrackerId = null;
                            animal.TrackerId = null;
                            cleanedCount++;
                        }
                    }
                }

                if (cleanedCount > 0)
                {
                    await _context.SaveChangesAsync();
                    _logger.LogInformation("Cleaned up {Count} inactive trackers from farm {FarmId}", cleanedCount, farmId);
                }
                else
                {
                    _logger.LogInformation("No inactive trackers found to clean up in farm {FarmId}", farmId);
                }

                return cleanedCount;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cleaning up inactive trackers from farm {FarmId}", farmId);
                throw;
            }
        }

        /// <summary>
        /// Obtiene información del tracker asignado a un animal
        /// </summary>
        public async Task<AnimalTrackerInfoDto?> GetAnimalTrackerInfoAsync(int animalId, int userId)
        {
            try
            {
                var animal = await _context.Animals
                    .Include(a => a.Farm)
                    .Include(a => a.CustomerTracker)
                        .ThenInclude(ct => ct!.Tracker)
                    .FirstOrDefaultAsync(a => a.Id == animalId);

                if (animal == null || animal.Farm.UserId != userId)
                {
                    return null;
                }

                if (animal.CustomerTracker == null || animal.CustomerTracker.Tracker == null)
                {
                    return null;
                }

                var tracker = animal.CustomerTracker.Tracker;

                return new AnimalTrackerInfoDto
                {
                    AnimalId = animalId,
                    CustomerTrackerId = animal.CustomerTrackerId.Value,
                    TrackerId = tracker.Id,
                    DeviceId = tracker.DeviceId,
                    TrackerName = tracker.Name ?? tracker.DeviceId,
                    CustomName = animal.CustomerTracker.CustomName,
                    Model = tracker.Model,
                    BatteryLevel = tracker.BatteryLevel,
                    LastSeen = tracker.LastSeen,
                    IsOnline = tracker.LastSeen > DateTime.UtcNow.AddMinutes(-5),
                    AssignedAt = animal.CustomerTracker.AssignedAt
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting tracker info for animal {AnimalId}", animalId);
                throw;
            }
        }

        /// <summary>
        /// Elimina un tracker específico de la base de datos - Versión simplificada como DeleteAllTrackers
        /// </summary>
        public async Task<bool> DeleteTrackerAsync(int trackerId, int userId)
        {
            try
            {
                _logger.LogInformation("Deleting tracker {TrackerId} for user {UserId}", trackerId, userId);

                using var transaction = await _context.Database.BeginTransactionAsync();

                try
                {
                    // Verificar que existe el tracker (usando SQL directo)
                    var trackerExists = await _context.Trackers
                        .Where(t => t.Id == trackerId)
                        .AnyAsync();

                    if (!trackerExists)
                    {
                        _logger.LogWarning("Tracker {TrackerId} not found in database", trackerId);
                        return false;
                    }

                    // Contar cuántos registros vamos a afectar antes de eliminar
                    var customerTrackersToDelete = await _context.CustomerTrackers
                        .Where(ct => ct.TrackerId == trackerId)
                        .CountAsync();

                    _logger.LogInformation("Found {Count} CustomerTracker records to delete for tracker {TrackerId}",
                        customerTrackersToDelete, trackerId);

                    // Desasignar de todos los animales que usan este tracker (SQL directo)
                    var affectedAnimals = await _context.Animals
                        .Where(a => a.TrackerId == trackerId)
                        .ExecuteUpdateAsync(a => a
                            .SetProperty(x => x.TrackerId, (int?)null)
                            .SetProperty(x => x.CustomerTrackerId, (int?)null));

                    _logger.LogInformation("Unassigned tracker from {Count} animals", affectedAnimals);

                    // Desasignar por CustomerTrackerId también
                    var affectedAnimalsByCustomerTracker = await _context.Database
                        .ExecuteSqlRawAsync(
                            "UPDATE \"Animals\" SET \"TrackerId\" = NULL, \"CustomerTrackerId\" = NULL " +
                            "WHERE \"CustomerTrackerId\" IN (SELECT \"Id\" FROM \"CustomerTrackers\" WHERE \"TrackerId\" = {0})",
                            trackerId);

                    _logger.LogInformation("Unassigned tracker by CustomerTracker from {Count} additional animals", affectedAnimalsByCustomerTracker);

                    // Eliminar CustomerTrackers usando SQL directo
                    var deletedCustomerTrackers = await _context.CustomerTrackers
                        .Where(ct => ct.TrackerId == trackerId)
                        .ExecuteDeleteAsync();

                    _logger.LogInformation("Removed {Count} CustomerTracker records", deletedCustomerTrackers);

                    // Eliminar el tracker usando SQL directo
                    var deletedTrackers = await _context.Trackers
                        .Where(t => t.Id == trackerId)
                        .ExecuteDeleteAsync();

                    _logger.LogInformation("Removed {Count} Tracker records", deletedTrackers);

                    await _context.SaveChangesAsync();
                    await transaction.CommitAsync();

                    _logger.LogInformation("Successfully deleted tracker {TrackerId}", trackerId);
                    return deletedTrackers > 0;
                }
                catch (Exception innerEx)
                {
                    _logger.LogError(innerEx, "Error in transaction while deleting tracker {TrackerId}: {Message}", trackerId, innerEx.Message);
                    await transaction.RollbackAsync();
                    throw;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting tracker {TrackerId}: {Message}", trackerId, ex.Message);
                return false;
            }
        }

        /// <summary>
        /// Obtiene información de debug para un tracker específico
        /// </summary>
        public async Task<object> GetTrackerDebugInfoAsync(int trackerId, int userId)
        {
            try
            {
                // Buscar customer del usuario
                var customer = await _context.Customers
                    .FirstOrDefaultAsync(c => c.UserId == userId && c.Status == "Active");

                // Buscar tracker SIN navegación
                var tracker = await _context.Trackers
                    .Where(t => t.Id == trackerId)
                    .Select(t => new { t.Id, t.DeviceId, t.Name, t.IsActive })
                    .FirstOrDefaultAsync();

                // Buscar customerTrackers para este usuario SIN navegación
                var customerTrackers = customer != null ?
                    (await _context.CustomerTrackers
                        .Where(ct => ct.CustomerId == customer.Id)
                        .Select(ct => new
                        {
                            Id = ct.Id,
                            TrackerId = ct.TrackerId,
                            CustomerId = ct.CustomerId,
                            Status = ct.Status
                        })
                        .ToListAsync()).Cast<object>().ToList() :
                    new List<object>();

                // Buscar customerTracker específico
                var specificCustomerTracker = customer != null ? await _context.CustomerTrackers
                    .Where(ct => ct.TrackerId == trackerId && ct.CustomerId == customer.Id)
                    .Select(ct => new
                    {
                        Id = ct.Id,
                        TrackerId = ct.TrackerId,
                        CustomerId = ct.CustomerId,
                        Status = ct.Status
                    })
                    .FirstOrDefaultAsync() : null;

                return new
                {
                    requestedTrackerId = trackerId,
                    userId = userId,
                    customer = customer != null ? new
                    {
                        id = customer.Id,
                        userId = customer.UserId,
                        status = customer.Status,
                        companyName = customer.CompanyName
                    } : null,
                    tracker = tracker != null ? new
                    {
                        id = tracker.Id,
                        deviceId = tracker.DeviceId,
                        name = tracker.Name,
                        isActive = tracker.IsActive
                    } : null,
                    customerTrackers = customerTrackers,
                    specificCustomerTracker = specificCustomerTracker,
                    allCustomers = await _context.Customers.Select(c => new
                    {
                        id = c.Id,
                        userId = c.UserId,
                        status = c.Status
                    }).ToListAsync()
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting debug info for tracker {TrackerId}", trackerId);
                throw;
            }
        }

        /// <summary>
        /// Elimina todos los trackers de la base de datos
        /// </summary>
        public async Task<int> DeleteAllTrackersAsync(int userId)
        {
            try
            {
                _logger.LogInformation("Deleting all trackers for user {UserId}", userId);

                using var transaction = await _context.Database.BeginTransactionAsync();

                try
                {
                    // Desasignar todos los trackers de animales
                    await _context.Animals
                        .ExecuteUpdateAsync(a => a
                            .SetProperty(x => x.TrackerId, (int?)null)
                            .SetProperty(x => x.CustomerTrackerId, (int?)null));

                    // Eliminar todos los CustomerTrackers
                    var customerTrackersCount = await _context.CustomerTrackers.CountAsync();
                    await _context.CustomerTrackers.ExecuteDeleteAsync();

                    // Eliminar todos los Trackers
                    var trackersCount = await _context.Trackers.CountAsync();
                    await _context.Trackers.ExecuteDeleteAsync();

                    await _context.SaveChangesAsync();
                    await transaction.CommitAsync();

                    _logger.LogInformation("Successfully deleted all {TrackerCount} trackers and {CustomerTrackerCount} customer tracker relationships",
                        trackersCount, customerTrackersCount);

                    return trackersCount;
                }
                catch
                {
                    await transaction.RollbackAsync();
                    throw;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting all trackers");
                throw;
            }
        }
    }

    /// <summary>
    /// DTO para trackers disponibles para asignación en granjas
    /// </summary>
    public class AvailableFarmTrackerDto
    {
        public int CustomerTrackerId { get; set; }
        public int TrackerId { get; set; }
        public string DeviceId { get; set; } = string.Empty;
        public string TrackerName { get; set; } = string.Empty;
        public string? CustomName { get; set; }
        public string Model { get; set; } = string.Empty;
        public int BatteryLevel { get; set; }
        public DateTime LastSeen { get; set; }
        public bool IsOnline { get; set; }
        public DateTime AssignedAt { get; set; }
    }

    /// <summary>
    /// DTO para información del tracker asignado a un animal
    /// </summary>
    public class AnimalTrackerInfoDto
    {
        public int AnimalId { get; set; }
        public int CustomerTrackerId { get; set; }
        public int TrackerId { get; set; }
        public string DeviceId { get; set; } = string.Empty;
        public string TrackerName { get; set; } = string.Empty;
        public string? CustomName { get; set; }
        public string Model { get; set; } = string.Empty;
        public int BatteryLevel { get; set; }
        public DateTime LastSeen { get; set; }
        public bool IsOnline { get; set; }
        public DateTime AssignedAt { get; set; }
    }
}