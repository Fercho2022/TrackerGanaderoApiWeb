using System.ComponentModel.DataAnnotations;

namespace ApiWebTrackerGanado.Models
{
    public class HealthRecord
    {
        public int Id { get; set; }

        public int AnimalId { get; set; }
        public Animal Animal { get; set; } = null!;

        [StringLength(100)]
        public string Treatment { get; set; } = string.Empty;

        [StringLength(100)]
        public string? Medication { get; set; }

        [StringLength(100)]
        public string? Veterinarian { get; set; }

        [StringLength(500)]
        public string? Notes { get; set; }

        public DateTime TreatmentDate { get; set; }
        public DateTime? NextCheckup { get; set; }

        public decimal? Cost { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
