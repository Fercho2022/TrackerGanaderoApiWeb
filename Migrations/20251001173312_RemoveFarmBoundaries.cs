using Microsoft.EntityFrameworkCore.Migrations;
using NetTopologySuite.Geometries;

#nullable disable

namespace ApiWebTrackerGanado.Migrations
{
    /// <inheritdoc />
    public partial class RemoveFarmBoundaries : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Boundaries",
                table: "Farms");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<Polygon>(
                name: "Boundaries",
                table: "Farms",
                type: "geometry",
                nullable: true);
        }
    }
}
