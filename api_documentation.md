# API Documentation for Pagination and Search

## Overview

This document provides detailed information on how to use the pagination and search features implemented across all list APIs in the Maknana API project.

## Pagination

All list APIs in the project now support number pagination, allowing you to retrieve results in manageable chunks.

### Pagination Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `page` | The page number to retrieve | 1 | `?page=2` |
| `page_size` | Number of items per page (max 100) | 10 | `?page_size=20` |

### Pagination Response Format

```json
{
  "count": 100,           // Total number of items
  "next": "http://api.example.org/accounts/?page=4",  // URL to next page (null if none)
  "previous": "http://api.example.org/accounts/?page=2",  // URL to previous page (null if none)
  "results": [
    // List of items on this page
  ]
}
```

### Example Usage

To retrieve the second page with 15 items per page:
```
GET /api/v1/accounts/?page=2&page_size=15
```

## Search

All list APIs support searching across all text fields using case-insensitive contains (icontains) lookup.

### Search Parameter

| Parameter | Description | Example |
|-----------|-------------|---------|
| `search` | Text to search for across all text fields | `?search=keyword` |

### Search Fields

The search is performed on all character-based fields of each model, including:
- CharField
- TextField
- EmailField

### Example Usage

To search for "machine" across all fields:
```
GET /api/v1/factories/?search=machine
```

## Combining Pagination and Search

You can combine both pagination and search in a single request:

```
GET /api/v1/accounts/?search=admin&page=1&page_size=10
```

## API Endpoints with Pagination and Search

### Core App

#### Accounts API
- **Endpoint**: `/api/accounts/`
- **Method**: GET
- **Description**: List all user accounts
- **Example**: `/api/accounts/?search=john&page=1&page_size=10`

#### Clients API
- **Endpoint**: `/api/clients/`
- **Method**: GET
- **Description**: List all clients
- **Example**: `/api/clients/?search=company&page=2`

#### Technicians API
- **Endpoint**: `/api/technicians/`
- **Method**: GET
- **Description**: List all technicians
- **Example**: `/api/technicians/?search=electrical&page=1`

### Machine and Factory App

#### Factories API
- **Endpoint**: `/api/factories/`
- **Method**: GET
- **Description**: List all factories
- **Example**: `/api/factories/?search=production&page=1&page_size=15`

#### Machines API
- **Endpoint**: `/api/machines/`
- **Method**: GET
- **Description**: List all machines
- **Example**: `/api/machines/?search=pump&page=2`

#### Malfunction Requests API
- **Endpoint**: `/api/malfunction-requests/`
- **Method**: GET
- **Description**: List all malfunction requests
- **Example**: `/api/malfunction-requests/?search=urgent&page=1`

#### Malfunction Reports API
- **Endpoint**: `/api/malfunction-reports/`
- **Method**: GET
- **Description**: List all malfunction reports
- **Example**: `/api/malfunction-reports/?search=repair&page=1`

#### Malfunction Invoices API
- **Endpoint**: `/api/malfunction-invoices/`
- **Method**: GET
- **Description**: List all malfunction invoices
- **Example**: `/api/malfunction-invoices/?search=payment&page=1`

#### Automation Requests API
- **Endpoint**: `/api/automation-requests/`
- **Method**: GET
- **Description**: List all automation requests
- **Example**: `/api/automation-requests/?search=system&page=1`

#### Market Categories API
- **Endpoint**: `/api/market-categories/`
- **Method**: GET
- **Description**: List all market categories
- **Example**: `/api/market-categories/?search=electronics&page=1`

#### Market Products API
- **Endpoint**: `/api/market-products/`
- **Method**: GET
- **Description**: List all market products
- **Example**: `/api/market-products/?search=motor&page=1&page_size=20`

#### Market Order Requests API
- **Endpoint**: `/api/market-order-requests/`
- **Method**: GET
- **Description**: List all market order requests
- **Example**: `/api/market-order-requests/?search=pending&page=1`

### Service App

#### Services API
- **Endpoint**: `/api/services/`
- **Method**: GET
- **Description**: List all services
- **Example**: `/api/services/?search=maintenance&page=1`

#### Client Requests API
- **Endpoint**: `/api/client-requests/`
- **Method**: GET
- **Description**: List all client service requests
- **Example**: `/api/client-requests/?search=installation&page=1`

#### Admin Requests API
- **Endpoint**: `/api/admin-requests/`
- **Method**: GET
- **Description**: List all service requests (admin only)
- **Example**: `/api/admin-requests/?search=urgent&page=1`

#### Technician Requests API
- **Endpoint**: `/api/technician-requests/`
- **Method**: GET
- **Description**: List all requests assigned to technician
- **Example**: `/api/technician-requests/?search=repair&page=1`

## Best Practices

1. Always use pagination for list endpoints to improve performance
2. Use specific search terms to narrow down results
3. Combine pagination with search when dealing with large datasets
4. Start with page=1 and a reasonable page_size (10-20) for initial queries
