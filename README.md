# Shop Manager 🏪

A desktop application built with Python and CustomTkinter for managing shop operations including inventory, suppliers, and billing. This application provides a modern, intuitive interface for small business management.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📦 Inventory Manager
- Add new items with name, price, and stock quantity
- Edit existing items (auto-updates if item name already exists)
- Delete items from inventory
- Visual low-stock alerts (items with ≤3 units shown in red)
- Real-time stock level tracking

### 👤 Supplier Log
- Maintain a database of suppliers with contact information
- Add, update, and delete supplier records
- Store supplier name, phone number, and address
- Easy-to-view supplier table

### 🛒 Billing (Cash Register)
- Select items from inventory with autocomplete dropdown
- Add items to cart with quantity validation
- Real-time cart total calculation
- Stock validation (prevents selling more than available)
- Automatic stock deduction upon bill generation
- Clear cart functionality

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **CustomTkinter** - Modern UI framework for Tkinter
- **SQLite3** - Lightweight embedded database
- **CTkScrollableDropdown** - Enhanced dropdown with scroll and autocomplete

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher installed
- pip package manager

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shop-manager.git
   cd shop-manager
   ```

2. **Install required dependencies**
   ```bash
   pip install customtkinter
   pip install CTkScrollableDropdown
   ```

   Or install from requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
shop-manager/
│
├── CTkScrollableDropdown   # Library imported         
├── main.py                 # Main application file
├── shop_manager.db         # SQLite database (auto-generated)
├── README.md               # Project documentation
└── LICENSE                 # License file
```

## 🎮 Usage Guide

### Inventory Management

1. Navigate to **Inventory Manager** from the sidebar
2. Enter item details:
   - Item Name (e.g., "Bread")
   - Price in ₹ (e.g., 25.00)
   - Stock quantity (e.g., 50)
3. Click **"Save Item to Inventory"**
4. View all items in the table on the right
5. Click the 🗑 button to delete an item

### Managing Suppliers

1. Navigate to **Supplier Log** from the sidebar
2. Enter supplier details:
   - Supplier/Company name
   - Phone number
   - Address
3. Click **"Add Supplier Record"**
4. View and manage suppliers in the table

### Processing Bills

1. Navigate to **Billing (Cash Register)** from the sidebar
2. Select an item from the dropdown (shows available stock)
3. Enter the quantity
4. Click **"Add to Billing Cart"**
5. Review cart items and total
6. Click **"Generate Bill & Update Stock"** to complete the transaction

## 🗄️ Database Schema

### Items Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| name | TEXT | Unique item name |
| price | REAL | Item price |
| stock | INTEGER | Available stock |

### Suppliers Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| name | TEXT | Supplier/company name |
| phone | TEXT | Contact number |
| address | TEXT | Supplier address |

## 🔧 Configuration

### Window Settings
You can modify the default window size in `main.py`:
```python
self.geometry("950x600")  # Width x Height
self.minsize(900, 550)    # Minimum window size
```

### Low Stock Threshold
To change the low stock alert threshold (default is 3):
```python
if stock <= 3:  # Change this value
    # Display in red
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown) - Scrollable dropdown component
- Python community for excellent documentation and support


---
@chirag982 

⭐ If you found this project helpful, please give it a star!