using Microsoft.EntityFrameworkCore.Migrations;
using NetTopologySuite.Geometries;

#nullable disable

namespace ApiWebTrackerGanado.Migrations
{
    /// <inheritdoc />
    public partial class AddGeometryColumns : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<Polygon>(
                name: "Area",
                table: "Pastures",
                type: "geometry",
                nullable: false);

            migrationBuilder.AddColumn<Point>(
                name: "Location",
                table: "LocationHistories",
                type: "geometry",
                nullable: false);

            migrationBuilder.AddColumn<Polygon>(
                name: "Boundaries",
                table: "Farms",
                type: "geometry",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Area",
                table: "Pastures");

            migrationBuilder.DropColumn(
                name: "Location",
                table: "LocationHistories");

            migrationBuilder.DropColumn(
                name: "Boundaries",
                table: "Farms");
        }
    }
}
