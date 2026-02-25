# Facturae (Spain) Module

Electronic invoicing for Spanish public administration (Facturae format).

## Features

- Generate Facturae-compliant XML electronic invoices for Spanish public sector
- Track invoice lifecycle through statuses: draft, generated, submitted, accepted, rejected
- Record recipient details including name and tax ID (NIF/CIF)
- Submit invoices to FACe or other Spanish e-invoicing platforms
- Track submission timestamps, XML generation dates, and response codes
- Dashboard with overview of all Facturae invoice activity

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Facturae (Spain) > Settings**

## Usage

Access via: **Menu > Facturae (Spain)**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/facturae/dashboard/` | Overview of Facturae invoice status and activity |
| Invoices | `/m/facturae/invoices/` | List and manage Facturae invoices |
| Settings | `/m/facturae/settings/` | Configure Facturae module settings |

## Models

| Model | Description |
|-------|-------------|
| `FacturaeInvoice` | Electronic invoice record with recipient details, amounts, XML generation and submission tracking |

## Permissions

| Permission | Description |
|------------|-------------|
| `facturae.view_facturaeinvoice` | View Facturae invoices |
| `facturae.generate_facturae` | Generate Facturae XML files |
| `facturae.submit_facturae` | Submit Facturae invoices to public administration |
| `facturae.manage_settings` | Manage Facturae module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
