using System.ComponentModel.DataAnnotations;

namespace ApiWebTrackerGanado.Models
{
    public class Tracker
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string DeviceId { get; set; } = string.Empty;

        [StringLength(50)]
        public string Model { get; set; } = string.Empty;

        public int BatteryLevel { get; set; }

        public bool IsActive { get; set; } = true;

        public DateTime LastSeen { get; set; }

        public Animal? Animal { get; set; }

        public ICollection<LocationHistory> LocationHistories { get; set; } = new List<LocationHistory>();

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
