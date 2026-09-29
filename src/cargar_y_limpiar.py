import os

import pandas as pd

PRECIO_USD_KWH = 0.12

MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def numero(valor):
    return f"{valor:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")

def main():
    datos = pd.read_csv("data/consumo_energia.csv", encoding="utf-8-sig")
    crudos = len(datos)

    print("Primeras 5 filas del DataFrame original:")
    print(datos.head(5).to_string(index=False))
    
    print("\nTipos de datos originales:")
    print(datos.dtypes.to_string())

    print("\nNúmero de filas originales:", len(datos))
    datos = datos.drop_duplicates()
    print("Número de filas después de eliminar duplicados:", len(datos))
    
    antes = len(datos)
    datos["fecha"] = pd.to_datetime(datos["fecha"], format="%Y-%m-%d", errors="coerce")
    datos = datos.dropna(subset=["fecha"])
    print(f"quitadas {antes - len(datos)} filas con fechas inválidas")

    datos["consumo_kwh"] = pd.to_numeric(datos["consumo_kwh"], errors="coerce")
    nulos_consumo = datos["consumo_kwh"].isnull().sum()
    promedio = datos["consumo_kwh"].mean()
    datos["consumo_kwh"] = datos["consumo_kwh"].fillna(promedio)
    print(f"Se reemplazaron {nulos_consumo} valores nulos de consumo_kwh con el promedio: {numero(promedio)} kWh")

    antes = len(datos)
    limite = promedio * 3
    datos = datos[datos["consumo_kwh"] <= limite]
    print(f"quitadas {antes - len(datos)} filas con consumo_kwh mayor a 3 veces el promedio ({numero(limite)} kWh)")

    antes = len(datos)
    datos = datos[datos["consumo_kwh"] > 0]
    print(f"quitadas {antes - len(datos)} filas con consumo_kwh menor a 0")

    datos["sede"] = datos["sede"].str.strip().str.title()
    datos["categoria"] = datos["categoria"].str.strip().str.title()
    print(f"sedes: {list(datos["sede"].unique())}")
    print(f"categorías: {list(datos["categoria"].unique())}")

    datos["mes"] = datos["fecha"].dt.month
    datos["mes_nombre"] = datos["mes"].map(MESES)
    datos["dia_semana"] = datos["fecha"].dt.dayofweek.map(lambda x: DIAS[x])
    datos["es_fin_de_semana"] = (datos["dia_semana"] == "Sábado") | (datos["dia_semana"] == "Domingo")
    datos["costo_usd"] = (datos["consumo_kwh"] * PRECIO_USD_KWH).round(2)

    datos = datos.sort_values(["fecha", "sede", "categoria"]).reset_index(drop=True)

    print("\n Resultado de la limpieza de datos:")
    print(f"Filas iniciales: {crudos}")
    print(f"Filas finales: {len(datos)}")
    print(f"Datos vacios: {datos.isnull().sum().sum()}")

    print("\n Primeras 5 filas del DataFrame limpio:")
    print(datos.head(5).to_string(index=False))

    print("\n Resumen con groupby por consumo_kwh:")
    print(datos.groupby("sede")["consumo_kwh"].sum().round(2).to_string())

    os.makedirs("salida/", exist_ok=True)
    datos.to_csv("salida/datos_limpios.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
