using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Models;
using AutoMapper;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AnimalsController : ControllerBase
    {
        private readonly CattleTrackingContext _context;
        private readonly IMapper _mapper;

        public AnimalsController(CattleTrackingContext context, IMapper mapper)
        {
            _context = context;
            _mapper = mapper;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<AnimalDto>>> GetAnimals([FromQuery] int? farmId)
        {
            var query = _context.Animals.AsQueryable();

            if (farmId.HasValue)
                query = query.Where(a => a.FarmId == farmId.Value);

            var animals = await query
                .Include(a => a.Tracker)
                .ToListAsync();

            var animalDtos = _mapper.Map<List<AnimalDto>>(animals);
            return Ok(animalDtos);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<AnimalDto>> GetAnimal(int id)
        {
            var animal = await _context.Animals
                .Include(a => a.Tracker)
                .Include(a => a.Farm)
                .FirstOrDefaultAsync(a => a.Id == id);

            if (animal == null)
                return NotFound();

            var animalDto = _mapper.Map<AnimalDto>(animal);
            return Ok(animalDto);
        }

        [HttpPost]
        public async Task<ActionResult<AnimalDto>> CreateAnimal([FromBody] CreateAnimalDto createAnimalDto)
        {
            var animal = _mapper.Map<Animal>(createAnimalDto);
            animal.CreatedAt = DateTime.UtcNow;
            animal.UpdatedAt = DateTime.UtcNow;

            _context.Animals.Add(animal);
            await _context.SaveChangesAsync();

            var animalDto = _mapper.Map<AnimalDto>(animal);
            return CreatedAtAction(nameof(GetAnimal), new { id = animal.Id }, animalDto);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateAnimal(int id, [FromBody] CreateAnimalDto updateAnimalDto)
        {
            var animal = await _context.Animals.FindAsync(id);
            if (animal == null)
                return NotFound();

            _mapper.Map(updateAnimalDto, animal);
            animal.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAnimal(int id)
        {
            var animal = await _context.Animals.FindAsync(id);
            if (animal == null)
                return NotFound();

            _context.Animals.Remove(animal);
            await _context.SaveChangesAsync();
            return NoContent();
        }

        [HttpGet("{id}/weight-history")]
        public async Task<ActionResult<IEnumerable<WeightRecord>>> GetAnimalWeightHistory(int id)
        {
            var weightRecords = await _context.WeightRecords
                .Where(wr => wr.AnimalId == id)
                .OrderByDescending(wr => wr.WeightDate)
                .ToListAsync();

            return Ok(weightRecords);
        }

        [HttpPost("{id}/weight")]
        public async Task<ActionResult<WeightRecord>> AddWeightRecord(int id, [FromBody] WeightRecord weightRecord)
        {
            weightRecord.AnimalId = id;
            weightRecord.CreatedAt = DateTime.UtcNow;

            _context.WeightRecords.Add(weightRecord);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetAnimalWeightHistory), new { id }, weightRecord);
        }
    }
}

