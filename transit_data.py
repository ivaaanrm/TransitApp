import csv
from typing import List
from datetime import datetime
from dataclasses import dataclass, field, asdict

@dataclass(frozen=True)
class Resultado:
    causa: str
    nivel: str
    via: str
    km_inicio_fin: str
    longitud: str
    demarcacion: str
    tramo: str
    direccion: str
    inicio: str
    observaciones: str
    fecha: str = field(default=datetime.now().strftime("%d-%m-%Y"))

class Message:
    @staticmethod
    def update_traffic_message(traffic_status: List[Resultado]):        
        template = "🚦 Traffic Update 🚦\n\n"
        if traffic_status:
            # Iterate through each Resultado and print as a string
            for resultado in traffic_status:
                template += (
                    f"⚠️ {resultado.causa} {resultado.via} ➡️ {resultado.direccion}\n"
                    f"Nivel: {resultado.nivel}\n"
                    f"Tramo: {resultado.longitud} km - {resultado.tramo}\n"
                    f"Inicio: {resultado.inicio}\n"
                    f"{resultado.observaciones}\n\n"
                )
        else:
            template += "* No hay incidencias ✅"
        return template
    


def save_results_to_csv(results: List[Resultado], csv_filename: str):
    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = Resultado.__annotations__.keys() 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write results to CSV
        for result in results:
            writer.writerow(asdict(result))

def load_results_from_csv(csv_filename: str) -> List[Resultado]:
    results = []
    try:
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                results.append(Resultado(**row))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    return results
        

