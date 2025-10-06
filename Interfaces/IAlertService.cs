using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Models;

namespace ApiWebTrackerGanado.Interfaces
{
    public interface IAlertService
    {
        Task CheckLocationAlertsAsync(Animal animal, LocationHistory location);
        Task CheckActivityAlertsAsync(Animal animal, int activityLevel);
        Task CheckBreedingAlertsAsync(Animal animal);
        Task<IEnumerable<AlertDto>> GetActiveAlertsAsync(int farmId);
        Task MarkAlertAsReadAsync(int alertId);
        Task ResolveAlertAsync(int alertId);
    }
}
