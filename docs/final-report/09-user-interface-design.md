# User Interface Design

## Overview

The Supplier Consumer Platform (SCP) supports multiple user interfaces:
- **Mobile Application** - For consumers and supplier sales representatives
- **Web Application (Admin)** - For supplier owners and managers

**Note:** This section documents the UI requirements. Actual screenshots should be added when available.

---

## Mobile Application (Consumer)

### Consumer Staff Interface

#### Screen 1: Login Screen
- **Language:** English, Russian, Kazakh (i18n)
- **Fields:** Email, Password
- **Actions:** Login button, Register link
- **Features:** Language selector, Remember me option

#### Screen 2: Dashboard
- **Language:** Based on user locale (EN/RU/KZ)
- **Content:** 
  - List of linked suppliers
  - Recent orders summary
  - Pending link requests
- **Currency:** Prices displayed in KZT (₸) format
- **Navigation:** Bottom navigation bar (Home, Orders, Suppliers, Profile)

#### Screen 3: Supplier Catalog
- **Language:** Based on user locale
- **Content:**
  - Product grid/list view
  - Product images, names, prices
  - Stock availability indicators
  - Search and filter options
- **Currency:** Prices in KZT format (e.g., "5 000 ₸")
- **Actions:** Add to cart, View product details

#### Screen 4: Product Details
- **Language:** Based on user locale
- **Content:**
  - Product images (swipeable gallery)
  - Product name, description
  - Pricing: Retail price, Bulk price (if applicable)
  - Stock quantity
  - Minimum order quantity
- **Currency:** KZT formatting
- **Actions:** Add to cart, Adjust quantity

#### Screen 5: Shopping Cart
- **Language:** Based on user locale
- **Content:**
  - List of selected products
  - Quantities, unit prices
  - Total price calculation
- **Currency:** Total in KZT format
- **Actions:** Update quantities, Remove items, Place order

#### Screen 6: Order Confirmation
- **Language:** Based on user locale
- **Content:**
  - Order summary
  - Order ID
  - Estimated delivery information
- **Currency:** Total in KZT
- **Actions:** View order details, Track order

#### Screen 7: Order Tracking
- **Language:** Based on user locale
- **Content:**
  - Order status timeline (created → processing → shipping → completed)
  - Order details and products
  - Total price
- **Currency:** KZT formatting
- **Actions:** View order details, Chat with supplier, Create complaint

#### Screen 8: Chat Screen
- **Language:** Based on user locale
- **Content:**
  - Message history (scrollable)
  - Message bubbles (sent/received)
  - System messages (order updates, complaint notifications)
- **Features:** Real-time updates, File attachment (future), Audio messages (future)
- **Actions:** Send message, Attach file (future)

#### Screen 9: Complaint Creation
- **Language:** Based on user locale
- **Content:**
  - Order information
  - Complaint description text area
  - Attach images option (future)
- **Actions:** Submit complaint, Cancel

#### Screen 10: Complaint Status
- **Language:** Based on user locale
- **Content:**
  - Complaint details
  - Status timeline (open → in_progress → resolved)
  - Resolution notes (when resolved)
- **Actions:** View complaint history, Chat about complaint

---

## Mobile Application (Supplier - Sales Representative)

### Sales Representative Interface

#### Screen 1: Login Screen
- Same as consumer login with supplier branding

#### Screen 2: Dashboard
- **Language:** Based on user locale
- **Content:**
  - Pending link requests
  - New orders
  - Assigned complaints
  - Recent chat messages
- **Currency:** KZT formatting for order values
- **Navigation:** Bottom navigation (Home, Orders, Complaints, Chat, Profile)

#### Screen 3: Link Requests
- **Language:** Based on user locale
- **Content:**
  - List of pending link requests from consumers
  - Consumer company information
  - Request message
- **Actions:** Approve, Reject, View consumer details

#### Screen 4: Orders List
- **Language:** Based on user locale
- **Content:**
  - List of orders (filterable by status)
  - Order ID, consumer name, total price, status
  - Order date
- **Currency:** KZT formatting
- **Actions:** View order details, Update status

#### Screen 5: Order Details
- **Language:** Based on user locale
- **Content:**
  - Order information
  - Product list with quantities
  - Total price
  - Status timeline
- **Currency:** KZT formatting
- **Actions:** Update status, Chat with consumer

#### Screen 6: Complaints List
- **Language:** Based on user locale
- **Content:**
  - Assigned complaints
  - Complaint status, order ID, consumer name
  - Created date
- **Actions:** View complaint, Resolve, Escalate

#### Screen 7: Complaint Details
- **Language:** Based on user locale
- **Content:**
  - Complaint description
  - Associated order details
  - Status and history
  - Resolution notes field
- **Actions:** Resolve complaint, Escalate to manager, Add notes

#### Screen 8: Chat Screen
- Similar to consumer chat interface
- **Features:** Real-time messaging, System notifications

---

## Web Application (Admin - Supplier)

### Supplier Owner/Manager Interface

#### Screen 1: Login Screen
- **Language:** English, Russian, Kazakh selector
- **Fields:** Email, Password
- **Features:** Language selector, Remember me

#### Screen 2: Dashboard
- **Language:** Based on user locale
- **Content:**
  - Company statistics (orders, complaints, products)
  - Recent activity feed
  - Quick actions
- **Currency:** KZT formatting for financial data
- **Navigation:** Sidebar navigation menu

#### Screen 3: User Management
- **Language:** Based on user locale
- **Content:**
  - Table of company users
  - User details: Name, Email, Role, Status
  - Actions column
- **Actions:** Create user, Edit user, Delete user, Suspend/Activate
- **RBAC:** Only Owner and Manager can access

