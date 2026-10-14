# Análisis de empleo e ingresos con datos públicos (ENOE, INEGI)

Investigación personal sobre datos del INEGI y cómo afectan a un estado de México seleccionado: **San Luis Potosí frente al promedio nacional**.

## Preguntas
1. ¿Cuánto cambia el ingreso mensual de los ocupados según su escolaridad en San Luis Potosí frente al promedio nacional, con y sin ponderar por el factor de expansión?
2. ¿Qué sectores de actividad pagan más y menos en San Luis Potosí, y cómo se comparan con el país?
3. ¿Qué porcentaje de los ocupados está en informalidad en San Luis Potosí frente al país, y cómo cambia por escolaridad y sector?

## Datos
ENOE, segundo trimestre de 2026, tabla sociodemográfica `SDEMT`. Detalle, fecha de descarga y hash en [FUENTE.md](FUENTE.md).

## Entorno
```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```
Copia `.env.example` a `.env` y llena tus credenciales de PostgreSQL 

## Estructura
`data/` (ignorada por Git) · `sql/` consultas · `src/` scripts · `notebooks/` · `reports/figures/` gráficas
