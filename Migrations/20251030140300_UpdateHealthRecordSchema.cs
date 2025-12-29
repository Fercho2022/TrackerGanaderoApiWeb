using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiWebTrackerGanado.Migrations
{
    /// <inheritdoc />
    public partial class UpdateHealthRecordSchema : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // Drop old columns that are being renamed/restructured
            migrationBuilder.DropColumn(
                name: "Treatment",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "TreatmentDate",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "Veterinarian",
                table: "HealthRecords");

            // Add new columns
            migrationBuilder.AddColumn<string>(
                name: "RecordType",
                table: "HealthRecords",
                type: "character varying(50)",
                maxLength: 50,
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "Description",
                table: "HealthRecords",
                type: "character varying(500)",
                maxLength: 500,
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<DateTime>(
                name: "RecordDate",
                table: "HealthRecords",
                type: "timestamp with time zone",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<string>(
                name: "VeterinarianName",
                table: "HealthRecords",
                type: "character varying(100)",
                maxLength: 100,
                nullable: true);

            // Modify existing Treatment column to be nullable with longer length
            migrationBuilder.AddColumn<string>(
                name: "Treatment",
                table: "HealthRecords",
                type: "character varying(500)",
                maxLength: 500,
                nullable: true);

            // Update Notes column length
            migrationBuilder.AlterColumn<string>(
                name: "Notes",
                table: "HealthRecords",
                type: "character varying(1000)",
                maxLength: 1000,
                nullable: true,
                oldClrType: typeof(string),
                oldType: "character varying(500)",
                oldMaxLength: 500,
                oldNullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // Remove new columns
            migrationBuilder.DropColumn(
                name: "RecordType",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "Description",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "RecordDate",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "VeterinarianName",
                table: "HealthRecords");

            migrationBuilder.DropColumn(
                name: "Treatment",
                table: "HealthRecords");

            // Restore old columns
            migrationBuilder.AddColumn<string>(
                name: "Treatment",
                table: "HealthRecords",
                type: "character varying(100)",
                maxLength: 100,
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<DateTime>(
                name: "TreatmentDate",
                table: "HealthRecords",
                type: "timestamp with time zone",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<string>(
                name: "Veterinarian",
                table: "HealthRecords",
                type: "character varying(100)",
                maxLength: 100,
                nullable: true);

            // Restore Notes original length
            migrationBuilder.AlterColumn<string>(
                name: "Notes",
                table: "HealthRecords",
                type: "character varying(500)",
                maxLength: 500,
                nullable: true,
                oldClrType: typeof(string),
                oldType: "character varying(1000)",
                oldMaxLength: 1000,
                oldNullable: true);
        }
    }
}