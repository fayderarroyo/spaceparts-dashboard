# SpaceParts Dashboard - Deployment Guide

## Paso 1: Preparar el Repositorio

Ya creaste el repositorio: `https://github.com/fayderarroyo/spaceparts-dashboard.git`

## Paso 2: Subir el Código

Desde la carpeta `streamlit-dashboard`, ejecuta:

```powershell
cd streamlit-dashboard
git init
git add .
git commit -m "Initial commit: SpaceParts Dashboard"
git remote add origin https://github.com/fayderarroyo/spaceparts-dashboard.git
git branch -M main
git push -u origin main
```

## Paso 3: Desplegar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en **"New app"**
3. Selecciona tu repositorio: `fayderarroyo/spaceparts-dashboard`
4. Main file path: `app.py`
5. Haz clic en **"Deploy"**

¡Listo! Tu dashboard estará en vivo en unos minutos.

## Paso 4: Enlazar desde tu Portafolio

Actualiza el archivo `data.js` en tu portafolio web para agregar el enlace al dashboard:

```javascript
{
    title: "SpaceParts - Business Intelligence",
    desc: "Dashboard interactivo con datos en tiempo real desde Google Drive",
    tags: ["Streamlit", "Python", "Plotly", "Google Drive"],
    image: "assets/images/spaceparts-1.png",
    link: "https://tu-app.streamlit.app"  // URL que te dará Streamlit Cloud
}
```

## Notas Importantes

- Los datos se descargan automáticamente desde Google Drive la primera vez
- Streamlit cachea los datos por 1 hora para mejor rendimiento
- La app funciona 100% gratis en Streamlit Cloud
