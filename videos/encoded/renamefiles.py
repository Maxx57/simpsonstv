import os
import re

def rename_video_files():
    """
    Rename video files to standardized format: The.Simpsons.S##E##.mp4
    - Removes extra text after season/episode information
    - Pads single digit season/episode numbers with leading zeros
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Pattern to match The.Simpsons.S##E## with optional single digits
    # Captures: Season number (with or without leading S), Episode number (with or without leading E)
    pattern = r'^(The\.Simpsons\.S)(\d{1,2})(E)(\d{1,2})(\..*)?\.mp4$'
    
    # Get all .mp4 files in the directory
    files = [f for f in os.listdir(script_dir) if f.endswith('.mp4')]
    
    renamed_count = 0
    skipped_count = 0
    
    for filename in files:
        match = re.match(pattern, filename)
        
        if match:
            prefix = match.group(1)  # "The.Simpsons.S"
            season = match.group(2)   # Season number
            e_letter = match.group(3) # "E"
            episode = match.group(4)  # Episode number
            extra = match.group(5)    # Extra text (like .720p.DSNP.WEB-DL...)
            
            # Pad season and episode with leading zeros if needed
            season_padded = season.zfill(2)
            episode_padded = episode.zfill(2)
            
            # Construct the new filename
            new_filename = f"{prefix}{season_padded}{e_letter}{episode_padded}.mp4"
            
            # Only rename if the filename would change
            if filename != new_filename:
                old_path = os.path.join(script_dir, filename)
                new_path = os.path.join(script_dir, new_filename)
                
                # Check if target filename already exists
                if os.path.exists(new_path):
                    print(f"[!] Skipping {filename}: Target {new_filename} already exists")
                    skipped_count += 1
                else:
                    os.rename(old_path, new_path)
                    print(f"[+] Renamed: {filename} -> {new_filename}")
                    renamed_count += 1
            else:
                print(f"[-] Skipped: {filename} (already in correct format)")
                skipped_count += 1
        else:
            print(f"[!] Skipped: {filename} (doesn't match expected pattern)")
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: {renamed_count} files renamed, {skipped_count} files skipped")
    print(f"{'='*60}")

if __name__ == "__main__":
    rename_video_files()
