# E-Commerce Backend Project Documentation

## Overview

This is a Django REST Framework-based e-commerce backend application. It provides APIs for managing users, products, orders, and payments in an online store.

---

## 1. Project Structure

```
ecommerce_project/
├── manage.py
├── ecommerce_backend/          # Main Django project settings
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                   # User authentication & management
├── products/                  # Product catalog management
├── orders/                    # Order processing
└── payments/                  # Payment handling
```

---

## 2. Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | Django 5.2 + Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (Simple JWT) |
| Image Storage | Django ImageField (local storage) |

---

## 3. Database Tables (Models)

### 3.1 Accounts App

#### Role Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| name | Char(50) | Role name (e.g., "Admin", "Customer") |

#### User Table (Custom)
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| username | Char(150) | Unique username |
| email | Email | User email |
| password | Char(128) | Hashed password |
| role | ForeignKey → Role | User role (optional) |
| + All standard Django auth fields (first_name, last_name, is_staff, etc.) |

**Extends:** Django's AbstractUser

---

### 3.2 Products App

#### Category Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| name | Char(255) | Category name |
| parent | ForeignKey → Category | Self-referential for subcategories |

#### Product Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| name | Char(255) | Product name |
| category | ForeignKey → Category | Product category |
| description | Text | Product description |

#### ProductImage Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| product | ForeignKey → Product | Related product |
| image | ImageField | Product image file |

#### ProductVariant Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| product | ForeignKey → Product | Related product |
| price | Decimal(10,2) | Variant price |
| quantity | Integer | Stock quantity |

#### ProductColor Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| color_name | Char(50) | Color name |

#### ProductSize Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| size | Char(50) | Size value |

#### Units Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| unit_type | Char(50) | Unit type (e.g., "Weight") |
| value | Char(50) | Unit value (e.g., "KG") |

#### VariantAttributes Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| product_variant | ForeignKey → ProductVariant | Related variant |
| color | ForeignKey → ProductColor | Color (optional) |
| size | ForeignKey → ProductSize | Size (optional) |
| unit | ForeignKey → Units | Unit (optional) |

---

### 3.3 Orders App

#### Order Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| user | ForeignKey → User | Customer who placed order |
| total_price | Decimal(10,2) | Total order amount |
| status | Char(20) | Order status (Pending/Shipped/Delivered) |
| created_at | DateTime | Order creation timestamp |

#### OrderItem Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| order | ForeignKey → Order | Related order |
| product_variant | ForeignKey → ProductVariant | Product variant ordered |
| quantity | Integer | Quantity ordered |
| price | Decimal(10,2) | Price at time of order |

---

### 3.4 Payments App

#### Payment Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Primary key |
| order | OneToOneField → Order | Related order |
| payment_method | Char(50) | Payment method used |
| payment_status | Char(50) | Payment status |
| transaction_id | Char(100) | Transaction identifier |

---

## 4. Table Relationships Diagram

```
User (1) ──────< Order (1) ──────< OrderItem (many) >────── ProductVariant (1) >────── Product (1) >────── Category (1)
                                                                              │
                                                                              └────< ProductImage
                                                                              │
                                                                              └────< VariantAttributes >──── ProductColor
                                                                                                      >──── ProductSize
                                                                                                      >──── Units

Payment (1) ────── Order (1)
```

---

## 5. API Endpoints

### Base URL: `http://localhost:8000/api/`

### 5.1 Authentication (JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain JWT access & refresh tokens |
| POST | `/api/token/refresh/` | Refresh access token |

**Request Body (Obtain Token):**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1Q...",
  "refresh": "eyJ0eXAiOiJKV1Q..."
}
```

---

### 5.2 Accounts Endpoints

**URL Prefix:** `/api/accounts/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/accounts/users/` | List all users | Yes |
| POST | `/api/accounts/users/` | Create new user | Yes |
| GET | `/api/accounts/users/{id}/` | Get user details | Yes |
| PUT | `/api/accounts/users/{id}/` | Update user | Yes |
| DELETE | `/api/accounts/users/{id}/` | Delete user | Yes |
| GET | `/api/accounts/roles/` | List all roles | Yes |
| POST | `/api/accounts/roles/` | Create new role | Yes |
| GET | `/api/accounts/roles/{id}/` | Get role details | Yes |
| PUT | `/api/accounts/roles/{id}/` | Update role | Yes |
| DELETE | `/api/accounts/roles/{id}/` | Delete role | Yes |

**Create User Request:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "role": 1
}
```

---

### 5.3 Products Endpoints

