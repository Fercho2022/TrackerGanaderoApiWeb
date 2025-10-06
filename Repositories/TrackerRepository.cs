using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Repositories
{
    public class TrackerRepository : ITrackerRepository
    {
        private readonly CattleTrackingContext _context;

        public TrackerRepository(CattleTrackingContext context)
        {
            _context = context;
        }

        public async Task<Tracker?> GetByIdAsync(int id)
        {
            return await _context.Trackers.FindAsync(id);
        }

        public async Task<IEnumerable<Tracker>> GetAllAsync()
        {
            return await _context.Trackers.ToListAsync();
        }

        public async Task<Tracker> AddAsync(Tracker tracker)
        {
            _context.Trackers.Add(tracker);
            await _context.SaveChangesAsync();
            return tracker;
        }

        public async Task UpdateAsync(Tracker tracker)
        {
            _context.Trackers.Update(tracker);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(Tracker tracker)
        {
            _context.Trackers.Remove(tracker);
            await _context.SaveChangesAsync();
        }

        public async Task<Tracker?> GetByDeviceIdAsync(string deviceId)
        {
            return await _context.Trackers
                .FirstOrDefaultAsync(t => t.DeviceId == deviceId);
        }

        public async Task<IEnumerable<Tracker>> GetActiveTrackersAsync()
        {
            return await _context.Trackers
                .Where(t => t.IsActive)
                .Include(t => t.Animal)
                .ToListAsync();
        }

        public async Task<IEnumerable<Tracker>> GetTrackersWithLowBatteryAsync(int threshold = 20)
        {
            return await _context.Trackers
                .Where(t => t.IsActive && t.BatteryLevel <= threshold)
                .Include(t => t.Animal)
                .ToListAsync();
        }

        public async Task<Tracker?> GetTrackerWithAnimalAsync(string deviceId)
        {
            return await _context.Trackers
                .Where(t => t.DeviceId == deviceId)
                .Include(t => t.Animal)
                .ThenInclude(a => a!.Farm)
                .FirstOrDefaultAsync();
        }

        public async Task<bool> ExistsAsync(string deviceId)
        {
            return await _context.Trackers.AnyAsync(t => t.DeviceId == deviceId);
        }
    }
}
