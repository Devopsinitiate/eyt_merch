Below is a **clean, structured, and professional MVP documentation** for **EYTGaming Mesh (Merch) Sales Platform**, organized for clarity and future scalability, while staying **minimal and practical**.

---

# EYTGaming Merchandise Sales MVP

**Project Documentation**

## Project Name

**EYT GAMER ARMY — Gear Up for 2026 🎮**

## Company

**EYTGaming**

## Product

**THE DOJO Under Sweatshirt (Mesh / Long Sleeve Gaming Wear)**

---

## 1. Project Overview

EYTGaming is launching its first official merchandise sales platform to unite its gaming community under a single identity. The MVP focuses on **selling limited-edition gaming mesh apparel**, collecting orders efficiently, and exporting structured sales data for production and fulfillment.

This MVP prioritizes:

* Speed to market
* Simple registration & order flow
* Excel-based order management
* Clean, branded user experience

---

## 2. Business Goals

* Launch official EYTGaming merch for 2026
* Create a unified “EYT Gamer Army” identity
* Sell limited stock efficiently (first-come, first-served)
* Collect accurate order data (size, name, number, color)
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

* Product showcase page
* Registration / order form
* Size availability control
* Order summary view (admin)
* Excel (.xlsx) export of orders
* Admin-only order dashboard

### Excluded (Future Versions)

* Online payments
* User accounts
* Shipping automation
* Inventory automation
* Multiple products

---

## 5. Tech Stack

### Backend

* **Django (Python)**
* Django ORM
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
Product Page (Tailwind + HTML)
   ↓
Order Form (Vanilla JS validation)
   ↓
Django Backend
   ↓
Database (Orders, Sizes)
   ↓
Admin Dashboard
   ↓
Excel Export (.xlsx)
```

---

## 7. Core Features

### 7.1 Product Display

* Front & back product mockups
* Clear pricing
* Available sizes indicator
* Color selection
* Brand messaging

---

### 7.2 Registration / Order Flow

**User fills form with:**

* Full Name
* Gamer Tag / Preferred Name
* Preferred Number
* Size (dropdown – filtered by availability)
* Colorway
* Contact (Phone / Email)

**Validation Rules**

* Required fields enforced
* Size availability checked before submission
* Prevent duplicate orders (basic check)

---

### 7.3 Size Availability Management

* Sizes have limited stock (e.g. ASH – 37 units)
* Once a size reaches zero:

  * Automatically hidden or disabled on frontend
* Admin can manually adjust stock

---

### 7.4 Admin Dashboard

Admin can:

* View all orders
* Filter by:

  * Size
  * Color
  * Date
* Track total units sold
* Export data to Excel

---

### 7.5 Excel Export (Key MVP Feature)

**Export Format Example:**

| Order ID | Name | Gamer Tag | Number | Size | Color | Date |
| -------- | ---- | --------- | ------ | ---- | ----- | ---- |

* One-click export
* Used for:

  * Printing
  * Production batching
  * Logistics
* Matches production requirement layout

---

## 8. Data Models (Simplified)

### Order Model

* id
* full_name
* gamer_tag
* preferred_number
* size
* color
* created_at

### Size Model

* name (S, M, L, XL, 2XL)
* available_quantity

---

## 9. User Journey

1. User lands on **EYT DOJO Merch Page**
2. Reads brand message:

   > *The DOJO is our home. Our uniform signifies what we stand for.*
3. Views product mockups
4. Selects:

   * Color
   * Size
5. Completes registration form
6. Submits order
7. Receives confirmation message
8. Admin exports Excel for fulfillment

---

## 10. Branding & UI Guidelines

### Visual Style

* Dark, minimal, esports-inspired
* Neutral backgrounds (ash, dark grey)
* Bold typography
* Strong contrast

### Fonts

* Sans-serif (clean & modern)
* Large headings for calls-to-action

### UX Principles

* Minimal clicks
* Clear availability
* Mobile-friendly
* Fast loading

---

## 11. Deployment (MVP)

* Hosted on VPS or shared hosting
* Gunicorn + Nginx (recommended)
* SQLite (MVP) → PostgreSQL (later)
* Admin access secured

---

## 12. Future Enhancements

* Online payment integration
* User order tracking
* Automated inventory deduction
* Multiple merch drops
* Shipping & pickup logic
* QR-based order confirmation

---

## 13. Conclusion

This MVP allows **EYTGaming** to:

* Launch merch quickly
* Control inventory manually
* Capture clean, production-ready data
* Build community identity
* Scale confidently in future drops

**Simple. Strong. United.**
