using ApiWebTrackerGanado.Services;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TrackerManagementController : ControllerBase
    {
        private readonly TrackerDiscoveryService _trackerDiscoveryService;
        private readonly LicenseService _licenseService;
        private readonly ILogger<TrackerManagementController> _logger;

        public TrackerManagementController(
            TrackerDiscoveryService trackerDiscoveryService,
            LicenseService licenseService,
            ILogger<TrackerManagementController> logger)
        {
            _trackerDiscoveryService = trackerDiscoveryService;
            _licenseService = licenseService;
            _logger = logger;
        }

        /// <summary>
        /// Obtiene todos los trackers disponibles para asignación
        /// </summary>
        [HttpGet("available")]
        public async Task<IActionResult> GetAvailableTrackers()
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                    return Unauthorized("Usuario no autenticado");

                var customer = await _licenseService.GetCurrentCustomerAsync(userId.Value);
                if (customer == null)
                {
                    return Ok(new {
                        success = false,
                        message = "Active una licencia para ver trackers disponibles",
                        trackers = new List<object>()
                    });
                }

                var availableTrackers = await _trackerDiscoveryService.GetAvailableTrackersAsync();

                return Ok(new {
                    success = true,
                    trackers = availableTrackers.Select(t => new {
                        id = t.Id,
                        deviceId = t.DeviceId,
                        name = t.Name,
                        model = t.Model,
                        manufacturer = t.Manufacturer,
                        serialNumber = t.SerialNumber,
                        firmwareVersion = t.FirmwareVersion,
                        batteryLevel = t.BatteryLevel,
                        lastSeen = t.LastSeen,
                        isOnline = t.IsOnline,
                        status = t.Status
                    }),
                    canAddMore = customer.CanAddMoreTrackers(),
                    currentCount = customer.CustomerTrackers.Count(ct => ct.Status == "Active"),
                    maxTrackers = customer.TrackerLimit
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving available trackers");
                return BadRequest(new {
                    success = false,
                    message = "Error obteniendo trackers disponibles"
                });
            }
        }

        /// <summary>
        /// Obtiene los trackers asignados al cliente actual
        /// </summary>
        [HttpGet("my-trackers")]
        public async Task<IActionResult> GetMyTrackers()
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                    return Unauthorized("Usuario no autenticado");

                var customer = await _licenseService.GetCurrentCustomerAsync(userId.Value);
                if (customer == null)
                {
                    return Ok(new {
                        success = true,
                        trackers = new List<object>(),
                        message = "No hay licencia activa"
                    });
                }

                var customerTrackers = await _trackerDiscoveryService.GetCustomerTrackersAsync(customer.Id);

                return Ok(new {
                    success = true,
                    trackers = customerTrackers.Select(ct => new {
                        id = ct.Id,
                        trackerId = ct.TrackerId,
                        deviceId = ct.DeviceId,
                        trackerName = ct.TrackerName,
                        customName = ct.CustomName,
                        model = ct.Model,
                        batteryLevel = ct.BatteryLevel,
                        lastSeen = ct.LastSeen,
                        isOnline = ct.IsOnline,
                        assignedAt = ct.AssignedAt,
                        assignmentMethod = ct.AssignmentMethod,
                        licenseKey = ct.LicenseKey,
                        assignedByUser = ct.AssignedByUser,
                        notes = ct.Notes
                    }),
                    totalTrackers = customerTrackers.Count,
                    onlineTrackers = customerTrackers.Count(t => t.IsOnline),
                    trackerLimit = customer.TrackerLimit,
                    canAddMore = customer.CanAddMoreTrackers()
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving customer trackers");
                return BadRequest(new {
                    success = false,
                    message = "Error obteniendo trackers del cliente"
                });
            }
        }

        /// <summary>
        /// Asigna un tracker al cliente actual
        /// </summary>
        [HttpPost("assign")]
        public async Task<IActionResult> AssignTracker([FromBody] AssignTrackerRequest request)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                    return Unauthorized("Usuario no autenticado");

                var customer = await _licenseService.GetCurrentCustomerAsync(userId.Value);
                if (customer == null)
                {
                    return BadRequest(new {
                        success = false,
                        message = "No hay licencia activa. Active una licencia primero."
                    });
                }

                if (!customer.CanAddMoreTrackers())
                {
                    return BadRequest(new {
                        success = false,
                        message = $"Ha alcanzado el límite de {customer.TrackerLimit} trackers"
                    });
                }

                var success = await _trackerDiscoveryService.AssignTrackerToCustomerAsync(
                    request.TrackerId,
                    customer.Id,
                    userId.Value,
                    request.LicenseId,
                    request.CustomName,
                    request.Notes);

                if (!success)
                {
                    return BadRequest(new {
                        success = false,
                        message = "No se pudo asignar el tracker. Verifique que esté disponible."
                    });
                }

                return Ok(new {
                    success = true,
                    message = "Tracker asignado exitosamente",
                    trackerId = request.TrackerId
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error assigning tracker {TrackerId}", request.TrackerId);
                return BadRequest(new {
                    success = false,
                    message = "Error interno al asignar el tracker"
                });
            }
        }

        /// <summary>
        /// Desasigna un tracker del cliente actual
        /// </summary>
        [HttpPost("unassign/{customerTrackerId}")]
        public async Task<IActionResult> UnassignTracker(int customerTrackerId)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                    return Unauthorized("Usuario no autenticado");

                var success = await _trackerDiscoveryService.UnassignTrackerAsync(customerTrackerId, userId.Value);

                if (!success)
                {
                    return BadRequest(new {
                        success = false,
                        message = "No se pudo desasignar el tracker"
                    });
                }

                return Ok(new {
                    success = true,
                    message = "Tracker desasignado exitosamente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error unassigning tracker {CustomerTrackerId}", customerTrackerId);
                return BadRequest(new {
                    success = false,
                    message = "Error interno al desasignar el tracker"
                });
            }
        }

        /// <summary>
        /// Detecta trackers que están transmitiendo datos GPS activamente
        /// </summary>
        [HttpGet("detect-new")]
        public async Task<IActionResult> DetectNewTrackers()
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                    return Unauthorized("Usuario no autenticado");

                var customer = await _licenseService.GetCurrentCustomerAsync(userId.Value);
                if (customer == null)
                {
                    return Ok(new {
                        success = false,
                        message = "Active una licencia para detectar trackers",
                        newTrackers = new List<object>()
                    });
                }

                var newTrackers = await _trackerDiscoveryService.GetActiveTransmittingTrackersAsync();

                return Ok(new {
                    success = true,
                    newTrackers = newTrackers.Select(t => new {
                        id = t.Id,
                        deviceId = t.DeviceId,
                        name = t.Name,
                        model = t.Model,
                        manufacturer = t.Manufacturer,
                        serialNumber = t.SerialNumber,
                        batteryLevel = t.BatteryLevel,
                        lastSeen = t.LastSeen,
                        isOnline = t.IsOnline,
                        status = t.Status
                    }),
                    count = newTrackers.Count,
                    message = newTrackers.Count > 0
                        ? $"Se encontraron {newTrackers.Count} trackers transmitiendo datos GPS"
                        : "No se encontraron trackers transmitiendo datos GPS actualmente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting new trackers");
                return BadRequest(new {
                    success = false,
                    message = "Error detectando nuevos trackers"
                });
            }
        }

        /// <summary>
        /// Registra un tracker detectado automáticamente
        /// </summary>
        [HttpPost("register-detected")]
        public async Task<IActionResult> RegisterDetectedTracker([FromBody] RegisterTrackerRequest request)
        {
            try
            {
                var userId = GetCurrentUserId();
                if (userId == null)
                {
                    // Para desarrollo - usar usuario por defecto
                    userId = 1;
                }

                var customer = await _licenseService.GetCurrentCustomerAsync(userId.Value);
                if (customer == null)
                {
                    // Para desarrollo - crear customer automáticamente
                    try
                    {
                        customer = await _licenseService.CreateDevelopmentCustomerAsync(userId.Value);
                        if (customer == null)
                        {
                            return BadRequest(new {
                                success = false,
                                message = "No se pudo crear customer de desarrollo"
                            });
                        }
                    }
                    catch (Exception ex)
                    {
                        return BadRequest(new {
                            success = false,
                            message = $"Error creando customer: {ex.Message}"
                        });
                    }
                }

                var trackerId = await _trackerDiscoveryService.RegisterDetectedTrackerAsync(
                    request.DeviceId,
                    request.Model);

                if (trackerId == null)
                {
                    return BadRequest(new {
                        success = false,
                        message = "No se pudo registrar el tracker"
                    });
                }

                // Si auto_assign es true, asignarlo automáticamente al cliente
                if (request.AutoAssign && customer.CanAddMoreTrackers())
                {
                    await _trackerDiscoveryService.AssignTrackerToCustomerAsync(
                        trackerId.Value,
                        customer.Id,
                        userId.Value,
                        null,
                        request.CustomName,
                        "Asignación automática al detectar"
                    );

                    return Ok(new {
                        success = true,
                        message = "Tracker registrado y asignado automáticamente",
                        trackerId = trackerId.Value,
                        assigned = true
                    });
                }

                return Ok(new {
                    success = true,
                    message = "Tracker registrado exitosamente",
                    trackerId = trackerId.Value,
                    assigned = false
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error registering tracker {DeviceId}", request.DeviceId);
                return BadRequest(new {
                    success = false,
                    message = "Error registrando el tracker"
                });
            }
        }

        /// <summary>
        /// Endpoint público para detectar trackers transmitiendo (sin autenticación para testing)
        /// </summary>
        [HttpGet("detect-new-public")]
        public async Task<IActionResult> DetectNewTrackersPublic()
        {
            try
            {
                var activeTrackers = await _trackerDiscoveryService.GetActiveTransmittingTrackersAsync();

                return Ok(new {
                    success = true,
                    newTrackers = activeTrackers.Select(t => new {
                        id = t.Id,
                        deviceId = t.DeviceId,
                        name = t.Name,
                        model = t.Model,
                        manufacturer = t.Manufacturer,
                        serialNumber = t.SerialNumber,
                        batteryLevel = t.BatteryLevel,
                        lastSeen = t.LastSeen,
                        isOnline = t.IsOnline,
                        status = t.Status
                    }),
                    count = activeTrackers.Count,
                    message = activeTrackers.Count > 0
                        ? $"Se encontraron {activeTrackers.Count} trackers transmitiendo datos GPS"
                        : "No se encontraron trackers transmitiendo datos GPS actualmente"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error detecting new trackers (public)");
                return BadRequest(new {
                    success = false,
                    message = "Error detectando nuevos trackers"
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

    public class AssignTrackerRequest
    {
        public int TrackerId { get; set; }
        public int? LicenseId { get; set; }
        public string? CustomName { get; set; }
        public string? Notes { get; set; }
    }

    public class RegisterTrackerRequest
    {
        public string DeviceId { get; set; } = string.Empty;
        public string? Model { get; set; }
        public string? CustomName { get; set; }
        public bool AutoAssign { get; set; } = true;
    }
}