import argparse
import os

CHR_ROM_SIZE = 8192  # NES CHR-ROM is typically 8 KB
TILE_SIZE = 16       # 16 bytes per tile

def chr_to_byte_rows(filename, tiles_to_read=1, start_tile=0):
    with open(filename, "rb") as f:
        data = f.read()

    total_bytes_needed = tiles_to_read * TILE_SIZE
    start_offset = start_tile * TILE_SIZE
    end_offset = start_offset + total_bytes_needed

    if end_offset > len(data):
        raise ValueError("Requested tiles exceed file size.")

    # Automatically create output filename with .asm extension
    base_name = os.path.splitext(filename)[0]
    output_file = base_name + ".asm"

    with open(output_file, "w") as out:
        for tile_index in range(tiles_to_read):
            offset = start_offset + tile_index * TILE_SIZE
            tile_bytes = data[offset:offset + TILE_SIZE]

            plane0 = tile_bytes[:8]
            plane1 = tile_bytes[8:]

            out.write(f"; Tile {start_tile + tile_index}\n")
            out.write(".byte " + ",".join(f"${byte:02X}" for byte in plane0) + "\n")
            out.write(".byte " + ",".join(f"${byte:02X}" for byte in plane1) + "\n\n")

        # Append .res to fill remaining CHR-ROM space
        remaining = CHR_ROM_SIZE - total_bytes_needed
        out.write("; Fill rest with empty tiles\n")
        out.write(f".res {remaining:>5}               ; Rest of CHR-ROM ({CHR_ROM_SIZE} - {total_bytes_needed} = {remaining} bytes)\n")

    print(f"✅ Output written to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert NES CHR tiles to .byte statements for assembly.")
    parser.add_argument("file", help="Path to .chr file")
    parser.add_argument("--start", type=int, default=0, help="Starting tile index (default: 0)")
    parser.add_argument("--count", type=int, default=1, help="Number of tiles to extract (default: 1)")

    args = parser.parse_args()
    chr_to_byte_rows(args.file, args.count, args.start)

if __name__ == "__main__":
    main()
