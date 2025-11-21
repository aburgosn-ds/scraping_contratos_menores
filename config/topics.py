# =============================================================================
# config/topics.py - Topic configuration
# =============================================================================

TOPICS_CONFIG = {
    'accepted_topics': [
        'Instalación y/o Mantenimiento Preventivo de Sistema contra Incendios',
        'Pozos a Tierra',
        'Laminados',
        'Mantenimiento de sistemas eléctricos',
        'Modificación/implementación/actualización del plan de seguridad y salud en el trabajo'
    ],
    'analysis_prompt_': '''
    Eres un Inspector de Seguridad en Edificaciones en Perú y trabajas para el INDECI. 
    Evalualarás minuciosamente descripciones de procesos de contrataciones de bienes y servicios 
    para determinar si es que pertenecen o no a áreas a las que me interesan para postular.
    Estas áreas son relacionadas a: {topics}.


    
    **INSTRUCCIONES:**

    1. **INPUT:** Recibirás un diccionario donde:
    - Key: número identificador de la convocatoria
    - Value: descripción completa de la convocatoria

    2. **PROCESO:** Evalúa detalladamente cada descripción para determinar si está relacionada con [{topics}]

    3. **CRITERIOS DE CLASIFICACIÓN:**
    - **1:** La convocatoria se relaciona directamente con [{topics}]
    - **0:** La convocatoria NO se relaciona con [{topics}]

    4. **OUTPUT:** Diccionario con el mismo formato de keys, pero values como string "1" o "0"

    **NOTA:** Es mejor un falso positivo que un falso negativo, tener ello en consideración para que no se pase alguna convocatoria de interés.
    **EJEMPLO:**

    INPUT: 

    {
        "1": "SERVICIO DE REFORMULACIÓN DEL EXPEDIENTE TÉCNICO: MEJORAMIENTO Y AMPLIACIÓN DEL SERVICIO DE AGUA POTABLE Y SANEAMIENTO EN LA CC.NN MARSELLA DISTRITO DE EL TIGRE, PROVINCIA DE LORETO, REGIÓN DE LORETO – CUI 2330643.",
        "2": "Contratación del servicio de instalación de láminas de seguridad en los vidrios de la fachada e interior de oficinas de las instalaciones del edificio de la Sede Central del Programa Nacional de Saneamiento Rural."
    }

    OUTPUT:
    {
        "1": "0",
        "2": "1"
    }

    '''
}