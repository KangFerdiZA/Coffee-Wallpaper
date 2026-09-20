import os
import json
from PIL import Image

def process_wallpapers():
    input_dir = "raw_images"       # Folder tempat Anda upload gambar mentah
    output_dir = "wallpapers"      # Folder hasil webp
    
    # Ganti dengan username, nama repo, dan branch Anda (misal: main)
    github_raw_base_url = "https://raw.githubusercontent.com/USERNAME/REPO_NAME/main/wallpapers"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wallpaper_list = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Directory '{input_dir}' not found.")
        return

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            img_path = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            webp_filename = f"{base_name}.webp"
            webp_path = os.path.join(output_dir, webp_filename)
            
            try:
                with Image.open(img_path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGBA")
                    else:
                        img = img.convert("RGB")
                    # Simpan sebagai WebP dengan kualitas 85% agar optimal untuk wallpaper mobile
                    img.save(webp_path, "WEBP", quality=85)
                print(f"Converted: {filename} -> {webp_filename}")
                
                title = base_name.replace("_", " ").replace("-", " ").title()
                
                wallpaper_item = {
                    "id": base_name,
                    "title": title,
                    "category": "Coffee",
                    "url": f"{github_raw_base_url}/{webp_filename}"
                }
                wallpaper_list.append(wallpaper_item)
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    # Struktur JSON Remote (Termasuk Konfigurasi AdMob)
    config = {
        "app_name": "Coffee Wallpaper",
        "package_name": "com.CoffeeWallpaper01",
        "admob": {
            "banner_id": "ca-app-pub-3940256099942544/6300978111",      # Bisa diubah jarak jauh via GitHub
            "interstitial_id": "ca-app-pub-3940256099942544/1033173712" # Bisa diubah jarak jauh via GitHub
        },
        "wallpapers": wallpaper_list
    }
    
    json_path = "wallpapers.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    print(f"Successfully generated {json_path} with {len(wallpaper_list)} items.")

if __name__ == "__main__":
    process_wallpapers()
