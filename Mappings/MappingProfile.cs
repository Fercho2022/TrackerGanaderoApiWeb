using ApiWebTrackerGanado.Dtos;
using ApiWebTrackerGanado.Helpers;
using ApiWebTrackerGanado.Models;
using AutoMapper;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace ApiWebTrackerGanado.Mappings
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            // Animal mappings
            CreateMap<Animal, AnimalDto>()
                .ForMember(dest => dest.CurrentLocation, opt => opt.Ignore());

            CreateMap<CreateAnimalDto, Animal>()
                .ForMember(dest => dest.Id, opt => opt.Ignore())
                .ForMember(dest => dest.CreatedAt, opt => opt.MapFrom(src => DateTime.UtcNow))
                .ForMember(dest => dest.UpdatedAt, opt => opt.MapFrom(src => DateTime.UtcNow));

            CreateMap<UpdateAnimalDto, Animal>()
                .ForMember(dest => dest.Id, opt => opt.Ignore())
                .ForMember(dest => dest.FarmId, opt => opt.Ignore())
                .ForMember(dest => dest.CreatedAt, opt => opt.Ignore())
                .ForMember(dest => dest.UpdatedAt, opt => opt.MapFrom(src => DateTime.UtcNow));

            // Health records mappings
            CreateMap<HealthRecord, HealthRecordDto>();
            CreateMap<CreateHealthRecordDto, HealthRecord>()
                .ForMember(dest => dest.Id, opt => opt.Ignore())
                .ForMember(dest => dest.CreatedAt, opt => opt.MapFrom(src => DateTime.UtcNow));

            // Alert mappings
            CreateMap<Alert, AlertDto>()
                .ForMember(dest => dest.AnimalName, opt => opt.MapFrom(src => src.Animal.Name));

            // Farm mappings with geometry conversion
            CreateMap<Farm, FarmDto>()
                .ForMember(dest => dest.BoundaryCoordinates, opt => opt.MapFrom(src =>
                    src.Boundaries != null ? GeometryHelper.ConvertPolygonToLatLng(src.Boundaries) : null));

            CreateMap<CreateFarmDto, Farm>()
                .ForMember(dest => dest.Boundaries, opt => opt.MapFrom(src =>
                    src.BoundaryCoordinates != null && src.BoundaryCoordinates.Any() ?
                    GeometryHelper.CreatePolygonFromGoogleMapsCoordinates(src.BoundaryCoordinates) : null))
                .ForMember(dest => dest.CreatedAt, opt => opt.MapFrom(src => DateTime.UtcNow))
                .ForMember(dest => dest.Id, opt => opt.Ignore())
                .ForMember(dest => dest.UserId, opt => opt.Ignore());
        }
    }
}