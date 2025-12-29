using ApiWebTrackerGanado.Data;
using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Models;
using AutoMapper;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize]
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
            try
            {
                // Log incoming data
                Console.WriteLine($"[CreateAnimal] Received data: Name={createAnimalDto.Name}, FarmId={createAnimalDto.FarmId}, Gender={createAnimalDto.Gender}, Breed={createAnimalDto.Breed}, Status={createAnimalDto.Status}, Weight={createAnimalDto.Weight}");

                // Check if farm exists
                var farmExists = await _context.Farms.AnyAsync(f => f.Id == createAnimalDto.FarmId);
                Console.WriteLine($"[CreateAnimal] Farm ID {createAnimalDto.FarmId} exists: {farmExists}");

                if (!farmExists)
                {
                    Console.WriteLine($"[CreateAnimal] WARNING: Farm with ID {createAnimalDto.FarmId} does not exist, using default Farm ID 1");
                    // Instead of failing, let's try using a default farm ID
                    createAnimalDto.FarmId = 1;

                    // Check if default farm exists
                    var defaultFarmExists = await _context.Farms.AnyAsync(f => f.Id == 1);
                    if (!defaultFarmExists)
                    {
                        Console.WriteLine($"[CreateAnimal] ERROR: No farms exist in database");
                        return BadRequest("No farms available. Please create a farm first.");
                    }
                }

                // Create animal manually to avoid AutoMapper issues
                var animal = new Animal
                {
                    Name = createAnimalDto.Name?.Trim() ?? "Unknown",
                    Tag = createAnimalDto.Tag?.Trim(),
                    BirthDate = DateTime.SpecifyKind(createAnimalDto.BirthDate, DateTimeKind.Utc), // Ensure UTC
                    Gender = createAnimalDto.Gender?.Trim() ?? "Unknown",
                    Breed = createAnimalDto.Breed?.Trim() ?? "Unknown",
                    Weight = createAnimalDto.Weight > 0 ? createAnimalDto.Weight : 100, // Default weight
                    Status = !string.IsNullOrEmpty(createAnimalDto.Status) ? createAnimalDto.Status.Trim() : "Active",
                    FarmId = createAnimalDto.FarmId,
                    TrackerId = null, // Don't assign tracker initially
                    CustomerTrackerId = null, // Don't assign customer tracker initially
                    CreatedAt = DateTime.SpecifyKind(DateTime.UtcNow, DateTimeKind.Utc),
                    UpdatedAt = DateTime.SpecifyKind(DateTime.UtcNow, DateTimeKind.Utc)
                };

                Console.WriteLine($"[CreateAnimal] Mapped animal: Name={animal.Name}, FarmId={animal.FarmId}, Gender={animal.Gender}, Breed={animal.Breed}, Status={animal.Status}, Weight={animal.Weight}");

                _context.Animals.Add(animal);
                await _context.SaveChangesAsync();

                Console.WriteLine($"[CreateAnimal] SUCCESS: Animal created with ID {animal.Id}");

                var animalDto = _mapper.Map<AnimalDto>(animal);
                return CreatedAtAction(nameof(GetAnimal), new { id = animal.Id }, animalDto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[CreateAnimal] ERROR: {ex.Message}");
                Console.WriteLine($"[CreateAnimal] Stack trace: {ex.StackTrace}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"[CreateAnimal] Inner exception: {ex.InnerException.Message}");
                }
                throw; // Re-throw to let the error handling middleware handle it
            }
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

