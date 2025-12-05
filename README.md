# SpaceParts Dashboard

> **Last Updated**: December 2, 2025 - PostgreSQL Version

Dashboard interactivo de Business Intelligence para análisis de ventas y operaciones.

## 🚀 Demo en Vivo

**URL**: https://spaceparts-dashboard-report.streamlit.app/

## 📊 Características

- **KPIs en Tiempo Real**: Ventas, Margen, OTD%, Órdenes
- **Visualizaciones Interactivas**: Gráficos de Plotly con filtros dinámicos
- **Base de Datos PostgreSQL**: Datos persistentes en Neon.tech
- **Performance Optimizada**: Queries eficientes, carga rápida
- **Responsive Design**: Tema oscuro profesional

## 🗄️ Arquitectura

```
┌─────────────────┐
│  Streamlit App  │
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Neon.tech     │
│  PostgreSQL DB  │
└─────────────────┘
```

## 🛠️ Setup Local

### Prerrequisitos
- Python 3.8+
- Cuenta en Neon.tech (gratis)
- Git

### Instalación

1. **Clonar repositorio**
```bash
git clone https://github.com/fayderarroyo/spaceparts-dashboard.git
cd spaceparts-dashboard
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**

Crea el archivo `.streamlit/secrets.toml`:

```toml
[database]
host = "your-host.neon.tech"
port = "5432"
database = "neondb"
user = "your-user"
password = "your-password"
```

4. **Ejecutar app**
```bash
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
spaceparts-dashboard/
├── app.py                      # App principal
├── requirements.txt            # Dependencias Python
├── .streamlit/
│   └── secrets.toml           # Credenciales DB (no en Git)
├── DEPLOYMENT.md              # Guía de deployment
└── README.md                  # Este archivo
```

## 🚀 Deployment en Streamlit Cloud

1. **Push a GitHub**
```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

2. **Configurar en Streamlit Cloud**
- Ve a [share.streamlit.io](https://share.streamlit.io)
- Settings → Secrets
- Pega el contenido de `secrets.toml`
- Reboot app

## 🎯 Tecnologías

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, Pandas
- **Database**: PostgreSQL (Neon.tech)
- **ORM**: SQLAlchemy
- **Deployment**: Streamlit Cloud

## 📈 Performance

| Métrica | Valor |
|---------|-------|
| Tiempo de carga | 3-5s |
| Memoria usada | ~200 MB |
| Escalabilidad | Excelente |

## 👤 Autor

**Fayder Arroyo**
- Portfolio: [fayderarroyo.github.io](https://fayderarroyo.github.io/CV-Website/)
- LinkedIn: [linkedin.com/in/fayderarroyo](https://linkedin.com/in/fayderarroyo)
- GitHub: [@fayderarroyo](https://github.com/fayderarroyo)

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

---

**Construido con ❤️ para demostrar habilidades de Data Analytics y BI**
