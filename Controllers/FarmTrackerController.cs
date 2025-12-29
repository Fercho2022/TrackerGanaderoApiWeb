using ApiWebTrackerGanado.Services;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FarmTrackerController : ControllerBase
    {
        private readonly FarmTrackerIntegrationService _farmTrackerService;
        private readonly ILogger<FarmTrackerController> _logger;

        public FarmTrackerController(
            FarmTrackerIntegrationService farmTrackerService,
            ILogger<FarmTrackerController> logger)
        {
            _farmTrackerService = farmTrackerService;
            _logger = logger;
        }

        /// <summary>
        /// Obtiene los trackers disponibles del usuario para asignar a granjas/animales
        /// </summary>
        [HttpGet("available")]
        public async Task<IActionResult> GetAvailableTrackers()
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var availableTrackers = await _farmTrackerService.GetAvailableTrackersForFarmsAsync(userId.Value);

                return Ok(new
                {
                    success = true,
                    trackers = availableTrackers,
                    count = availableTrackers.Count,
                    message = availableTrackers.Count > 0
                        ? $"Se encontraron {availableTrackers.Count} trackers disponibles para asignar"
                        : "No hay trackers disponibles. Primero asigne trackers desde la gestión de trackers."
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting available farm trackers");
                return BadRequest(new
                {
                    success = false,
                    message = "Error obteniendo trackers disponibles"
                });
            }
        }

        /// <summary>
        /// Asigna un CustomerTracker a un animal específico
        /// </summary>
        [HttpPost("assign-to-animal")]
        public async Task<IActionResult> AssignTrackerToAnimal([FromBody] AssignTrackerToAnimalRequest request)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var success = await _farmTrackerService.AssignTrackerToAnimalAsync(
                    request.CustomerTrackerId,
                    request.AnimalId,
                    userId.Value);

                if (!success)
                {
                    return BadRequest(new
                    {
                        success = false,
                        message = "No se pudo asignar el tracker al animal. Verifique que ambos le pertenezcan."
                    });
                }

                return Ok(new
                {
                    success = true,
                    message = "Tracker asignado al animal exitosamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error assigning tracker to animal");
                return BadRequest(new
                {
                    success = false,
                    message = "Error interno al asignar el tracker"
                });
            }
        }

        /// <summary>
        /// Desasigna un tracker de un animal
        /// </summary>
        [HttpPost("unassign-from-animal/{animalId}")]
        public async Task<IActionResult> UnassignTrackerFromAnimal(int animalId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var success = await _farmTrackerService.UnassignTrackerFromAnimalAsync(animalId, userId.Value);

                if (!success)
                {
                    return BadRequest(new
                    {
                        success = false,
                        message = "No se pudo desasignar el tracker del animal"
                    });
                }

                return Ok(new
                {
                    success = true,
                    message = "Tracker desasignado del animal exitosamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error unassigning tracker from animal {AnimalId}", animalId);
                return BadRequest(new
                {
                    success = false,
                    message = "Error interno al desasignar el tracker"
                });
            }
        }

        /// <summary>
        /// Obtiene información del tracker asignado a un animal
        /// </summary>
        [HttpGet("animal/{animalId}/tracker")]
        public async Task<IActionResult> GetAnimalTrackerInfo(int animalId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var trackerInfo = await _farmTrackerService.GetAnimalTrackerInfoAsync(animalId, userId.Value);

                if (trackerInfo == null)
                {
                    return Ok(new
                    {
                        success = true,
                        hasTracker = false,
                        message = "El animal no tiene tracker asignado"
                    });
                }

                return Ok(new
                {
                    success = true,
                    hasTracker = true,
                    tracker = trackerInfo
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting tracker info for animal {AnimalId}", animalId);
                return BadRequest(new
                {
                    success = false,
                    message = "Error obteniendo información del tracker"
                });
            }
        }

        /// <summary>
        /// Elimina un tracker específico de la base de datos
        /// </summary>
        [HttpDelete("delete-tracker/{trackerId}")]
        public async Task<IActionResult> DeleteTracker(int trackerId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    userId = 1; // Para desarrollo
                }

                _logger.LogInformation("DeleteTracker called with trackerId={TrackerId}, userId={UserId}", trackerId, userId.Value);

                var success = await _farmTrackerService.DeleteTrackerAsync(trackerId, userId.Value);

                if (!success)
                {
                    return BadRequest(new
                    {
                        success = false,
                        message = "No se pudo eliminar el tracker. Verifique que le pertenezca."
                    });
                }

                return Ok(new
                {
                    success = true,
                    message = "Tracker eliminado exitosamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting tracker {TrackerId}", trackerId);
                return BadRequest(new
                {
                    success = false,
                    message = "Error interno al eliminar el tracker"
                });
            }
        }

        /// <summary>
        /// Elimina todos los trackers de la base de datos
        /// </summary>
        [HttpDelete("delete-all-trackers")]
        public async Task<IActionResult> DeleteAllTrackers()
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    userId = 1; // Para desarrollo
                }

                var deletedCount = await _farmTrackerService.DeleteAllTrackersAsync(userId.Value);

                return Ok(new
                {
                    success = true,
                    deletedCount = deletedCount,
                    message = $"Se eliminaron {deletedCount} trackers exitosamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting all trackers");
                return BadRequest(new
                {
                    success = false,
                    message = "Error interno al eliminar todos los trackers"
                });
            }
        }

        /// <summary>
        /// Limpia trackers inactivos (sin transmisión en los últimos 2 minutos) de una granja
        /// </summary>
        [HttpPost("cleanup-inactive/{farmId}")]
        public async Task<IActionResult> CleanupInactiveTrackers(int farmId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var cleanedCount = await _farmTrackerService.CleanupInactiveTrackersFromFarmAsync(farmId, userId.Value);

                return Ok(new
                {
                    success = true,
                    cleanedCount = cleanedCount,
                    message = cleanedCount > 0
                        ? $"Se limpiaron {cleanedCount} trackers inactivos de la granja"
                        : "No se encontraron trackers inactivos para limpiar"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cleaning up inactive trackers from farm {FarmId}", farmId);
                return BadRequest(new
                {
                    success = false,
                    message = "Error limpiando trackers inactivos"
                });
            }
        }

        /// <summary>
        /// Endpoint de diagnóstico para verificar datos de tracker
        /// </summary>
        [HttpGet("debug-tracker/{trackerId}")]
        public async Task<IActionResult> DebugTracker(int trackerId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    userId = 1; // Para desarrollo
                }

                var debugInfo = await _farmTrackerService.GetTrackerDebugInfoAsync(trackerId, userId.Value);

                return Ok(debugInfo);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting debug info for tracker {TrackerId}", trackerId);
                return BadRequest(new
                {
                    success = false,
                    message = "Error obteniendo información de debug"
                });
            }
        }

        private int? GetCurrentUserId()
        {
            var userIdClaim = HttpContext.User.FindFirst("sub")?.Value ??
                             HttpContext.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

            return int.TryParse(userIdClaim, out var userId) ? userId : null;
        }
    }

    /// <summary>
    /// Request para asignar tracker a animal
    /// </summary>
    public class AssignTrackerToAnimalRequest
    {
        public int CustomerTrackerId { get; set; }
        public int AnimalId { get; set; }
    }
}