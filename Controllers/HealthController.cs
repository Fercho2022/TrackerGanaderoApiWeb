using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using AutoMapper;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HealthController : ControllerBase
    {
        private readonly IHealthRecordRepository _healthRecordRepository;
        private readonly IMapper _mapper;

        public HealthController(IHealthRecordRepository healthRecordRepository, IMapper mapper)
        {
            _healthRecordRepository = healthRecordRepository;
            _mapper = mapper;
        }

        [HttpGet("animal/{animalId}")]
        public async Task<ActionResult<IEnumerable<HealthRecordDto>>> GetAnimalHealthRecords(int animalId)
        {
            var healthRecords = await _healthRecordRepository.GetAnimalHealthRecordsAsync(animalId);
            var healthRecordDtos = _mapper.Map<List<HealthRecordDto>>(healthRecords);
            return Ok(healthRecordDtos);
        }

        [HttpPost]
        public async Task<ActionResult<HealthRecordDto>> CreateHealthRecord([FromBody] CreateHealthRecordDto createHealthRecordDto)
        {
            var healthRecord = _mapper.Map<HealthRecord>(createHealthRecordDto);
            healthRecord.CreatedAt = DateTime.UtcNow;

            await _healthRecordRepository.AddAsync(healthRecord);

            var healthRecordDto = _mapper.Map<HealthRecordDto>(healthRecord);
            return CreatedAtAction(nameof(GetAnimalHealthRecords), new { animalId = healthRecord.AnimalId }, healthRecordDto);
        }

        [HttpGet("farm/{farmId}/upcoming-checkups")]
        public async Task<ActionResult<IEnumerable<HealthRecordDto>>> GetUpcomingCheckups(int farmId, [FromQuery] int daysAhead = 30)
        {
            var upcomingCheckups = await _healthRecordRepository.GetUpcomingCheckupsAsync(farmId, daysAhead);
            var healthRecordDtos = _mapper.Map<List<HealthRecordDto>>(upcomingCheckups);
            return Ok(healthRecordDtos);
        }

        [HttpGet("farm/{farmId}/costs")]
        public async Task<ActionResult<decimal>> GetHealthCosts(int farmId, [FromQuery] DateTime from, [FromQuery] DateTime to)
        {
            var totalCosts = await _healthRecordRepository.GetHealthCostsByFarmAsync(farmId, from, to);
            return Ok(totalCosts);
        }
    }
}
