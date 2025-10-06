using NetTopologySuite.Geometries;

namespace ApiWebTrackerGanado.Models
{
    public class LocationHistory
    {
        public int Id { get; set; }

        public int AnimalId { get; set; }
        public Animal Animal { get; set; } = null!;

        public int TrackerId { get; set; }
        public Tracker Tracker { get; set; } = null!;

        // Temporarily disabled for PostGIS migration
        [System.ComponentModel.DataAnnotations.Schema.NotMapped]
        public Point Location { get; set; } = null!;
        public double Latitude { get; set; }
        public double Longitude { get; set; }

        public double Altitude { get; set; }

        public double Speed { get; set; }

        public int ActivityLevel { get; set; }

        public double Temperature { get; set; }

        public int SignalStrength { get; set; }

        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }
}
