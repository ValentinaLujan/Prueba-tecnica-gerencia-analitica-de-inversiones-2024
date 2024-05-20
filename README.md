# Prueba-tecnica-gerencia-analitica-de-inversiones-2024 

## Descripción

Esta herramienta permite a los gerentes comerciales de inversión visualizar y analizar el portafolio de sus clientes de manera automatizada y eficiente. Proporciona información sobre la composición del portafolio por cliente, por banca y por perfil de riesgo, así como la evolución de los Activos Bajo Administración (ABA) promedio.

## Estructura del Proyecto

- `tablas.sql`: Script SQL para crear la base de datos y las tablas necesarias.
- `cargar_datos.py`: Carga los datos de los archivos CSV en PostgreSQL.
- `limpieza_datos.sql`: Contiene las consultas SQL para limpiar, ajustar y transformar los datos.
- `app.py`: Implementa la aplicación Dash para la visualización de los datos.
- `diagramas`: En esta carpeta se encuentran el diagrama de entidad - relación de la base de datos y el diagrama del proceso empleado para la realización del proyecto 
- `data`: En esta carpeta se deben agregar los archivos.csv proporcionados para la realización del reto
- `README.md`: Proporciona una visión general del proyecto y las instrucciones de uso.

## Instalación y Ejecución

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/ValentinaLujan/Prueba-tecnica-gerencia-analitica-de-inversiones-2024.git
    ```

2. Verificar que se cuente con todas las librerias necesarias para la ejecución del programa. Estas son:
    dash
    pandas
    plotly
    sqlalchemy
    psycopg2

3. Crear la base de datos "Inversiones" en PostgreSQL 

4. Configurar la base de datos y tablas en PostgreSQL utilizando para esto el script `tablas.sql` (Ejecutar desde PostgreSQL)

5. Actualizar en `cargar_datos.py` con tus credenciales de base de datos (Usuario y contraseña).

6. Agregar a la carpeta `data` los archivos.csv proporcionados para la realización del reto

6. Cargar los datos en la base de datos:
    ```bash
    python cargar_datos.py
    ```

7. Ejecutar las consultas SQL para para limpiar, ajustar y transformar los datos presentes en el archivo `limpieza_datos.sql` desde PostgreSQL


8. Ejecutar la aplicación Dash:
    ```bash
    python app.py
    ```
En este archivo se encuentran las consultas hechas en SQL para obtener los gráficos, si desea ver este codigo a detalle lo puede hacer en el archivo `query.sql`


Como extra, se graficó como se comportan los macroactivos y activos en la tabla "historico_aba_macroactivos", estos gráficos se observan al final del dashboard. Estos gráficos permiten obtener una visión más completa de como se distribuyen estas dos variables a lo largo de la tabla. 

## Conclusiones Técnicas
- La correcta centralización de las bases de datos permite acceder a la información de una manera más sencilla, reduciendo el tiempo y esfuerzo necesarios para manejar múltiple fuentes. En este caso, el uso correcto de las claves foraneas fue fundamental para el desarrollo del proyecto, logrando conseguir con estas una base de datos relacional bien estructurada
- El modelado y la normalización de datos son procesos indispensables antes de analizar una base de datos. Estos procesos evitan la redundancia y asegura la integridad de los datos, mejorando la efectividad y alcance de las consultas
- Las consultas en SQL deben ser específicas para poder extraer y calcular los datos necesarios, si estas se hacen correctamente pueden proporcionar información precisa y relevante para conocer los datos y tomar decisiones informadas. 
- Las visualizaciones mejoran completamente la comprensión de los datos y apoyan la toma de decisiones, especialmente cuando se trata de bases de datos muy grandes y con tablas que poseen un número considerable de registros.  
- El sistema es escalable y puede ajustarse para incluir nuevas fuentes de datos o modificar las consultas y visualizaciones según las necesidades que se presenten.
- Puede ser bastante común que al ingresar los datos a la tabla se cometan errores, por lo que varios registros tendrían que ser tomados como nulos o redefinidos según la interpretación del programador

## Conclusiones de Negocio
-  Los dashboards facilitan el acceso a información clave y su interpretación, mejorando la capacidad de los gerentes para acceder a la información de sus clientes, identificar oportunidades de inversión y gestionar riesgos.
- Al revisar la gráfica del portafolio de clientes se puede observar que hay clientes que repetidamente hacen uso de estos servicios mientras que otros representan un porcentaje bastante pequeño.
- Al revisar la gráfica del portafolio de banca podemos observar que la banca que tiene mayor promedio del ABA (Activos Bajo Administración) es la de "Empresas", mientras que la que menos tiene es la "Personal".
- En cuanto a la gráfica del portafolio de riesgo, podemos observar que la que tiene mayor promedio del ABA es la del perfil "Conservador", teniendo una gran diferencia con los otros perfiles, donde tanto el perfil "Agresivo" como el perfil "Sin definir" tienen un valor promedio bastante bajo en comparación con el Conservador. 
- Si analizamos la evolución mes a mes del ABA (Activos Bajo Administración) promedio, podemos observar que este es bastante similar en el periodo analizado, teniendo un incremento notorio en los meses de enero y febrero de este año
- Al analizar la gráfica del porcentaje de macroactivos podemos ver que tanto "Renta Variable" como "FICs" son macroactivos bastante empleados por los clientes, mientras que "Renta Fija" no es muy usado al solo representar el 3.39% de todos los macroactivos empleados.
- Por ultimo, al analizar la gráfica del porcentaje de activos, podemos observar que al igual que en el punto anterior hay activos bastante empleados como "Ecopetrol", "Fiducuenta" y "Renta Liquidez" que juntos suman alrededor del 59.4% de los activos empleados, mientras que hay otros como "CEMARGOS" que representa tan solo el 0.0751% de todos los activos empleados.

## Video de Demostración

Falta

## Autor

Valentina Luján Robledo ()
