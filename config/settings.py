# =============================================================================
# config/settings.py - Configuration management
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': os.getenv('SENDER_EMAIL', 'dango.vq@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', ''),
    'recipient_email': os.getenv('RECIPIENT_EMAIL', 'burgos1269@gmail.com'),
    'subject_template': 'Reporte Contrataciones Menores - {date}',
    'cc': os.getenv('CC', 'a.burgos.n05@gmail.com')
}

# Scraper configurations
SCRAPERS_CONFIG = {
    'example_static_site':
        {
            'type': 'static',
            'base_url': 'https://example.com/records',
            'description_column': 'description',
            'max_pages': 10,
            'selectors': {
                'records_container': '.records-table tbody tr',
                'title': 'td:nth-child(1)',
                'description': 'td:nth-child(2)',
                'date': 'td:nth-child(3)',
                'next_page': '.pagination .next'
            }
        },
    'contratos_menores_seace':
        {
            'type': 'dynamic',
            'base_url': 'https://prod6.seace.gob.pe/buscador-publico/contrataciones',
            'description_column': 'content',
            'selectors': {
                'checkbox_vigente': '/html/body/main/div/app-root/app-contrataciones/div/div/div[2]/div[1]/app-filtro/form/div[5]/span[1]/mat-checkbox/div/div/input',
                'dropdown_department': '/html/body/main/div/app-root/app-contrataciones/div/div/div[2]/div[1]/app-filtro/form/div[6]/ng-select',
                'select_department': '/html/body/ng-dropdown-panel/div/div[2]/div[6]',
                'paginator': '//*[@class="mat-mdc-paginator-range-label"]',
                'dropdown_records_per_page': '/html/body/main/div/app-root/app-contrataciones/div/div/div[2]/div[2]/mat-paginator/div/div/div[1]/mat-form-field',
                'max_records': '/html/body/div[5]/div[2]/div/div/mat-option[4]',
                'all_calls': '//*[@id="single-spa-application:@s8uitContainerApp/s8uitbuscadorpublico"]/app-root/app-contrataciones/div/div/div[2]/div[2]/div/lista-contrataciones/div/div',
                'ps': ".//p",
                'url': ".//a[starts-with(@href, '/buscador-publico/contrataciones')]",
            },
            'wait_time': 10
        }
    }

# Gemini API configuration
GEMINI_CONFIG = {
    'api_key': os.getenv('GEMINI_API_KEY', ''),
    'model': 'gemini-2.5-flash-lite',
    'max_retries': 3,
    'retry_delay': 1,
    'response_mime_type': 'application/json',
}