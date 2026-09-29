# Guía paso a paso del taller

**Análisis de datos energéticos y dashboards de control con Pandas + Power BI**

---

## 1. Requisitos

| Herramienta | Versión | Uso |
|---|---|---|
| Windows | 10 u 11 | Sistema operativo de la práctica |
| Python | 3.10 o superior | Ejecutar los scripts |
| Pandas | 2.2 o superior | Manipular las tablas |
| Power BI Desktop | Versión gratuita | Construir el tablero |

### 1.1 Crear el entorno virtual

Un entorno virtual es una carpeta aislada donde quedan los paquetes de la
práctica, sin tocar la instalación de Python de la máquina.

En PowerShell, dentro de la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

> Si PowerShell bloquea la activación, ejecuta primero:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Cuando el entorno está activo, la terminal muestra `(.venv)` al principio de la línea.

### 1.2 Instalar los paquetes

Con el entorno activo:

```powershell
python -m pip install pandas
```

`pandas` es el único paquete que necesita la práctica (instala también `numpy`
automáticamente).

### 1.3 Ejecutar los scripts

```powershell
python cargar_y_limpiar.py
python preparar_powerbi.py
```

> Al terminar la práctica puedes desactivar el entorno con `deactivate`.

---

## 2. Parte 1 — Python

Ejecuta los dos scripts en orden (comandos en el paso 1.4), porque cada uno
usa el archivo que dejó el anterior:

| Orden | Script | Entrada | Salida |
|---|---|---|---|
| 1º | `cargar_y_limpiar.py` | `data/consumo_energia.csv` | `salida/datos_limpios.csv` |
| 2º | `preparar_powerbi.py` | `salida/datos_limpios.csv` | los otros 3 CSV |

### Paso 1 — Cargar y limpiar

Qué hace: lee el CSV con `read_csv`, revisa tipos de dato, busca incompletos y repetidos, limpia la tabla y agrega columnas nuevas.

Conceptos de Pandas que se practican:

| Concepto | Para qué se usa |
|---|---|
| `read_csv` | Leer el archivo |
| `head`, `dtypes`, `shape` | Ver qué se cargó |
| `isnull().sum()` | Contar datos vacíos |
| `duplicated()`, `drop_duplicates()` | Quitar repetidos |
| `to_datetime` | Convertir la fecha |
| `to_numeric` | Asegurar que el consumo sea número |
| `fillna` | Rellenar consumos vacíos |
| `str.strip()`, `str.title()` | Corregir " sede norte " → "Sede Norte" |
| `datos[condición]` | Filtrar filas |
| `groupby` | Resumir consumo por sede |
| `sort_values` | Ordenar por fecha |

Resultado esperado (los números deben coincidir):

```
Filas iniciales: 826
Filas finales: 787
Datos vacios: 0
```

Columnas que se agregan para el tablero: `mes`, `mes_nombre`, `dia_semana`, `es_fin_de_semana` y `costo_usd`.

### Paso 2 — Preparar las tablas del tablero

Qué hace: con `groupby` calcula los totales que luego se usan en Power BI.

Conceptos: `groupby(...).agg(...)`, `value_counts`, `nlargest`, `sort_values`, `to_csv`.

Los 3 archivos que se importan en Power BI:

| Archivo | Filas | Para qué sirve |
|---|---|---|
| `datos_limpios.csv` | 787 | Tabla principal: alimenta los 3 gráficos |
| `resumen_mensual.csv` | 9 | Consumo y costo por mes y sede |
| `kpi_sedes.csv` | 3 | Indicadores por sede |

---

## 4. Parte 2 — Power BI Desktop

### 4.1 Importar los 3 archivos

1. `Inicio > Obtener datos > Texto/CSV`
2. En `salida/` elige un archivo y pulsa *Abrir* (el diálogo solo permite uno a la vez).
3. Pulsa *Cerrar y aplicar*.
4. Repite 3 veces con: `datos_limpios`, `resumen_mensual`, `kpi_sedes`.

Al terminar debes tener 3 tablas en la vista de datos.

### 4.3 Transformar los datos

En Power BI, la vista *Transformar datos* permite revisar y modificar los datos antes de construir los gráficos. En esta se pueden corregir errores, cambiar tipos de datos, crear columnas calculadas y eliminar filas.

En caso de que los Power BI tome el punto decimal como divisor de miles, se puede cambiar dando click derecho sobre la columna y eligiendo *Cambiar tipo* > *Decimal*.

### 4.2 Página 1 — Resumen energético (3 gráficos)

Los 3 gráficos se construyen con la tabla `datos_limpios`. Por eso los segmentadores los filtran a todos al mismo tiempo.

**a) Gráfico de columnas apiladas**
- Insertar > Gráfico de columnas apiladas
- Eje X: `datos_limpios` > `mes_nombre`
- Leyenda: `datos_limpios` > `sede`
- Eje Y: *Suma de* `datos_limpios` > `consumo_kwh`

**b) Gráfico circular**
- Leyenda: `datos_limpios` > `categoria`
- Valores: *Suma de* `datos_limpios` > `consumo_kwh`

**c) Segmentaciones (slicers)**
- Inserta dos segmentaciones de cualquier tipo desde `datos_limpios`: `sede` y `mes_nombre`.
- Al hacer clic en un valor, los 3 gráficos se filtran.

**d) Tarjeta de indicador**
- Insertar > Tarjeta
- Valores: *Suma de* `kpi_sedes` > `consumo_total_kwh`

### 4.3 Guardar el tablero

`Archivo > Guardar como` → `taller_powerbi.pbix` en la carpeta del proyecto.

## 5. Crear archivo comprimido para entregar

1. Cierra Power BI Desktop.
2. Comprime todos los archivos de la carpeta en un ZIP a excepción de la carpeta `.venv` (que es muy grande y no hace falta).
3. Entrega el archivo ZIP en el grupo de whatsapp.

**Fecha límite:** 30 de junio de 2024, 18:00 horas.
