Below is an **updated and improved version of the documentation**, revised to **explicitly include User Signup / Registration**, while still keeping the MVP lean, practical, and production-ready.

I’ve **integrated signup cleanly into the flow** (before ordering), without turning this into a full-blown account system.

---

# EYTGaming Merchandise Sales MVP

**Project Documentation (Updated with User Signup & Registration)**

## Project Name

**EYT GAMER ARMY — Gear Up for 2026 🎮**

## Company

**EYTGaming**

## Product

**THE DOJO Under Sweatshirt (Mesh / Long Sleeve Gaming Wear)**

---

## 1. Project Overview

EYTGaming is launching its first official merchandise sales platform to unite its gaming community under a single identity. The MVP focuses on **selling limited-edition gaming mesh apparel**, onboarding users through a simple signup process, collecting orders efficiently, and exporting structured sales data for production and fulfillment.

This MVP prioritizes:

* Speed to market
* Simple **user signup + order flow**
* Excel-based order management
* Clean, branded esports experience
* Minimal backend complexity

---

## 2. Business Goals

* Launch official EYTGaming merch for 2026
* Build a verified **EYT Gamer Army user base**
* Sell limited stock efficiently (first-come, first-served)
* Collect accurate user & order data
* Export orders to Excel for logistics and production
* Avoid over-engineering (no payment gateway in MVP)

---

## 3. Product Description

### Product Name

**THE DOJO Under Sweatshirt**

### Description

Designed for class and undeniable presence.
Features **premium puff-print style** for superior quality and durability.
Built for gamers who represent discipline, unity, and dominance in the e-sports space.

### Colorways

* Blue
* Light Heather Grey

### Sizes Available

* S
* M
* L
* XL
* 2XL

> Only available sizes will be served first. More sizes coming soon.

### Fit Recommendation

➤ **Select one size up for the perfect fit**
Example: *CHUX wears a 2XL*

---

## 4. MVP Scope

### Included

* Public product landing page
* **User signup / registration**
* Logged-in order placement
* Size availability control
* Order summary view (admin)
* Excel (.xlsx) export of orders
* Admin-only dashboard

### Excluded (Future Versions)

* Online payments
* Order history per user
* Shipping automation
* Inventory automation
* Multiple product catalog

---

## 5. Tech Stack

### Backend

* **Django (Python)**
* Django ORM
* Django Authentication System
* Django Admin

### Frontend

* **HTML**
* **Vanilla JavaScript**
* **Tailwind CSS**

### Data & Export

* **Excel Export (XLSX)**
* openpyxl / pandas (Python)

---

## 6. System Architecture (High-Level)

```
User Browser
   ↓
Landing Page (Tailwind + HTML)
   ↓
Signup / Login
   ↓
Product Page
   ↓
Order Form (JS validation)
   ↓
Django Backend
   ↓
Database (Users, Orders, Sizes)
   ↓
Admin Dashboard
   ↓
Excel Export (.xlsx)
```

---

## 7. Core Features

### 7.1 User Signup & Registration (NEW)

**Purpose:**
To identify each member of the **EYT Gamer Army** and link orders to real users.

#### Signup Fields

* Full Name
* Gamer Tag
* Email Address
* Phone Number
* Password

#### Rules

* Email must be unique
* Password stored securely (Django auth)
* Gamer Tag used for personalization

#### Login

* Email + password
* Session-based authentication

> MVP uses **Django’s built-in authentication**, customized lightly for branding.

---

### 7.2 Product Display

* Front & back product mockups
* Clear pricing
* Available sizes indicator
* Color selection
* Brand storytelling

---

### 7.3 Order Flow (Authenticated Users Only)

**User must be logged in to place an order**

**Order Form Fields**

* Preferred Name (printed name)
* Preferred Number
* Size (filtered by availability)
* Colorway

**Validation Rules**

* All required fields enforced
* Size availability checked server-side
* One active order per user (MVP rule)

---

### 7.4 Size Availability Management

* Sizes have limited stock (e.g. ASH – 37 units)
* Once a size reaches zero:

  * Disabled or hidden automatically
* Admin can manually update stock

---

### 7.5 Admin Dashboard

Admin can:

* View all registered users
* View all orders
* Filter orders by:

  * Size
  * Color
  * Date
* Track total units sold
* Export orders to Excel

---

### 7.6 Excel Export (Key MVP Feature)

**Export Format Example**

| Order ID | User Name | Gamer Tag | Number | Size | Color | Date |
| -------- | --------- | --------- | ------ | ---- | ----- | ---- |

**Features**

* One-click export
* Production-ready format
* Used for:

  * Printing
  * Batch production
  * Logistics
* Matches manufacturer requirements

---

## 8. Data Models (Simplified)

### User Model (Django Auth – Extended)

* id
* full_name
* email
* phone
* gamer_tag
* password
* created_at

---

### Order Model

* id
* user (FK)
* preferred_name
* preferred_number
* size
* color
* created_at

---

### Size Model

* name (S, M, L, XL, 2XL)
* available_quantity

---

## 9. User Journey (Updated)

1. User lands on **EYT DOJO Merch Page**
2. Reads brand message:

   > *The DOJO is our home. Our uniform signifies what we stand for.*
3. Clicks **Join the EYT Clan**
4. Signs up / logs in
5. Views product mockups
6. Selects:

   * Color
   * Size
7. Completes order form
8. Submits order
9. Receives confirmation message
10. Admin exports Excel for fulfillment

---

## 10. Branding & UI Guidelines

### Visual Style

* Dark, minimal, esports-inspired
* Neutral tones (ash, dark grey)
* Red accent for power & identity
* Bold typography

### UX Principles

* Simple onboarding
* Minimal clicks
* Clear size availability
* Mobile-first
* Fast load times

---

## 11. Deployment (MVP)

* VPS or shared hosting
* Gunicorn + Nginx
* SQLite (MVP) → PostgreSQL (Scale)
* Secure admin routes
* Environment variables for secrets

---

## 12. Future Enhancements

* Payment gateway integration
* User order history
* Automated inventory deduction
* Multiple merch drops
* Shipping vs pickup selection
* QR-based order verification
* Email notifications

---

## 13. Conclusion

This MVP enables **EYTGaming** to:

* Build a verified gamer community
* Launch merch with confidence
* Maintain production accuracy
* Scale seamlessly into future drops

**The DOJO is ready.
The uniform is defined.
The Gamer Army is forming. 🎮🔥**

