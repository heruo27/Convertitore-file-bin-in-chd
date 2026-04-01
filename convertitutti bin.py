import os
import subprocess
import glob

def process_folders():
    # Ottieni la cartella corrente (dove si trova lo script)
    root_dir = os.getcwd()

    # Cammina attraverso tutte le sottocartelle
    for subdir, dirs, files in os.walk(root_dir):
        # Filtra solo i file .bin (case-insensitive) nella cartella attuale
        bin_files = sorted([f for f in files if f.lower().endswith('.bin')])

        if not bin_files:
            continue

        print(f"\n--- Elaborazione cartella: {os.path.basename(subdir)} ---")

        # Cambia la directory di lavoro nella sottocartella per chdman
        os.chdir(subdir)

        # Nome base del gioco (usiamo il nome della cartella stessa)
        game_name = os.path.basename(subdir)
        cue_filename = f"{game_name}.cue"
        chd_filename = f"{game_name}.chd"

        # 1. Crea il file .cue
        print(f"  > Generazione {cue_filename}...")
        try:
            with open(cue_filename, 'w') as f:
                for i, bin_file in enumerate(bin_files):
                    track_num = i + 1
                    track_type = "MODE1/2352" if track_num == 1 else "AUDIO"
                    f.write(f'FILE "{bin_file}" BINARY\n')
                    f.write(f'  TRACK {track_num:02d} {track_type}\n')
                    f.write(f'    INDEX 01 00:00:00\n')

            # 2. Esegui chdman
            print(f"  > Compressione in {chd_filename}...")
            # createcd: crea il CHD dal file CUE
            subprocess.run(['chdman', 'createcd', '-i', cue_filename, '-o', chd_filename],
                           check=True, stdout=subprocess.DEVNULL)

            print(f"  > [OK] Completato!")

            # 3. Pulizia (Opzionale: decommenta le righe sotto per eliminare i file originali)
            # os.remove(cue_filename)
            # for b in bin_files: os.remove(b)

        except Exception as e:
            print(f"  > [ERRORE] in {game_name}: {e}")

        # Torna alla root_dir per il prossimo ciclo
        os.chdir(root_dir)

if __name__ == "__main__":
    process_folders()
    print("\n--- Processo terminato su tutte le cartelle! ---")
