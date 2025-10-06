using ApiWebTrackerGanado.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Reflection.Emit;

namespace ApiWebTrackerGanado.Data
{
    public class CattleTrackingContext : DbContext
    {
        public CattleTrackingContext(DbContextOptions<CattleTrackingContext> options) : base(options) { }

        public DbSet<User> Users { get; set; }
        public DbSet<Farm> Farms { get; set; }
        public DbSet<Animal> Animals { get; set; }
        public DbSet<Tracker> Trackers { get; set; }
        public DbSet<LocationHistory> LocationHistories { get; set; }
        public DbSet<Pasture> Pastures { get; set; }
        public DbSet<PastureUsage> PastureUsages { get; set; }
        public DbSet<Alert> Alerts { get; set; }
        public DbSet<HealthRecord> HealthRecords { get; set; }
        public DbSet<WeightRecord> WeightRecords { get; set; }
        public DbSet<BreedingRecord> BreedingRecords { get; set; }
        public DbSet<Transaction> Transactions { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // User Configuration
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.Email).IsUnique();
                entity.Property(e => e.Email).IsRequired();
                entity.Property(e => e.PasswordHash).IsRequired();
            });

            // Farm Configuration
            modelBuilder.Entity<Farm>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.User)
                      .WithMany(e => e.Farms)
                      .HasForeignKey(e => e.UserId);
                // Temporarily disabled for testing
                // entity.Property(e => e.Boundaries).HasColumnType("geometry");
            });

            // Animal Configuration
            modelBuilder.Entity<Animal>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Farm)
                      .WithMany(e => e.Animals)
                      .HasForeignKey(e => e.FarmId);
                entity.HasOne(e => e.Tracker)
                      .WithOne(e => e.Animal)
                      .HasForeignKey<Animal>(e => e.TrackerId)
                      .IsRequired(false);
                entity.Property(e => e.Weight).HasPrecision(10, 2);
            });

            // Tracker Configuration
            modelBuilder.Entity<Tracker>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasIndex(e => e.DeviceId).IsUnique();
            });

            // LocationHistory Configuration
            modelBuilder.Entity<LocationHistory>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany(e => e.LocationHistories)
                      .HasForeignKey(e => e.AnimalId);
                entity.HasOne(e => e.Tracker)
                      .WithMany(e => e.LocationHistories)
                      .HasForeignKey(e => e.TrackerId);
                // Temporarily disabled for PostGIS migration
                // entity.Property(e => e.Location).HasColumnType("geometry");
                entity.HasIndex(e => e.Timestamp);
            });

            // Pasture Configuration
            modelBuilder.Entity<Pasture>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Farm)
                      .WithMany(e => e.Pastures)
                      .HasForeignKey(e => e.FarmId);
                entity.Property(e => e.Area).HasColumnType("geometry");
                entity.Property(e => e.AreaSize).HasPrecision(10, 2);
            });

            // PastureUsage Configuration
            modelBuilder.Entity<PastureUsage>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Pasture)
                      .WithMany(e => e.PastureUsages)
                      .HasForeignKey(e => e.PastureId);
                entity.HasOne(e => e.Animal)
                      .WithMany()
                      .HasForeignKey(e => e.AnimalId);
            });

            // Alert Configuration
            modelBuilder.Entity<Alert>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany(e => e.Alerts)
                      .HasForeignKey(e => e.AnimalId);
                entity.HasIndex(e => e.CreatedAt);
            });

            // HealthRecord Configuration
            modelBuilder.Entity<HealthRecord>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany(e => e.HealthRecords)
                      .HasForeignKey(e => e.AnimalId);
                entity.Property(e => e.Cost).HasPrecision(10, 2);
            });

            // WeightRecord Configuration
            modelBuilder.Entity<WeightRecord>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany(e => e.WeightRecords)
                      .HasForeignKey(e => e.AnimalId);
                entity.Property(e => e.Weight).HasPrecision(10, 2);
            });

            // BreedingRecord Configuration
            modelBuilder.Entity<BreedingRecord>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany(e => e.BreedingRecords)
                      .HasForeignKey(e => e.AnimalId);
            });

            // Transaction Configuration
            modelBuilder.Entity<Transaction>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.HasOne(e => e.Animal)
                      .WithMany()
                      .HasForeignKey(e => e.AnimalId);
                entity.Property(e => e.Amount).HasPrecision(12, 2);
            });
        }
    }
}

