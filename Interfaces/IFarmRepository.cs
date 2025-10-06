using ApiWebTrackerGanado.Models;

namespace ApiWebTrackerGanado.Interfaces
{
    public interface IFarmRepository
    {
        Task<Farm?> GetByIdAsync(int id);
        Task<IEnumerable<Farm>> GetAllAsync();
        Task<Farm> AddAsync(Farm farm);
        Task UpdateAsync(Farm farm);
        Task DeleteAsync(Farm farm);
        Task<IEnumerable<Farm>> GetFarmsByUserAsync(int userId);
        Task<Farm?> GetFarmWithAnimalsAsync(int id);
        Task<Farm?> GetFarmWithPasturesAsync(int id);
        Task<Farm?> GetFarmWithBoundariesAsync(int id);
        Task<bool> ExistsAsync(int id);
    }
}
