![image](https://github.com/user-attachments/assets/b87d2a6f-8f5b-4a86-9c29-3f1ada29ff69)


Este repositorio contiene un modelo de programación lineal en Python que resuelve un problema de distribución de agua mediante camiones cisterna (pipas) en contextos urbanos con escasez hídrica. La motivación del proyecto surge de la necesidad urgente de hacer más eficiente y equitativo el reparto de agua en ciudades mexicanas donde este servicio es esencial, pero muchas veces gestionado de forma informal o subóptima.

## 🎯 Propósito

El objetivo del modelo es mostrar cómo herramientas de optimización accesibles pueden aplicarse al diseño de políticas de distribución de agua, especialmente en zonas donde el reparto por pipas es la única fuente confiable de acceso. El trabajo está inspirado en iniciativas reales como:

- El programa “Agua Gratuita para tu Familia” (San Luis Potosí)
- Reparto de agua de emergencia en Monterrey y la CDMX
- Soluciones tecnológicas como sensores IoT de Kraken Agua o apps ciudadanas como “Agua Chinelo” en Cuernavaca

## 🧠 ¿Qué hace este modelo?

- Minimiza el costo total de entrega a lo largo de una semana de planificación.
- Respeta las limitaciones operativas de cada camión (capacidad, tiempo de trabajo).
- Considera franja horaria (mañana, mediodía, tarde) con costos variables.
- Impone mínimos de entrega diarios por camión para balance de carga.
- Establece mínimos semanales por colonia para garantizar equidad.
- Controla máximos de almacenamiento semanal por colonia para evitar rebases.
- Genera una visualización interactiva de las entregas por camión y colonia.

## 📊 Resultado Esperado

Al ejecutar el script principal, se obtiene una gráfica de entregas por camión y por colonia a lo largo del tiempo, permitiendo observar patrones operativos como:

- Distribución especializada de la flota
- Reparto constante en colonias de menor demanda
- Utilización intensiva de camiones eficientes para zonas con alta necesidad

Esto proporciona una herramienta práctica para diseñar y evaluar políticas públicas más justas y sustentables en el reparto de agua.

## 📦 Requisitos

- Python 3.8+
- `numpy`
- `scipy`
- `plotly`

Puedes instalar las dependencias fácilmente con:

```bash
pip install numpy scipy plotly

▶️ Ejecución

Simplemente corre el archivo principal
watertruckdelivery.py

Este proyecto está disponible bajo la licencia MIT.
📬 Contacto

Desarrollado por Adrián Guel. Si quieres proponer mejoras o contribuir al proyecto, ¡los PRs son bienvenidos!
