import os
import pandas as pd

def main():
    datos = pd.read_csv("salida/datos_limpios.csv", encoding="utf-8-sig")

    print("Resumen por mes y sede:")
    resumen_mensual = (
        datos.groupby(["mes", "mes_nombre", "sede"], as_index=False)
        .agg(
            consumo_kwh=("consumo_kwh", "sum"),
            costo_usd=("costo_usd", "sum"),
            dias_medidas=("fecha", "nunique"),
        )
        .sort_values(["mes", "consumo_kwh"], ascending=[True, False])
    )
    resumen_mensual["consumo_kwh"] = resumen_mensual["consumo_kwh"].round(1)
    print(resumen_mensual.to_string(index=False))

    print("Indicadores por sede (KPI)")
    kpi_sede = datos.groupby("sede", as_index=False).agg(
        consumo_total_kwh=("consumo_kwh", "sum"),
        consumo_promedio_kwh=("consumo_kwh", "mean"),
        dias_medidos=("fecha", "nunique"),
    )
    kpi_sede["consumo_total_kwh"] = kpi_sede["consumo_total_kwh"].round(1)
    kpi_sede["consumo_promedio_kwh"] = kpi_sede["consumo_promedio_kwh"].round(1)
    kpi_sede["participacion_pct"] = (kpi_sede["consumo_total_kwh"] / kpi_sede["consumo_total_kwh"].sum() * 100).round(1)
    kpi_sede = kpi_sede.sort_values("consumo_total_kwh", ascending=False)
    print(kpi_sede.to_string(index=False))

    os.makedirs("salida/", exist_ok=True)
    archivos = {
        "datos_limpios.csv": datos,
        "resumen_mensual.csv": resumen_mensual,
        "kpi_sede.csv": kpi_sede,
    }
    for nombre, tabla in archivos.items():
        tabla.to_csv(f"salida/{nombre}", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