#### Screen 4: Product Catalog Management
- **Language:** Based on user locale
- **Content:**
  - Product table/grid
  - Product details: Name, Price, Stock, Status
  - Search and filter options
- **Currency:** KZT formatting for prices
- **Actions:** Add product, Edit product, Delete product, Update stock
- **RBAC:** Owner and Manager only

#### Screen 5: Product Form (Create/Edit)
- **Language:** Based on user locale
- **Fields:**
  - Product name (required)
  - Description (textarea)
  - Images (upload multiple, preview)
  - Stock quantity
  - Retail price (KZT)
  - Bulk price threshold
  - Bulk price (KZT)
  - Minimum order quantity
  - Unit (kg, piece, etc.)
  - Availability toggle
- **Currency:** All prices in KZT format
- **Actions:** Save, Cancel, Delete (if editing)

#### Screen 6: Orders Management
- **Language:** Based on user locale
- **Content:**
  - Orders table with filters
  - Columns: Order ID, Consumer, Date, Total, Status
  - Status badges (color-coded)
- **Currency:** KZT formatting
- **Actions:** View order, Update status, Filter by status
- **RBAC:** All supplier users can view, Manager/Owner can update

#### Screen 7: Order Details
- **Language:** Based on user locale
- **Content:**
  - Order information panel
  - Product list with quantities and prices
  - Status timeline visualization
  - Total price
- **Currency:** KZT formatting
- **Actions:** Update status, View chat, View complaint (if exists)

#### Screen 8: Complaints Management
- **Language:** Based on user locale
- **Content:**
  - Complaints table
  - Filters: Status, Assigned to, Date range
  - Columns: Complaint ID, Order ID, Consumer, Status, Assigned to, Date
- **Actions:** View complaint, Claim (for managers), Resolve, Escalate
- **RBAC:** Different views based on role (assigned, escalated, all company)

#### Screen 9: Complaint Details
- **Language:** Based on user locale
- **Content:**
  - Complaint description
  - Associated order information
  - Status timeline
  - History log
  - Resolution notes field
  - Cancel order option (Manager only)
- **Actions:** Resolve, Close, Escalate, Add notes

#### Screen 10: Linkings Management
- **Language:** Based on user locale
- **Content:**
  - Linkings table
  - Columns: Consumer Company, Status, Requested Date, Salesman
  - Status filters
- **Actions:** Approve, Reject, Assign salesman, View details

#### Screen 11: Company Profile
- **Language:** Based on user locale
- **Content:**
  - Company information form
  - Logo upload (preview)
  - Company details: Name, Description, Location
- **Actions:** Update profile, Upload logo, Save
- **RBAC:** Owner only

#### Screen 12: Chat Interface
- **Language:** Based on user locale
- **Content:**
  - Chat list (linkings and orders)
  - Message panel
  - Message history
  - System notifications
- **Features:** Real-time updates, File attachments (future)

---

## Internationalization (i18n)

### Supported Languages
- **English (EN)** - Default
- **Russian (RU)** - Cyrillic script
- **Kazakh (KZ)** - Cyrillic script

### Implementation
- User locale stored in user profile
- UI text translated based on locale
- City names available in all three languages
- Currency formatting: KZT (Kazakhstani Tenge)

### Currency Formatting (KZT)
- **Format:** `{amount} ₸` or `{amount} KZT`
- **Thousands separator:** Space (e.g., "5 000 ₸")
- **Decimal places:** 0 (KZT has no subdivisions)
- **Examples:**
  - `1 500 ₸`
  - `10 000 ₸`
  - `250 000 ₸`

---

## UI/UX Design Principles

### Design System
- **Color Scheme:** Professional, business-appropriate colors
- **Typography:** Clear, readable fonts with proper hierarchy
- **Spacing:** Consistent spacing and padding
- **Icons:** Consistent icon set (Material Icons or similar)

### Responsive Design
- **Mobile:** Optimized for iOS and Android
- **Web:** Responsive design for desktop and tablet
- **Breakpoints:** Mobile-first approach

### Accessibility
- **WCAG 2.1 AA Compliance:** Target standard
- **Keyboard Navigation:** Full keyboard support
- **Screen Readers:** Proper ARIA labels
- **Color Contrast:** Sufficient contrast ratios

### User Experience
- **Loading States:** Clear loading indicators
- **Error Handling:** User-friendly error messages
- **Success Feedback:** Confirmation messages for actions
- **Empty States:** Helpful empty state messages
- **Onboarding:** User guides for first-time users

---

## Screenshots Placeholder

**TODO:** Add screenshots for the following:

### Mobile (Consumer)
1. Login screen
2. Dashboard
3. Supplier catalog
4. Product details
5. Shopping cart
6. Order tracking
7. Chat interface
8. Complaint creation

### Mobile (Supplier)
1. Dashboard
2. Link requests
3. Orders list
4. Complaint management
5. Chat interface

### Web (Admin)
1. Dashboard
2. User management
3. Product catalog
4. Orders management
5. Complaints management
6. Company profile

**Note:** Screenshots should demonstrate:
- Multi-language support (EN/RU/KZ)
- KZT currency formatting
- Role-based UI differences
- Responsive design

---

## Design Tools

- **Figma:** Recommended for UI/UX design and prototyping
- **Design System:** Consistent component library
- **Prototyping:** Interactive prototypes for user testing

---

## Future UI Enhancements

- Dark mode support
- Advanced filtering and search
- Data visualization (charts, graphs)
- Export functionality (orders, reports)
- Mobile push notifications
- Email notifications with templates
- SMS notifications
- Real-time order tracking map
- Product image gallery with zoom
- Voice messages in chat
- Video call integration (future)

