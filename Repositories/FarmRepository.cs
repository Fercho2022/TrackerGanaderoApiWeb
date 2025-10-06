using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Repositories
{
    public class FarmRepository : IFarmRepository
    {
        private readonly CattleTrackingContext _context;

        public FarmRepository(CattleTrackingContext context)
        {
            _context = context;
        }

        public async Task<Farm?> GetByIdAsync(int id)
        {
            return await _context.Farms.FindAsync(id);
        }

        public async Task<IEnumerable<Farm>> GetAllAsync()
        {
            return await _context.Farms.ToListAsync();
        }

        public async Task<Farm> AddAsync(Farm farm)
        {
            _context.Farms.Add(farm);
            await _context.SaveChangesAsync();
            return farm;
        }

        public async Task UpdateAsync(Farm farm)
        {
            _context.Farms.Update(farm);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(Farm farm)
        {
            _context.Farms.Remove(farm);
            await _context.SaveChangesAsync();
        }

        public async Task<IEnumerable<Farm>> GetFarmsByUserAsync(int userId)
        {
            return await _context.Farms
                .Where(f => f.UserId == userId)
                .ToListAsync();
        }

        public async Task<Farm?> GetFarmWithAnimalsAsync(int id)
        {
            return await _context.Farms
                .Where(f => f.Id == id)
                .Include(f => f.Animals)
                .ThenInclude(a => a.Tracker)
                .FirstOrDefaultAsync();
        }

        public async Task<Farm?> GetFarmWithPasturesAsync(int id)
        {
            return await _context.Farms
                .Where(f => f.Id == id)
                .Include(f => f.Pastures)
                .FirstOrDefaultAsync();
        }

        public async Task<Farm?> GetFarmWithBoundariesAsync(int id)
        {
            return await _context.Farms
                .Where(f => f.Id == id)
                .FirstOrDefaultAsync();
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.Farms.AnyAsync(f => f.Id == id);
        }
    }
}
