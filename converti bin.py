import os
import subprocess
import glob

def create_chd_on_debian():
    # Cerca tutti i file .bin nella cartella corrente
    bin_files = sorted(glob.glob("*.bin"))

    if not bin_files:
        print("Errore: Nessun file .bin trovato.")
        return

    # Usa il nome del primo file (senza estensione e senza eventuali tag "Track") come base
    base_name = bin_files[0].split(' (')[0].replace('.bin', '')
    cue_filename = f"{base_name}.cue"
    chd_filename = f"{base_name}.chd"

    print(f"--- Generazione file CUE: {cue_filename} ---")
    with open(cue_filename, 'w') as f:
        for i, bin_file in enumerate(bin_files):
            track_num = i + 1
            # Assunzione standard: traccia 1 = dati, altre = audio
            track_type = "MODE1/2352" if track_num == 1 else "AUDIO"
            f.write(f'FILE "{bin_file}" BINARY\n')
            f.write(f'  TRACK {track_num:02d} {track_type}\n')
            f.write(f'    INDEX 01 00:00:00\n')

    print(f"--- Compressione in CHD: {chd_filename} ---")
    try:
        # Su Debian il comando è 'chdman' (fornito da mame-tools)
        subprocess.run(['chdman', 'createcd', '-i', cue_filename, '-o', chd_filename], check=True)
        print("\nSuccesso! Il file .chd è pronto.")

        # Facoltativo: rimuovi il .cue temporaneo se non ti serve più
        # os.remove(cue_filename)

    except FileNotFoundError:
        print("\nErrore: 'chdman' non trovato. Installa con: sudo apt install mame-tools")
    except subprocess.CalledProcessError as e:
        print(f"\nErrore durante la creazione del CHD: {e}")

if __name__ == "__main__":
    create_chd_on_debian()
