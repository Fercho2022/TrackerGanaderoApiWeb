using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiWebTrackerGanado.Migrations
{
    /// <inheritdoc />
    public partial class AddFarmBoundaryTable : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "FarmBoundaries",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", Npgsql.EntityFrameworkCore.PostgreSQL.Metadata.NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    FarmId = table.Column<int>(type: "integer", nullable: false),
                    Latitude = table.Column<decimal>(type: "numeric(10,8)", precision: 10, scale: 8, nullable: false),
                    Longitude = table.Column<decimal>(type: "numeric(11,8)", precision: 11, scale: 8, nullable: false),
                    SequenceOrder = table.Column<int>(type: "integer", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_FarmBoundaries", x => x.Id);
                    table.ForeignKey(
                        name: "FK_FarmBoundaries_Farms_FarmId",
                        column: x => x.FarmId,
                        principalTable: "Farms",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_FarmBoundaries_FarmId_SequenceOrder",
                table: "FarmBoundaries",
                columns: new[] { "FarmId", "SequenceOrder" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "FarmBoundaries");
        }
    }
}