**URL Prefix:** `/api/products/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/categories/` | List all categories | No |
| POST | `/api/products/categories/` | Create category | Yes |
| GET | `/api/products/categories/{id}/` | Get category | No |
| PUT | `/api/products/categories/{id}/` | Update category | Yes |
| DELETE | `/api/products/categories/{id}/` | Delete category | Yes |
| GET | `/api/products/items/` | List all products | No |
| POST | `/api/products/items/` | Create product | Yes |
| GET | `/api/products/items/{id}/` | Get product details | No |
| PUT | `/api/products/items/{id}/` | Update product | Yes |
| DELETE | `/api/products/items/{id}/` | Delete product | Yes |
| GET | `/api/products/variants/` | List all variants | No |
| POST | `/api/products/variants/` | Create variant | Yes |
| GET | `/api/products/variants/{id}/` | Get variant details | No |
| PUT | `/api/products/variants/{id}/` | Update variant | Yes |
| DELETE | `/api/products/variants/{id}/` | Delete variant | Yes |
| GET | `/api/products/colors/` | List all colors | No |
| POST | `/api/products/colors/` | Create color | Yes |
| GET | `/api/products/sizes/` | List all sizes | No |
| POST | `/api/products/sizes/` | Create size | Yes |
| GET | `/api/products/units/` | List all units | No |
| POST | `/api/products/units/` | Create unit | Yes |

**Create Product with Variants Request:**
```json
{
  "name": "T-Shirt",
  "category": 1,
  "description": "Cotton t-shirt",
  "variants": [
    {
      "price": 25.00,
      "quantity": 100,
      "attributes": [
        {
          "color": 1,
          "size": 1,
          "unit": 1
        }
      ]
    }
  ]
}
```

---

### 5.4 Orders Endpoints

**URL Prefix:** `/api/orders/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List all orders | Yes |
| POST | `/api/orders/` | Create new order | Yes |
| GET | `/api/orders/{id}/` | Get order details | Yes |
| PUT | `/api/orders/{id}/` | Update order | Yes |
| DELETE | `/api/orders/{id}/` | Delete order | Yes |

**Create Order Request:**
```json
{
  "total_price": 75.00,
  "status": "Pending",
  "items": [
    {
      "product_variant": 1,
      "quantity": 2,
      "price": 25.00
    },
    {
      "product_variant": 2,
      "quantity": 1,
      "price": 50.00
    }
  ]
}
```

> **Note:** The `user` field is automatically set from the authenticated request user.

---

### 5.5 Payments Endpoints

**Note:** Payments URLs are currently commented out in the main URL configuration.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/payments/` | List all payments | Yes |
| POST | `/api/payments/` | Create payment | Yes |
| GET | `/api/payments/{id}/` | Get payment details | Yes |
| PUT | `/api/payments/{id}/` | Update payment | Yes |
| DELETE | `/api/payments/{id}/` | Delete payment | Yes |

---

## 6. Authentication & Permissions

### Default Authentication
- **JWT (JSON Web Tokens)** using `rest_framework_simplejwt`
- Token lifetime: 1 day (access), 7 days (refresh)

### Custom Permission
- **IsAdminRole**: Custom permission class in [`products/permissions.py`](products/permissions.py:4)
  - Checks if authenticated user has role with name "Admin"

### Default Settings
- All endpoints require authentication by default
- Override with `permission_classes = []` in views for public access

---

## 7. Database Configuration

Settings in [`ecommerce_backend/settings.py`](ecommerce_backend/settings.py:88):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 8. Project Workflow

### 8.1 Product Management Flow
1. Create a **Category** (e.g., "Electronics")
2. Create a **Product** associated with the category
3. Add **ProductImages** to the product
4. Create **ProductVariants** with price and quantity
5. Add **VariantAttributes** (color, size, unit) to variants

### 8.2 Order Flow
1. Authenticated user creates an **Order**
2. Add **OrderItems** with product variants and quantities
3. Total price is calculated and stored
4. Order status can be: Pending → Shipped → Delivered

### 8.3 Payment Flow
1. Create a **Payment** linked to an **Order**
2. Set payment method, status, and transaction ID
3. Payment status tracks the transaction state

---

## 9. API Summary Table

| App | Total Endpoints | ViewSets |
|-----|-----------------|----------|
| Accounts | 10 | 2 (User, Role) |
| Products | 22 | 6 (Category, Product, Variant, Color, Size, Unit) |
| Orders | 5 | 1 (Order) |
| Payments | 5* | 1 (Payment) |
| **Total** | **42+** | **10** |

*Note: Payments endpoints are commented out in main URL configuration

---

## 10. Running the Project

### Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary pillow
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
```

### Access Admin Panel
- URL: `http://localhost:8000/admin/`

---

## 11. Future Improvements

1. **Uncomment Payments URLs**: Enable payment endpoints in main URL configuration
2. **Add Product Permissions**: Implement admin-only product management
3. **Order Status Updates**: Add workflow for order status changes
4. **Shopping Cart**: Implement cart functionality
5. **Reviews & Ratings**: Add product review system
6. **Shipping**: Add shipping address management
7. **Notifications**: Email/push notifications for orders
