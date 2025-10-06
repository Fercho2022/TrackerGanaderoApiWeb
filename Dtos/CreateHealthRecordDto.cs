using System.ComponentModel.DataAnnotations;

namespace ApiWebTrackerGanado.Dtos
{
    public class CreateHealthRecordDto
    {
        public int AnimalId { get; set; }
        [Required]
        public string Treatment { get; set; } = string.Empty;
        public string? Medication { get; set; }
        public string? Veterinarian { get; set; }
        public string? Notes { get; set; }
        public DateTime TreatmentDate { get; set; }
        public DateTime? NextCheckup { get; set; }
        public decimal? Cost { get; set; }
    }
}
