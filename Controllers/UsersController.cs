using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Interfaces;
using ApiWebTrackerGanado.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Security.Cryptography;
using System.Text;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.IdentityModel.Tokens;

namespace ApiWebTrackerGanado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        private readonly IUserRepository _userRepository;
        private readonly IConfiguration _configuration;

        public UsersController(IUserRepository userRepository, IConfiguration configuration)
        {
            _userRepository = userRepository;
            _configuration = configuration;
        }

        [HttpGet]
        
        public async Task<ActionResult<IEnumerable<object>>> GetUsers()
        {
            var users = await _userRepository.GetAllAsync();
            var userDtos = users.Select(u => new
            {
                u.Id,
                u.Name,
                u.Email,
                u.Role,
                u.IsActive,
                u.CreatedAt
            });

            return Ok(userDtos);
        }

        [HttpGet("{id}")]
        
        public async Task<ActionResult<object>> GetUser(int id)
        {
            var user = await _userRepository.GetUserWithFarmsAsync(id);
            if (user == null) return NotFound();

            var userDto = new
            {
                user.Id,
                user.Name,
                user.Email,
                user.Role,
                user.IsActive,
                user.CreatedAt,
                FarmsCount = user.Farms.Count,
                Farms = user.Farms.Select(f => new { f.Id, f.Name })
            };

            return Ok(userDto);
        }

        [HttpGet("test-connection")]
        
        public async Task<ActionResult<object>> TestConnection()
        {
            try
            {
                var users = await _userRepository.GetAllAsync();
                return Ok(new { Status = "Connection successful", UserCount = users.Count() });
            }
            catch (Exception ex)
            {
                return Ok(new { Status = "Connection failed", Error = ex.Message, StackTrace = ex.StackTrace });
            }
        }

        [HttpPost("register")]

        public async Task<ActionResult<object>> Register([FromBody] RegisterUserDto registerDto)
        {
            // Validate model state (includes password confirmation)
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            // Check if email already exists
            if (await _userRepository.EmailExistsAsync(registerDto.Email))
            {
                return BadRequest("Email already exists");
            }

            // Hash password
            var passwordHash = HashPassword(registerDto.Password);

            var user = new User
            {
                Name = registerDto.Name,
                Email = registerDto.Email,
                PasswordHash = passwordHash,
                Role = "User",
                IsActive = true,
                CreatedAt = DateTime.UtcNow
            };

            await _userRepository.AddAsync(user);

            var userDto = new
            {
                user.Id,
                user.Name,
                user.Email,
                user.Role,
                user.IsActive,
                user.CreatedAt
            };

            return CreatedAtAction(nameof(GetUser), new { id = user.Id }, userDto);
        }

        [HttpPost("login")]
        [AllowAnonymous]
        public async Task<ActionResult<AuthResponseDto>> Login([FromBody] LoginDto loginDto)
        {
            var user = await _userRepository.GetByUsernameAsync(loginDto.Username);
            if (user == null || !VerifyPassword(loginDto.Password, user.PasswordHash))
            {
                return Unauthorized("Invalid credentials");
            }

            if (!user.IsActive)
            {
                return Unauthorized("Account is inactive");
            }

            // Generate real JWT token
            var jwtToken = GenerateJwtToken(user);

            // Create the response in the format expected by Blazor MAUI
            var authResponse = new AuthResponseDto
            {
                Token = jwtToken,
                Expiration = DateTime.UtcNow.AddHours(24),
                User = new UserDto
                {
                    Id = user.Id,
                    Username = user.Name,
                    Email = user.Email,
                    FirstName = user.Name, // Using Name as FirstName for now
                    LastName = "",
                    PhoneNumber = null,
                    CreatedAt = user.CreatedAt,
                    UpdatedAt = user.CreatedAt
                }
            };

            return Ok(authResponse);
        }

        [HttpPut("{id}")]
        
        public async Task<IActionResult> UpdateUser(int id, [FromBody] UpdateUserDto updateDto)
        {
            var user = await _userRepository.GetByIdAsync(id);
            if (user == null) return NotFound();

            user.Name = updateDto.Name;
            user.Email = updateDto.Email;
            user.IsActive = updateDto.IsActive;

            if (!string.IsNullOrEmpty(updateDto.Password))
            {
                user.PasswordHash = HashPassword(updateDto.Password);
            }

            await _userRepository.UpdateAsync(user);
            return NoContent();
        }

        [HttpDelete("{id}")]
        
        public async Task<IActionResult> DeleteUser(int id)
        {
            var user = await _userRepository.GetByIdAsync(id);
            if (user == null) return NotFound();

            await _userRepository.DeleteAsync(user);
            return NoContent();
        }

        private static string HashPassword(string password)
        {
            using var sha256 = SHA256.Create();
            var hashedBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password + "your-salt-here"));
            return Convert.ToBase64String(hashedBytes);
        }

        private static bool VerifyPassword(string password, string hash)
        {
            return HashPassword(password) == hash;
        }

        private string GenerateJwtToken(User user)
        {
            var jwtSecret = _configuration["JWT:Secret"] ??
                throw new InvalidOperationException("JWT Secret is not configured");

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSecret));
            var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
                new Claim(JwtRegisteredClaimNames.Email, user.Email),
                new Claim("name", user.Name),
                new Claim("role", user.Role),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                new Claim(JwtRegisteredClaimNames.Iat,
                    new DateTimeOffset(DateTime.UtcNow).ToUnixTimeSeconds().ToString(),
                    ClaimValueTypes.Integer64)
            };

            var token = new JwtSecurityToken(
                claims: claims,
                expires: DateTime.UtcNow.AddHours(24),
                signingCredentials: credentials
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }
    }
}
